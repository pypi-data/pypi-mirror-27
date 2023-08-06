#!/usr/bin/env python3

"""
    Copyright (c) 2017 Martin F. Falatic

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.

"""

import telnetlib
import time
import argparse
import signal
import sys
from os.path import expanduser
from colorama import Fore, Back, Style
# from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.history import FileHistory
from prompt_toolkit import prompt
try:
    from remotepdb_client.__config__ import PACKAGE_DATA
except ModuleNotFoundError:
    from __config__ import PACKAGE_DATA


TITLE = "{} v{}".format(PACKAGE_DATA['friendly_name'], PACKAGE_DATA['version'])

RESET_COLOR = ''


def exit_handler():
    print()
    print(RESET_COLOR + "Exiting...")
    sys.exit(0)


def signal_handler(signal, frame):
    print()
    exit_handler()


def pad_line(padding=0):
    for _ in range(padding):
        print()


def setup(params):
    signal.signal(signal.SIGINT, signal_handler)

    default_host = 'localhost'
    default_port = 4544
    default_delay = 0.5  # seconds between retries
    minimum_delay = 0.1
    default_theme = 'none'
    default_prompt = '(Pdb) '  # trailing spaces are important
    default_pad_before = 0
    default_pad_after = 1

    def port_value(string):
        value = int(string)
        if not (0 <= value <= 65535):
            msg = "Port {} is invalid".format(string)
            raise argparse.ArgumentTypeError(msg)
        return value

    def delay_value(string):
        value = float(string)
        if value and value < minimum_delay:
            msg = "{} is less than minimum delay {}".format(string, minimum_delay)
            raise argparse.ArgumentTypeError(msg)
        return value

    parser = argparse.ArgumentParser(
        description="{} - {}".format(TITLE, PACKAGE_DATA['description']),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('--host', metavar='HOST_NAME', required=False,
                        type=str, default=default_host,
                        help='hostname to connect to')
    parser.add_argument('--port', metavar='PORT', required=False,
                        type=port_value, default=default_port,
                        help='port to connect to')
    parser.add_argument('--delay', metavar='DELAY_SECS', required=False,
                        type=delay_value, default=default_delay,
                        help='connection retry delay')
    parser.add_argument('--theme', metavar='THEME_NAME', required=False,
                        type=str, default=default_theme,
                        help='output theme (dark, light, none)')
    parser.add_argument('--padbefore', required=False,
                        type=int, metavar='LINES', default=default_pad_before,
                        help='pad before remote lines')
    parser.add_argument('--padafter', metavar='LINES', required=False,
                        type=int, default=default_pad_after,
                        help='pad after remote lines')
    parser.add_argument('--prompt', metavar='STRING', required=False,
                        type=str, default=default_prompt,
                        help='remote prompt incl. trailing spaces')
    args = parser.parse_args()

    params['host'] = args.host if args.host else default_host
    params['port'] = args.port
    params['delay'] = args.delay
    params['prompt'] = args.prompt if args.prompt else default_prompt
    params['pad_before'] = args.padbefore
    params['pad_after'] = args.padafter

    theme = {
        'none': {
            'color_default': '',
            'color_prompt': '',
            'color_cmd': '',
            'color_output': '',
            'color_wait': '',
            'color_alert': '',
        },
        'light': {
            'color_default': Style.RESET_ALL,
            'color_prompt': Style.DIM + Fore.GREEN,
            'color_cmd': Style.NORMAL + Fore.BLUE,
            'color_output': Style.NORMAL + Fore.BLACK,
            'color_wait': Style.NORMAL + Fore.CYAN,
            'color_alert': Style.NORMAL + Fore.RED,
        },
        'dark': {
            'color_default': Style.RESET_ALL,
            'color_prompt': Style.BRIGHT + Fore.GREEN,
            'color_cmd': Style.NORMAL + Fore.YELLOW,
            'color_output': Style.NORMAL + Fore.WHITE,
            'color_wait': Style.NORMAL + Fore.CYAN,
            'color_alert': Style.NORMAL + Fore.RED,
        },
    }
    params['theme'] = args.theme.lower() if args.theme else default_theme
    params.update(theme[params['theme']])
    global RESET_COLOR
    RESET_COLOR = params['color_default']

    # params['history'] = InMemoryHistory()
    params['history'] = FileHistory(expanduser("~/.remotepdb_history"))

    return params


def connector(params):
    remote = telnetlib.Telnet(params['host'], params['port'])
    textout = ''
    read_remote = True
    while textout not in ['c', 'q']:
        if read_remote:
            textin = remote.read_until(params['prompt'].encode('ascii'))
            text_main = textin.decode('ascii').rsplit(params['prompt'], 1)
            pad_line(params['pad_before'])
            print(params['color_output'] + text_main[0], end='')
            pad_line(params['pad_after'])
            print(params['color_prompt'] + params['prompt'].strip() + params['color_cmd'] + ' ', end='')
        try:
            textout = prompt(history=params['history']).strip()
        except KeyboardInterrupt:
            exit_handler()
        if textout in ['cl', 'clear']:
            pad_line(params['pad_before'])
            print(params['color_alert'] + "{} is not allowed here (would block on stdin on the server)".format(textout))
            pad_line(params['pad_after'])
            print(params['color_prompt'] + params['prompt'].strip() + params['color_cmd'] + ' ', end='', flush=True)
            read_remote = False
        else:
            remote.write(textout.encode('ascii') + b'\n')
            read_remote = True
        if textout in ['e', 'exit', 'q', 'quit']:
            exit_handler()


def main(params={}):
    setup(params=params)
    print()
    print("{} debugging via {}:{}".format(TITLE, params['host'], params['port']))
    waiting = False
    while 1:
        try:
            connector(params=params)
            waiting = False
        except (ConnectionRefusedError, EOFError):
            if not waiting:
                pad_line(params['pad_before'])
                print(params['color_wait'] + "Waiting for breakpoint/trace...")
                pad_line(params['pad_after'])
                waiting = True
            time.sleep(params['delay'])


if __name__ == '__main__':
    main()
