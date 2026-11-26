# UptimeWatch

A small Python website uptime checker built as Week 1 of the SkillMe DevOps internship task.

## Features

- Reads website URLs from `sites.txt` (one URL per line).
- Reports `UP` or `DOWN`, HTTP status code, and response time in milliseconds.
- Treats HTTP status codes `400` and above as `DOWN`.
- Handles connection errors and timeouts without stopping the remaining checks.
- Returns exit code `1` if at least one website is down, otherwise `0`.

## Requirements

- Python 3.9+
- Internet connection

## Setup

```bash
git clone <https://github.com/11abdo1a7med-collab/uptimewatch.git>
cd <YOUR_REPOSITORY_NAME>

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## Configure websites

Edit `sites.txt` and add one URL per line. Blank lines and lines starting with `#` are ignored.

## Run

```bash
python3 check.py
```

The request timeout is currently set to 5 seconds in `check.py`.

## Check the exit code (Ubuntu/Linux)

Run:

```bash
python3 check.py
echo $?
```

- `0`: all websites are UP.
- `1`: at least one website is DOWN, or the input file could not be read.

## Example output

The exact status codes and response times depend on the network and the websites at runtime.

```text
WEBSITE                                      | STATUS | HTTP | RESPONSE TIME
---------------------------------------------+--------+------+--------------
https://www.google.com                      | UP     | 200  | 120.00 ms
https://example.invalid                     | DOWN   | N/A  | 10.00 ms

Summary: 1 UP, 1 DOWN
```


## Project structure

```text
uptime-watch/
├── check.py
├── sites.txt
├── requirements.txt
├── .gitignore
└── README.md
```
