# GitHub Name Friends

A simple Python tool that generates a list of your GitHub friends with their profile links, names, followers, and more. The tool fetches data from GitHub profiles, formats it in multiple output formats (Markdown, HTML, JSON, CSV), and allows you to sort users by name or followers.

## Features

- Fetches GitHub profile data (name, followers, location, bio, etc.)
- Supports input from a file or command line
- Sort users by name or followers
- Output in Markdown, HTML, JSON, and CSV formats

## Installation

1. Clone the repository:

```bash
git clone https://github.com/BaseMax/github-name-friends.git
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a .env file with your GitHub token (optional but recommended for higher API limits):

```plaintext
GITHUB_TOKEN=your_github_token
```

## Usage

### Command-Line Arguments

- `-f`, `--file`: Input file containing GitHub usernames or profile URLs (one per line).
- `usernames`: GitHub usernames or profile URLs directly passed as arguments.
- `-v`, `--verbose`: Enable verbose output (for debugging).
- `--include-orgs`: Include organization accounts.
- `--sort-by`: Sort users by name or followers (default: name).
- `--out-dir`: Directory to save the output files (default: current directory).

## Example Usage

### 1. Using a file:

```bash
$ python github_friends.py -f friends.txt
```

### 2. Using a list of usernames:

```bash
$ python github_friends.py user1 user2 user3
```

### 3. Enabling verbose output:

```bash
$ python github_friends.py user1 -v
```

### 4. Sorting by followers:

```bash
$ python github_friends.py user1 user2 --sort-by followers
```

## Output

The tool will generate the following files in the output directory:

- `friends.md`: A Markdown file with a list of your friends' GitHub profile links.
- `friends.html`: An HTML file with a list of your friends' GitHub profile links.
- `friends.json`: A JSON file containing detailed information about the users.
- `friends.csv`: A CSV file with basic profile information.

### Example Output (Markdown)

```markdown
# My Friends

- [John Doe](https://github.com/johndoe)
- [Jane Smith](https://github.com/janesmith)
```

### Example Output (HTML)

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>My Friends</title>
  <style>body{font-family:sans-serif;padding:20px;}a{color:#0366d6;text-decoration:none;}li{margin:5px 0;}</style>
</head>
<body>
  <h1>My Friends</h1>
  <ul>
    <li><a href="https://github.com/johndoe" target="_blank">John Doe</a></li>
    <li><a href="https://github.com/janesmith" target="_blank">Jane Smith</a></li>
  </ul>
</body>
</html>
```

### License

MIT License - Copyright (c) 2025 Max Base
