# dhbw-labor-netztechnik

## Requirements

- python >= 3.12
- python-venv to run python virtual environments

## Execution

1. create a python virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

> Note that this step can technically be skipped when the packages in requirements.txt are desired to be installed globally.

2. install requirements

```bash
pip install -r requirements.txt
```

3.

```bash
python main.py
```

## Configuration

Configuration happens in the file `network.yml`. It is expected to have the following structure:

```yml
env:
  # environment-variables
switches:
  a:
    mac: "11:11:11:11:11:11"
    priority: 10000
  b: ...

edges:
  a:
    b: 10
    c: 42
```

Note that edges are symmetrical - if an edge `a.b` has been specifyed, specifying it again as `b.a` is redundant. In case such redundant configuration exists, it is the first configuration that will be used.<br>
Note that passing a mac address is not required. If no mac address is found, a node gets assigned a default address of `dd:dd:dd:dd:dd:dd`. Specifying no priority will assign the default priority of `32768`.

### Environment Variables

In the `env` section of the yaml, configure configuration variables that control the behaviour of the algorithm. Two parameters are supported:

- `timeout` (int): The timeout (in seconds) waited by a switch between sending its BPDUs. Defaults to `1`.
- `iterations` (int): How many BPDUs each Switch sends. Defaults to `10`.
