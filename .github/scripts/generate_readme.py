
# .github/scripts/generate_readme.py
from datetime import datetime
from github import Github
import os, textwrap

user = os.environ["GH_USERNAME"]
client = Github(os.environ.get("GITHUB_TOKEN"))
me = client.get_user(user)

# Pull repos and filter by topic/name heuristics
ml_keywords = {"ml", "aiml", "ai", "deep", "dl", "cv", "nlp", "titanic", "churn", "disease", "recommender", "cnn"}
repos = []
for r in me.get_repos():
    topics = set(r.get_topics())
    name = r.name.lower()
    if topics.intersection(ml_keywords) or any(k in name for k in ml_keywords):
        repos.append(r)

# Sort by pushed_at desc
repos.sort(key=lambda r: r.pushed_at, reverse=True)

def row(name, tech, status, url):
    return f"| **{name}** | {tech} | {status} | [View Repo]({url}) |"

beginner, intermediate, advanced, end2end = [], [], [], []
for r in repos:
    n = r.name
    url = r.html_url
    # Quick heuristics
    nm = n.lower()
    if "agroscan" in nm:
        end2end.append(f"| 🌿 **{n}** | Coming Soon | {r.created_at.strftime('%b %Y')} | Full-stack (React, FastAPI, TF/Keras) | 🚧 In Progress | [View Repo]({url}) |")
    elif any(k in nm for k in ["titanic", "churn", "price", "diabetes", "breast", "loan", "heart", "spam", "retention"]):
        beginner.append(row(n, "Python, Scikit-Learn", "✅ Completed", url))
    elif any(k in nm for k in ["recommender", "movie", "book", "spaceship", "multiple"]):
        intermediate.append(row(n, "Python, Recommenders/EDA", "✅ Completed", url))
    elif any(k in nm for k in ["cnn", "transfer", "celebrity", "fraud"]):
        advanced.append(row(n, "TensorFlow/Keras / Advanced ML", "✅ Completed", url))

readme = f"""
# 🤖 AI/ML Projects Overview

Welcome to my curated collection of **Artificial Intelligence & Machine Learning projects**.

---

## 🟡 End-to-End Projects

| 📁 Project Name | 🔗 Live Demo | 🗓️ Date | 🛠️ Tech Stack | 📌 Status | 🔗 Repo Link |
|-----------------|--------------|---------|----------------|-----------|--------------|
{os.linesep.join(end2end) or '| _No E2E projects detected yet_ | — | — | — | — | — |'}

---

## 🟢 Beginner Projects

| 📁 Project Name | 🛠️ Tech Stack | 📌 Status | 🔗 Repo Link |
|-----------------|----------------|-----------|--------------|
{os.linesep.join(beginner) or '| _No beginner projects detected_ | — | — | — |'}

---

## 🟠 Intermediate Projects

| 📁 Project Name | 🛠️ Tech Stack | 📌 Status | 🔗 Repo Link |
|-----------------|----------------|-----------|--------------|
{os.linesep.join(intermediate) or '| _No intermediate projects detected_ | — | — | — |'}

---

## 🔴 Advanced / Deep Learning Projects

| 📁 Project Name | 🛠️ Tech Stack | 📌 Status | 🔗 Repo Link |
|-----------------|----------------|-----------|--------------|
{os.linesep.join(advanced) or '| _No advanced projects detected_ | — | — | — |'}

"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(textwrap.dedent(readme).strip() + "\n")