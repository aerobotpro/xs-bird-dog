# xs-bird-dog
An aggressive, programmable crawler, that doesn't follow the rules.
For proof of concept only.

[!](https://content.osgnetworks.tv/gundog/content/photos/bracco-italiano-holding-rooster.jpg)

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
# Notes

- Saves one JSON file per generation to `/current_dir/data/saves/`.

- Adjust `drop_expressions` + `seek_expressions` in *config.py* to target your querying.

# TODOS

- Fix Proxy-Usage.

- Search all text in each webpage for `seek_expressions`.

- Utilize headless browser to render js using `requests-html` instead of non-js rendering `python requests` (current).

- Add expressions to `drop_expressions` to avoid all ui/site-based links(junk) like cdn's etc.

