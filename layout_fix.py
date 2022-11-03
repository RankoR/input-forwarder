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

# This (whole file) is a rough hack to detect invalid layout
# For now it considers RU layout only and will fail if we have more than two layouts

import platform
from typing import List

from pynput import keyboard

RUSSIAN_CHARS = 'йцукенгшщзхъ' \
                'фывапролджэ' \
                'ячсмитьбю'

INVALID_LAYOUT_CHARS = RUSSIAN_CHARS

SYSTEM_MACOS = 'Darwin'


def is_valid_layout_char(char) -> bool:
    return char not in INVALID_LAYOUT_CHARS


def get_layout_switch_shortcut_keys() -> List[keyboard.Key]:
    system = platform.system()
    if system == SYSTEM_MACOS:
        return [keyboard.Key.cmd, keyboard.Key.space]  # Hack, as the shortcut may differ
    else:
        return []
