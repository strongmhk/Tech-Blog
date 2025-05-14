import feedparser
import git
import os

rss_url = 'https://api.velog.io/rss/@alsgudtkwjs'
repo_path = '.'
posts_dir = os.path.join(repo_path, 'velog-posts')
readme_path = os.path.join(repo_path, 'README.md')

if not os.path.exists(posts_dir):
    os.makedirs(posts_dir)

repo = git.Repo(repo_path)
feed = feedparser.parse(rss_url)

has_changes = False

# Markdown 파일 저장
for entry in feed.entries:
    file_name = entry.title.replace('/', '-').replace('\\', '-') + '.md'
    file_path = os.path.join(posts_dir, file_name)
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(entry.description)
        has_changes = True

# README.md 생성
latest_entries = feed.entries[:5]
readme_content = """## My Velog

<p>
  <a href="https://velog.io/@alsgudtkwjs" target="_blank">
    <img src="https://img.shields.io/badge/Velog-20C997?style=flat&logo=velog&logoColor=white"/>
  </a>
</p>

## 📕 Latest Blog Posts

"""

for entry in latest_entries:
    readme_content += f"- [{entry.title}]({entry.link})\n"

# 변경 감지 및 파일 저장
prev_content = ""
if os.path.exists(readme_path):
    with open(readme_path, 'r', encoding='utf-8') as f:
        prev_content = f.read()

if readme_content != prev_content:
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    has_changes = True

# Git add, commit, push
if has_changes:
    repo.git.add(all=True)
    repo.git.commit('-m', 'Sync latest Velog posts and update README with badge')
    repo.git.push()
