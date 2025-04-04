# dhbw-labor-netztechnik

## Execution

1. create a python virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

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

Note that edges are symmetrical - if an edge `a.b` has been specifyed, specifying it again as `b.a` is redundant. In case such redundant configuration exists, it is the first configuration that will be used.
