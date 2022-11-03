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
from typing import Optional

from pynput import keyboard

from data_types import Packet, KEY_TYPE_KEY, KEY_TYPE_KEY_CODE, KEY_ACTION_TYPE_PRESS, KEY_ACTION_TYPE_RELEASE


# TODO: Close socket gracefully
class KeyboardClient(object):
    __BUFFER_SIZE = 128

    __ip: str
    __port: int
    __verbose: bool

    __socket: Optional[socket.socket]
    __controller = keyboard.Controller()

    def __init__(self, ip: str, port: int, verbose: bool) -> None:
        super().__init__()

        self.__ip = ip
        self.__port = port
        self.__verbose = verbose

    def start(self):
        self.__socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.__socket.bind((self.__ip, self.__port))

        print(f'Listening on {self.__ip}:{self.__port}')

    def listen(self):
        while True:
            data, _ = self.__socket.recvfrom(KeyboardClient.__BUFFER_SIZE)

            packet = Packet.from_bytes(data)

            self.__handle_packet(packet=packet)

    def __handle_packet(self, packet: Packet):
        if self.__verbose:
            print(f'Handling packet = {packet}')

        key = None

        if packet.key_type == KEY_TYPE_KEY_CODE:
            key = keyboard.KeyCode(char=packet.key_value)
        elif packet.key_type == KEY_TYPE_KEY:
            key = keyboard.Key(value=keyboard.KeyCode(vk=packet.key_value))

        if self.__verbose:
            print(f'Key = {key}')

        if key is None:
            print(f'Key is None for packet = {packet}')
            return

        if packet.key_action_type == KEY_ACTION_TYPE_PRESS:
            self.__controller.press(key)
        elif packet.key_action_type == KEY_ACTION_TYPE_RELEASE:
            self.__controller.release(key)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', type=str, required=True, help='IP to listen on')
    parser.add_argument('--port', type=int, required=True, help='Port to listen on')
    parser.add_argument('--verbose', action='store_true', default=False, help='Verbose')
    args = parser.parse_args()

    ip = args.ip
    port = args.port
    verbose = args.verbose

    print(f'Starting client on {ip}:{port}, verbose={verbose}')

    client = KeyboardClient(ip=ip, port=port, verbose=verbose)
    client.start()
    client.listen()
