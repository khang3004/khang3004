import os
import re
import json
import urllib.request
from urllib.error import URLError

# GitHub API setup
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Accept": "application/vnd.github.v3+json",
}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"

USERNAME = "khang3004"

# Configuration for the featured projects
PROJECTS = [
    {
        "repo": "forked_mini_dev_hcmus_underdogs",
        "name": "AgentSQL",
        "theme": "tokyonight",
    },
    {
        "repo": "DataAnalysis_Agent",
        "name": "DataAnalysis Agent",
        "theme": "radical",
    },
    {
        "repo": "artist-revenue-management-project",
        "name": "Artist Revenue Mgmt",
        "theme": "merko",
    },
    {
        "repo": "FINANCIAL-SENTIMENT-ANALYSIS-onVietnamese-Stock-Market-Headlines",
        "name": "Financial Sentiment NLP",
        "theme": "gruvbox",
    },
    {
        "repo": "Comprehensive-ML-DL-Approaches-for-Hotel-Room-Review-Score-Prediction",
        "name": "Hotel Review Score ML",
        "theme": "onedark",
    },
    {
        "repo": "GMM_4_missing_data",
        "name": "GMM for Missing Data",
        "theme": "cobalt",
    }
]

# Language color mappings for Shields.io
LANG_COLORS = {
    "Python": "3776AB",
    "Swift": "F05138",
    "Jupyter Notebook": "DA5B0B",
    "HTML": "E34F26",
    "CSS": "1572B6",
    "JavaScript": "F7DF1E",
    "TypeScript": "3178C6",
    "Java": "007396",
    "C++": "00599C",
    "C": "A8B9CC",
    "C#": "239120",
    "Ruby": "CC342D",
    "Go": "00ADD8",
    "Rust": "000000",
    "PHP": "777BB4",
    "Shell": "89E051",
    "Unknown": "000000",
}


def fetch_repo_data(repo_name):
    url = f"https://api.github.com/repos/{USERNAME}/{repo_name}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                return json.loads(response.read().decode("utf-8"))
    except URLError as e:
        print(f"Error fetching {repo_name}: {e}")
    return None


def generate_html_table(projects_data):
    html = ""
    for i in range(0, len(projects_data), 2):
        html += '<p align="center">\n'
        for j in range(2):
            if i + j < len(projects_data):
                p = projects_data[i + j]
                repo = p["repo"]
                theme = p["theme"]
                # Removing show_owner=true to only show the repo name
                # Adding description_lines_count to ensure the project description is visible
                html += f'''  <a href="https://github.com/{USERNAME}/{repo}">
    <img src="https://github-readme-stats.anuraghazra1.vercel.app/api/pin/?username={USERNAME}&repo={repo}&theme={theme}&description_lines_count=2&hide_border=true&bg_color=0D1117" width="48%" />
  </a>\n'''
        html += "</p>\n\n"
    return html


def update_readme(html_content):
    readme_path = "README.md"
    with open(readme_path, "r", encoding="utf-8") as f:
        readme = f.read()

    # Find the injection markers
    start_marker = "<!-- PROJECTS_START -->\n"
    end_marker = "<!-- PROJECTS_END -->\n"

    pattern = re.compile(f"{start_marker}.*?{end_marker}", re.DOTALL)

    if not pattern.search(readme):
        print(
            f"Error: Could not find markers {start_marker.strip()} and {end_marker.strip()} in README.md"
        )
        return

    new_content = f"{start_marker}{html_content}{end_marker}"
    updated_readme = pattern.sub(new_content, readme)

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(updated_readme)

    print("README.md has been successfully updated!")


def main():
    print("Fetching repository data...")
    projects_data = []

    for p in PROJECTS:
        data = fetch_repo_data(p["repo"])
        if data:
            lang = p.get("override_lang") or data.get("language") or "Unknown"
            # Normalize Jupyter Notebook to Python if no override
            if lang == "Jupyter Notebook" and not p.get("override_lang"):
                lang = "Python"

            desc = p.get("override_desc") or data.get("description") or ""

            projects_data.append(
                {
                    "repo": p["repo"],
                    "theme": p["theme"],
                    "desc": desc,
                    "lang": lang,
                    "stars": data.get("stargazers_count", 0),
                    "forks": data.get("forks_count", 0),
                }
            )
        else:
            print(f"Failed to load data for {p['repo']}, using default fallback.")
            projects_data.append(
                {
                    "repo": p["repo"],
                    "theme": p["theme"],
                    "desc": p.get("override_desc", ""),
                    "lang": p.get("override_lang", "Python"),
                    "stars": 0,
                    "forks": 0,
                }
            )

    print("Generating HTML table...")
    html_content = generate_html_table(projects_data)

    print("Updating README.md...")
    update_readme(html_content)


if __name__ == "__main__":
    main()
