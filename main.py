# Made by Yrashka 
# Pls give me a star on github if you like it :D 
# GitHub repo: https://github.com/Yrashka200/Readme-Generator 

import os
from datetime import datetime
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()
TEMPLATE_DIR = "templates"

# template functions 

def load_templates():
    if not os.path.exists(TEMPLATE_DIR):
        os.makedirs(TEMPLATE_DIR)
    return [f for f in os.listdir(TEMPLATE_DIR) if f.endswith(".md")]


def load_template(template_name):
    path = os.path.join(TEMPLATE_DIR, template_name)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def render_template(template, context):
    for key, value in context.items():
        template = template.replace(f"{{{{{key}}}}}", value)
    return template


#requirements functions 

def read_requirements():
    if not os.path.exists(""):
        return []

    with open("requirements.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    packages = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            packages.append(line.split("==")[0])

    return packages


#badge and stats functions

def generate_badges(username, repo, tech_stack):
    badges = []

    if username and repo:
        badges.append(
            f"![Stars](https://img.shields.io/github/stars/{username}/{repo}?style=social)"
        )
        badges.append(
            f"![Forks](https://img.shields.io/github/forks/{username}/{repo}?style=social)"
        )
        badges.append(
            f"![Issues](https://img.shields.io/github/issues/{username}/{repo})"
        )
        badges.append(
            f"![License](https://img.shields.io/github/license/{username}/{repo})"
        )

    for tech in tech_stack:
        badges.append(
            f"![{tech}](https://img.shields.io/badge/{tech}-blue?style=flat-square)"
        )

    return "\n".join(badges)


def generate_stats(username, theme):
    if not username:
        return ""

    return f"""
## 📊 GitHub Stats

![Stats](https://github-readme-stats.vercel.app/api?username={username}&show_icons=true&theme={theme})
![Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username={username}&layout=compact&theme={theme})
"""


def generate_license(choice):
    year = datetime.now().year

    licenses = {
        "MIT": f"MIT License © {year}",
        "Apache 2.0": "Licensed under Apache License 2.0",
        "GPL v3": "Licensed under GNU GPL v3",
        "None": ""
    }

    if choice == "None":
        return ""

    return f"\n## 📜 License\n\n{licenses[choice]}\n"


#default readme generator

def generate_default_readme(context):
    return f"""
# {context['title']}

{context['badges']}

## 📖 Description
{context['description']}

## ✨ Features
{context['features']}

## 🛠 Tech Stack
{context['tech_stack']}

## ⚙️ Installation
```bash
{context['installation']}
🚀 Usage
{context['usage']}
👤 Author

{context['author']}

{context['stats']}
{context['license']}
"""


def main():
    console.print(Panel(" README Generator\n by Yrashka ", style="bold cyan", box=box.DOUBLE))

use_template = Prompt.ask(
    "Use custom template?",
    choices=["yes", "no"],
    default="no"
)

template_content = None
if use_template == "yes":
    templates = load_templates()

    if not templates:
        console.print("[red]No templates found in /templates folder[/red]")
       

    template_choice = Prompt.ask("Choose template", choices=templates)
    template_content = load_template(template_choice)

title = Prompt.ask("Project title")
description = Prompt.ask("Short description")
username = Prompt.ask("GitHub username", default="")
repo = Prompt.ask("Repository name", default="")
author = Prompt.ask("Author name")


console.print("\n[bold yellow]Analyzing requirements.txt...[/bold yellow]")
tech_stack = read_requirements()

if tech_stack:
    table = Table(title="Detected Dependencies", box=box.ROUNDED)
    table.add_column("Package", style="cyan")
    for pkg in tech_stack:
        table.add_row(pkg)
    console.print(table)
else:
    console.print("[red]No requirements.txt found[/red]")

features = []
console.print("\nEnter features (type 'done'):")
while True:
    feature = Prompt.ask(">")
    if feature.lower() == "done":
        break
    if feature.strip():
        features.append(feature)

installation = Prompt.ask(
    "Installation command",
    default="pip install -r requirements.txt"
)
usage = Prompt.ask(
    "Usage command",
    default="python main.py"
)

theme = Prompt.ask(
    "GitHub Stats theme",
    choices=["tokyonight", "dark", "radical", "gruvbox", "onedark", "dracula"],
    default="tokyonight"
)

license_choice = Prompt.ask(
    "License",
    choices=["MIT", "Apache 2.0", "GPL v3", "None"],
    default="MIT"
)

features_text = "\n".join([f"- {f}" for f in features])
tech_text = "\n".join([f"- {t}" for t in tech_stack])

badges = generate_badges(username, repo, tech_stack)
stats = generate_stats(username, theme)
license_section = generate_license(license_choice)

context = {
    "title": title,
    "description": description,
    "features": features_text,
    "tech_stack": tech_text,
    "installation": installation,
    "usage": usage,
    "author": author,
    "stats": stats,
    "license": license_section,
    "badges": badges,
    "year": str(datetime.now().year)
}

if template_content:
    final_readme = render_template(template_content, context)
else:
    final_readme = generate_default_readme(context)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(final_readme)

console.print("\n[bold green]✅ README.md successfully generated![/bold green]")


if __name__ == "__main__":
    main()