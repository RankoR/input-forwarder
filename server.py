"""
Copyright 2022 Artem Smirnov

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import argparse
import socket
from threading import Event
from time import sleep
from typing import Optional, Tuple

from pynput import keyboard

from data_types import Packet, KEY_ACTION_TYPE_PRESS, KEY_ACTION_TYPE_RELEASE, KEY_TYPE_KEY_CODE, KEY_TYPE_KEY
from layout_fix import is_valid_layout_char, get_layout_switch_shortcut_keys


class KeyboardMonitor(object):
    __ACTIVATION_KEY = keyboard.Key.f13

    __controller = keyboard.Controller()
    __listener: Optional[keyboard.Listener] = None
    __is_redirecting: bool = False

    __client_ip_port: Tuple[str, int]
    __verbose: bool
    __correct_invalid_layout: bool

    __socket: socket.socket

    def __init__(self, client_ip: str, client_port: int, verbose: bool, correct_invalid_layout: bool) -> None:
        super().__init__()

        self.__client_ip_port = (client_ip, client_port)
        self.__verbose = verbose
        self.__correct_invalid_layout = correct_invalid_layout

        self.__socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def start(self):
        def on_press(key):
            if self.__verbose:
                print(f'Pressed: {key}')

            if self.__is_redirecting:
                if self.__correct_invalid_layout and not self.is_valid_layout(key=key):
                    self.stop()
                    sleep(1.0)
                    self.switch_layout()
                    self.start()
                    return

                self.__send_key(key=key, key_action_type=KEY_ACTION_TYPE_PRESS)

        def on_release(key):
            if self.__verbose:
                print(f'Released: {key}')

            if self.__is_redirecting:
                self.__send_key(key=key, key_action_type=KEY_ACTION_TYPE_RELEASE)

            if key == KeyboardMonitor.__ACTIVATION_KEY:
                if self.__verbose:
                    print(f'Activation key detected, current suppress={self.__is_redirecting}')

                self.__is_redirecting = not self.__is_redirecting
                self.start()

        self.stop()

        # noinspection PyTypeChecker
        self.__listener = keyboard.Listener(
            on_press=on_press,
            on_release=on_release,
            suppress=self.__is_redirecting
        )

        self.__listener.start()
        self.__listener.wait()

        print(f'Started, suppress={self.__is_redirecting}')

    def stop(self):
        if self.__listener is not None:
            print('Stopping')
            self.__listener.stop()

    def __send_key(self, key, key_action_type):
        packet: Optional[Packet] = None

        if isinstance(key, keyboard.KeyCode) and hasattr(key, 'char') and key.char is not None:
            packet = Packet(
                key_action_type=key_action_type,
                key_type=KEY_TYPE_KEY_CODE,
                key_value=key.char
            )
        elif isinstance(key, keyboard.Key) and hasattr(key, 'value') and key.value is not None:
            packet = Packet(
                key_action_type=key_action_type,
                key_type=KEY_TYPE_KEY,
                key_value=key.value.vk
            )

        if packet is not None:
            self.__socket.sendto(packet.to_bytes(), self.__client_ip_port)

    def switch_layout(self):
        shortcut_keys = get_layout_switch_shortcut_keys()
        if len(shortcut_keys) == 0:
            print('No shortcut keys found, can not switch layout')
            return

        print(f'Will switch layout with keys = {shortcut_keys}')

        for key in shortcut_keys:
            self.__controller.press(key)
            sleep(0.1)

        sleep(0.5)

        for key in reversed(shortcut_keys):
            self.__controller.release(key)
            sleep(0.1)

        print('Switched layout')

    @staticmethod
    def is_valid_layout(key) -> bool:
        if isinstance(key, keyboard.KeyCode) and hasattr(key, 'char') and key.char is not None:
            return is_valid_layout_char(char=key.char)

        return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--client-ip', type=str, required=True, help='IP of client')
    parser.add_argument('--client-port', type=int, required=True, help='Port of client')
    parser.add_argument('--correct-invalid-layout', action='store_true', default=False, help='Correct invalid layout')
    parser.add_argument('--verbose', action='store_true', default=False, help='Verbose logs')
    args = parser.parse_args()

    client_ip = args.client_ip
    client_port = args.client_port
    correct_invalid_layout = args.correct_invalid_layout
    verbose = args.verbose

    print(f'Starting server with client on {client_ip}:{client_port}, '
          f'correct invalid layout={correct_invalid_layout}, '
          f'verbose={verbose}')

    keyboard_monitor = KeyboardMonitor(
        client_ip=client_ip,
        client_port=client_port,
        verbose=verbose,
        correct_invalid_layout=correct_invalid_layout
    )

    keyboard_monitor.start()

    Event().wait()
