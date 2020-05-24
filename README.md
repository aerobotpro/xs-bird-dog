# xs-bird-dog
An aggressive, programmable crawler, that doesn't follow the rules.
For proof of concept only.

## Requirements
- Python3.6+

## Tests
- Windows(nt)[passing]

# Issues

- Proxy-Usage is **not** working.

- Saves lost @ occasional interpreter crash/stumble due to indexError @ main.py:flex()

## Usage
```bash
cd ~/xs-bird-dog/src
python3 main.py -h
```
```bash
cd ~/xs-bird-dog/src
python3 main.py host-info.net 25
```
```bash
cd ~/xs-bird-dog/src
python3 main.py https://www.instagram.com/joerogan/?hl=en 500
```



