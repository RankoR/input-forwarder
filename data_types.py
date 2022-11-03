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

import dataclasses

import orjson


def dataclass_from_dict(schema: any, data: dict):
    data_updated = {
        key: (
            data[key]
            if not dataclasses.is_dataclass(schema.__annotations__[key])
            else dataclass_from_dict(schema.__annotations__[key], data[key])
        )
        for key in data.keys()
    }
    return schema(**data_updated)


KEY_ACTION_TYPE_PRESS = 0
KEY_ACTION_TYPE_RELEASE = 1

KEY_TYPE_KEY_CODE = 0
KEY_TYPE_KEY = 1


@dataclasses.dataclass
class Packet:
    key_action_type: int
    key_type: int
    key_value: str

    def to_bytes(self) -> bytes:
        return orjson.dumps(self)

    @staticmethod
    def from_bytes(data: bytes) -> 'Packet':
        return dataclass_from_dict(Packet, orjson.loads(data))
