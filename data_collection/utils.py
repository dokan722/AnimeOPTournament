import os
import time
from typing import List
from requests import Response


separator = '#SEP#'
class Colors:
    grey = '\033[90m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    end_color = '\033[0m'

def color_text(text: str, color: str) -> str:
    return f'{color}{text}{Colors.end_color}'

def check_limit_and_wait(r: Response) -> None:
    remaining = r.headers['X-RateLimit-Remaining']
    if remaining == '0':
        print(color_text('Waiting 60 seconds for more requests', Colors.yellow))
        time.sleep(60)
    else:
        time.sleep(0.3)

def write_lines(filename: str, lines: List[str]) -> None:
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        for lines in lines:
            f.write(lines + "\n")