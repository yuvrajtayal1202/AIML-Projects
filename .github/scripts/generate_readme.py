# .github/scripts/generate_readme.py
from github import Github
import os, textwrap

user = os.environ["GH_USERNAME"]
client = Github(os.environ.get("GITHUB_TOKEN"))
me = client.get_user(user)

# Category mapping from topic -> section name
CATEGORY_MAP = {
    "ml": "## 🟢 Beginner / ML Projects",
    "dl": "## 🔴 Deep Learning Projects",
    "end_to_end": "## 🟡 End-to-End Projects",
    "genai": "## 🔵 Generative AI Projects",
    "agenticai": "## 🟣 Agentic AI Projects",
}

# Collect repos by category
projects_by_category = {section: [] for section in CATEGORY_MAP.values()}

for repo in me.get_repos():
    topics = [t.lower() for t in repo.get_topics()]
    for key, section in CATEGORY_MAP.items():
        if key in topics:
            row = f"| **{repo.name}** | {repo.updated_at.strftime('%b %Y')} | 🚧 Active | [View Repo]({repo.html_url}) |"
            projects_by_category[section].append(row)

# Build README
readme = f"""
# 🤖 AI/ML Projects Overview

Welcome to my curated collection of **Artificial Intelligence & Machine Learning projects**.  
This repo serves as a central hub linking to all my AI/ML project repositories.

---

"""

# Add each section
for section, rows in projects_by_category.items():
    readme += f"{section}\n\n"
    readme += "| 📁 Project Name | 🕰️ Last Updated | 📌 Status | 🔗 Repo Link |\n"
    readme += "|-----------------|-----------------|-----------|--------------|\n"
    readme += "\n".join(rows) if rows else "| _No projects detected yet_ | — | — | — |"
    readme += "\n\n---\n\n"

# Final footer
readme += """## 📬 Connect

- GitHub: [@YuvrajTayal1202](https://github.com/YuvrajTayal1202)  
- LinkedIn: [Yuvraj Tayal](https://www.linkedin.com/in/yuvraj-tayal-7a3a48356)  
- Twitter: [@YuvrajTayal](https://x.com/YuvrajTayal)  

---
⭐ If you find these projects helpful, don’t forget to **star the repo**!
"""

# Write README.md
with open("README.md", "w", encoding="utf-8") as f:
    f.write(textwrap.dedent(readme).strip() + "\n")

print("✅ README.md generated using topics!")
