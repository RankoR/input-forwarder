# Keyboard forwarder

Simple keyboard forwarder written in Python 3.

**Use with caution**: it's written in 2 hours, so code is pretty shitty. 
Tested only on macOS server and Linux client.

There is no encryption, so use it in local network only!

There also are some hard-coded things: auto layout change works on macOS only (and only with `cmd+space` shortcut) and for Russian only.

`F13` is also hardcoded as an activation key.

### Terminology

**Server** — computer with keyboard.

**Client** — computer where you want to forward keys to.

### Installation

```shell
git clone https://github.com/RankoR/input-forwarder.git
cd input-forwarder
virtualenv -p python3 venv
. venv/bin/activate
pip install -r requirements.txt
```

### Usage

#### Client

```shell
python client.py --ip 192.168.1.2 --port 31337 --verbose
```

Options:

- `--ip`: IP address to listen on
- `--port`: Port to listen on
- `--verbose`: Optional, for verbose logs (for debugging purposes only)

#### Server

```shell
python server.py --client-ip 192.168.1.2 --client-port 31337 --correct-invalid-layout --verbose 
```

Options:

- `--client-ip`: IP address of the client
- `--client-port`: Port of the client
- `--correct-invalid-layout`: Switch layout if it's incorrect (see warnings above)
- `--verbose`: Optional, for verbose logs (for debugging purposes only)

Then press `F13` to turn on or turn off forwarding.

### License

```
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
```