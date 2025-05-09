import argparse
import os
import re
import time
import requests
from typing import List, Optional, Dict, Set

GITHUB_API_URL = "https://api.github.com/users/{}"
HEADERS = {'Accept': 'application/vnd.github+json'}

# ------------- Utility Functions -------------
def log(msg: str, level: str = "info", verbose: bool = True):
    if verbose or level == "error":
        symbol = {"info": "ℹ️", "error": "❌", "success": "✅", "warn": "⚠️"}.get(level, "")
        print(f"{symbol} {msg}")

def parse_input_line(line: str) -> Optional[str]:
    line = line.strip()
    if not line:
        return None
    if line.startswith("http"):
        match = re.match(r"https?://github\.com/([\w-]+)", line)
        if match:
            return match.group(1)
    elif re.match(r"^[\w-]+$", line):
        return line
    return None

# ------------- GitHub Data --------------
def get_user_data(username: str, retries: int = 3, delay: float = 1.5, verbose: bool = True) -> Optional[Dict]:
    for attempt in range(retries):
        try:
            response = requests.get(GITHUB_API_URL.format(username), headers=HEADERS)
            if response.status_code == 404:
                return None
            elif response.status_code == 403:  # Rate limited
                log(f"Rate limit hit, sleeping for 60s", "warn", verbose)
                time.sleep(60)
                continue
            elif response.status_code != 200:
                log(f"Error fetching {username}: {response.status_code}", "error", verbose)
                continue

            data = response.json()
            if data.get('type') != 'User':
                return None
            name = data.get('name') or ''
            name_parts = name.strip().split()
            first_name = name_parts[0] if name_parts else ''
            last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ''
            return {
                'username': username,
                'html_url': data.get('html_url'),
                'first_name': first_name,
                'last_name': last_name,
                'raw': data
            }
        except requests.RequestException as e:
            log(f"Request error for {username}: {e}", "error", verbose)
            time.sleep(delay)
    return None

def get_user_list(file: Optional[str], inputs: Optional[List[str]]) -> List[str]:
    usernames: Set[str] = set()
    lines: List[str] = []

    if file and os.path.exists(file):
        with open(file, 'r', encoding="utf-8") as f:
            lines.extend(f.readlines())
    if inputs:
        lines.extend(inputs)

    for line in lines:
        uname = parse_input_line(line)
        if uname:
            usernames.add(uname)
    return sorted(usernames)

# ------------- Output Generators -------------
def generate_markdown(users: List[Dict]) -> str:
    md = "# My Friends\n\n"
    for user in users:
        name = f"{user['first_name']} {user['last_name']}".strip() or user['username']
        md += f"- [{name}]({user['html_url']})\n"
    return md

def generate_html(users: List[Dict]) -> str:
    html = "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>My Friends</title>"
    html += "<style>body{font-family:sans-serif;padding:20px;}a{color:#0366d6;text-decoration:none;}li{margin:5px 0;}</style></head><body>"
    html += "<h1>My Friends</h1><ul>"
    for user in users:
        name = f"{user['first_name']} {user['last_name']}".strip() or user['username']
        html += f"<li><a href='{user['html_url']}' target='_blank'>{name}</a></li>"
    html += "</ul></body></html>"
    return html

def save_output(users: List[Dict], verbose: bool = True):
    with open("friends.md", "w", encoding="utf-8") as f_md:
        f_md.write(generate_markdown(users))
    with open("friends.html", "w", encoding="utf-8") as f_html:
        f_html.write(generate_html(users))
    with open("friends.json", "w", encoding="utf-8") as f_json:
        import json
        json.dump([u['raw'] for u in users], f_json, indent=2)

    log("Generated `friends.md`, `friends.html`, and `friends.json`.", "success", verbose)

# ------------- Main -------------
def main():
    parser = argparse.ArgumentParser(description="Generate a list of GitHub friends with profile links.")
    parser.add_argument("-f", "--file", help="Input file containing GitHub usernames or profile URLs")
    parser.add_argument("usernames", nargs="*", help="GitHub usernames or profile URLs")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    usernames = get_user_list(args.file, args.usernames)
    log(f"Found {len(usernames)} potential usernames", "info", args.verbose)

    valid_users: List[Dict] = []
    invalid_users: List[str] = []

    for uname in usernames:
        log(f"Fetching {uname}...", "info", args.verbose)
        user = get_user_data(uname, verbose=args.verbose)
        if user:
            valid_users.append(user)
        else:
            invalid_users.append(uname)

    log(f"Valid users: {len(valid_users)}", "success", args.verbose)
    log(f"Invalid or org accounts: {len(invalid_users)}", "warn", args.verbose)

    sorted_users = sorted(valid_users, key=lambda u: (u['first_name'].lower(), u['last_name'].lower()))
    save_output(sorted_users, verbose=args.verbose)

if __name__ == "__main__":
    main()
