import argparse
import os
import re
import requests
from bs4 import BeautifulSoup

GITHUB_API = "https://api.github.com/users/{}"

def parse_input_line(line):
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

def get_user_data(username):
    url = GITHUB_API.format(username)
    response = requests.get(url, headers={'Accept': 'application/vnd.github+json'})
    if response.status_code != 200:
        return None
    data = response.json()
    if data.get('type') != 'User':
        return None
    name = data.get('name') or ''
    name_parts = name.strip().split()
    first_name = name_parts[0] if name_parts else ''
    last_name = name_parts[1] if len(name_parts) > 1 else ''
    return {
        'username': username,
        'html_url': data.get('html_url'),
        'first_name': first_name,
        'last_name': last_name,
    }

def get_user_list(source_file=None, cli_args=None):
    usernames = set()
    lines = []
    if source_file:
        with open(source_file, 'r') as f:
            lines.extend(f.readlines())
    if cli_args:
        lines.extend(cli_args)
    for line in lines:
        uname = parse_input_line(line)
        if uname:
            usernames.add(uname)
    return sorted(usernames)

def generate_markdown(users):
    md = "# My friends\n\n"
    for user in users:
        name = f"{user['first_name']} {user['last_name']}".strip() or user['username']
        md += f"- [{name}]({user['html_url']})\n"
    return md

def generate_html(users):
    html = "<!DOCTYPE html>\n<html><head><meta charset='UTF-8'><title>My Friends</title>"
    html += "<style>body{font-family:sans-serif;padding:20px;}a{color:#0366d6;text-decoration:none;}li{margin:5px 0;}</style></head><body>"
    html += "<h1>My friends</h1>\n<ul>"
    for user in users:
        name = f"{user['first_name']} {user['last_name']}".strip() or user['username']
        html += f"<li><a href='{user['html_url']}' target='_blank'>{name}</a></li>\n"
    html += "</ul></body></html>"
    return html

def main():
    parser = argparse.ArgumentParser(description="Generate list of GitHub friends.")
    parser.add_argument('-f', '--file', help="Input file (one GitHub username or profile URL per line)")
    parser.add_argument('usernames', nargs='*', help="GitHub usernames or URLs directly from CLI")
    args = parser.parse_args()

    usernames = get_user_list(args.file, args.usernames)
    print(f"🔍 Validating and fetching {len(usernames)} users...")

    valid_users = []
    for uname in usernames:
        print(f"→ Fetching {uname}...", end="")
        user_data = get_user_data(uname)
        if user_data:
            print("OK")
            valid_users.append(user_data)
        else:
            print("Invalid or organization")

    sorted_users = sorted(valid_users, key=lambda u: (u['first_name'].lower(), u['last_name'].lower()))

    with open("friends.md", "w", encoding="utf-8") as f:
        f.write(generate_markdown(sorted_users))
    with open("friends.html", "w", encoding="utf-8") as f:
        f.write(generate_html(sorted_users))

    print(f"\n✅ Done! Generated `friends.md` and `friends.html`.")

if __name__ == "__main__":
    main()
