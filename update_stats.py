#!/usr/bin/env python3
import os
import re
from github import Github

# --- CONFIG --- #
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
USERNAME = "BaoTo12"   # ← your GitHub username
README_PATH = "README.md"
START = "<!-- STATS_START -->"
END   = "<!-- STATS_END -->"
# --------------- #

if not GITHUB_TOKEN:
    raise SystemExit("Error: GITHUB_TOKEN not set in environment.")

gh = Github(GITHUB_TOKEN)
user = gh.get_user(USERNAME)

# Fetch stats
total_repos = user.public_repos
followers   = user.followers
# (extend here if you want languages, stars, etc.)

new_stats_md = f"""
**Public repos:** {total_repos}  
**Followers:** {followers}  
_Last updated: {user.updated_at.strftime('%Y-%m-%d %H:%M:%S UTC')}_  
"""

# Read README
with open(README_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Replace between markers
pattern = re.compile(
    rf"({re.escape(START)})(.*?)(\s*{re.escape(END)})",
    flags=re.DOTALL
)
updated = pattern.sub(rf"\1\n{new_stats_md}\3", content)

# Write back if changed
if updated != content:
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(updated)
    print("✅ README.md updated.")
else:
    print("ℹ️  No changes detected.")
