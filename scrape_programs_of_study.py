import os
import re
import time
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md


BASE_URL = "https://www.daiict.ac.in"
START_URL = "https://www.daiict.ac.in/index.php/programs-of-study"
OUTPUT_DIR = "output"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


PROGRAM_SECTIONS = {
    "Undergraduate Programs": {
        "folder": "undergraduate_programs",
        "overview_filename": "undergraduate_programs.md",
        "overview_url": "https://www.daiict.ac.in/index.php/programs-of-study#tab-1",
        "tab_id": "tab-1",
        "programs": [
            ("B.Tech. (ICT)", "https://www.daiict.ac.in/btech-ict"),
            ("B.Tech. (Honours) in ICT with minor in Computational Science", "https://www.daiict.ac.in/btech-honours-ict-minor-computational-science"),
            ("B.Tech. (MnC)", "https://www.daiict.ac.in/btech-mnc"),
            ("B.Tech. (EVD)", "https://www.daiict.ac.in/btech-evd"),
            ("B.Tech. (CS and AI)", "https://www.daiict.ac.in/btech-csai"),
            ("B.Tech. (ECE-AI)", "https://www.daiict.ac.in/btech-ece-ai"),
        ],
    },
    "Postgraduate Programs": {
        "folder": "postgraduate_programs",
        "overview_filename": "postgraduate_programs.md",
        "overview_url": "https://www.daiict.ac.in/index.php/programs-of-study#tab-2",
        "tab_id": "tab-2",
        "programs": [
            ("M.Tech. (ICT)", "https://www.daiict.ac.in/mtech-ict"),
            ("M.Sc. (IT)", "https://www.daiict.ac.in/msc-it"),
            ("M.Sc. (Agriculture Analytics)", "https://www.daiict.ac.in/msc-agriculture-analytics"),
            ("M.Sc. (Data Science)", "https://www.daiict.ac.in/msc-data-science"),
            ("M.Des. (Communication Design)", "https://www.daiict.ac.in/mdes-communication-design"),
            ("M.Des. (Intelligent User Experience Design)", "https://www.daiict.ac.in/mdes-intelligent-user-experience-design"),
        ],
    },
    "Dual Degree Programs": {
        "folder": "dual_degree_programs",
        "overview_filename": "dual_degree_programs.md",
        "overview_url": "https://www.daiict.ac.in/index.php/programs-of-study#tab-4",
        "tab_id": "tab-4",
        "programs": [
            ("BS-MS in Information Technology", "https://www.daiict.ac.in/bs-ms-information-technology"),
            ("BS-MS in Data Science & Artificial Intelligence", "https://www.daiict.ac.in/bs-ms-data-science-artificial-intelligence"),
        ],
    },
    "Doctoral Program": {
        "folder": "doctoral_program",
        "overview_filename": "doctoral_program.md",
        "overview_url": "https://www.daiict.ac.in/index.php/programs-of-study#tab-3",
        "tab_id": "tab-3",
        "programs": [
            ("Ph.D.", "https://www.daiict.ac.in/phd"),
        ],
    },
}

def fetch_html(url):
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    return response.text


def slugify(text):
    text = text.lower().strip()
    text = text.replace("&", "and")
    text = text.replace("+", "plus")
    text = re.sub(r"[()]", "", text)
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text)
    return text.strip("_") or "page"


def clean_markdown(text):
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def make_absolute_links(soup, page_url):
    for a in soup.find_all("a", href=True):
        a["href"] = urljoin(page_url, a["href"])
    return soup


def remove_unwanted(soup):
    for tag in soup.find_all([
        "script", "style", "noscript", "iframe", "svg",
        "form", "button", "input", "img", "picture", "source"
    ]):
        tag.decompose()
    return soup


def get_main_content(soup):
    selectors = [
        "main",
        "article",
        ".region-content",
        ".main-content",
        ".content",
        "#content",
        ".node__content",
    ]

    for selector in selectors:
        found = soup.select_one(selector)
        if found and len(found.get_text(" ", strip=True)) > 300:
            return found

    return soup.body or soup


def extract_title(soup, fallback):
    h1 = soup.find("h1")
    if h1 and h1.get_text(strip=True):
        return h1.get_text(" ", strip=True)

    title = soup.find("title")
    if title and title.get_text(strip=True):
        return title.get_text(" ", strip=True)

    return fallback


def extract_downloadable_resources(soup, page_url):
    resources = []
    extensions = {
        ".pdf": "PDF",
        ".doc": "DOC",
        ".docx": "DOC",
        ".xls": "Excel",
        ".xlsx": "Excel",
    }

    for a in soup.find_all("a", href=True):
        href = urljoin(page_url, a["href"])
        path = urlparse(href).path.lower()
        text = a.get_text(" ", strip=True) or os.path.basename(path)

        for ext, resource_type in extensions.items():
            if path.endswith(ext):
                resources.append((text, href, resource_type))

    seen = set()
    unique = []

    for item in resources:
        if item[1] not in seen:
            unique.append(item)
            seen.add(item[1])

    return unique


def extract_related_links(soup, page_url):
    links = []

    for a in soup.find_all("a", href=True):
        href = urljoin(page_url, a["href"])
        text = a.get_text(" ", strip=True)

        if not text:
            continue

        if href.startswith("mailto:") or href.startswith("tel:"):
            continue

        if urlparse(href).path.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp")):
            continue

        links.append((text, href))

    seen = set()
    unique = []

    for text, href in links:
        key = (text, href)
        if key not in seen:
            unique.append((text, href))
            seen.add(key)

    return unique


def convert_html_to_md(html_or_tag, page_url):
    soup = BeautifulSoup(str(html_or_tag), "lxml")
    soup = make_absolute_links(soup, page_url)
    soup = remove_unwanted(soup)

    markdown = md(
        str(soup),
        heading_style="ATX",
        bullets="-",
        strip=["img"],
    )

    return clean_markdown(markdown)


def build_md(title, url, subcategory, page_type, main_content, related_links, resources):
    safe_title = title.replace('"', "'")

    output = f"""---
title: "{safe_title}"
url: "{url}"
category: "Programs_of_Study"
subcategory: "{subcategory}"
page_type: "{page_type}"
---

# Overview

"""

    overview = []
    for line in main_content.splitlines():
        line = line.strip()
        if line and not line.startswith("#") and not line.startswith("-"):
            overview.append(line)
        if len(" ".join(overview)) > 350:
            break

    if overview:
        output += " ".join(overview) + "\n\n"
    else:
        output += "Information related to this page is provided below.\n\n"

    output += "# Main Content\n\n"
    output += main_content + "\n\n"

    if related_links:
        output += "# Related Links\n\n"
        for text, href in related_links:
            output += f"- [{text}]({href})\n"
        output += "\n"

    output += "# Downloadable Resources\n\n"

    if resources:
        output += "| Resource | Type |\n"
        output += "| --- | --- |\n"
        for text, href, resource_type in resources:
            output += f"| [{text}]({href}) | {resource_type} |\n"
    else:
        output += "No downloadable resources found.\n"

    return clean_markdown(output) + "\n"


def save_file(folder, filename, content):
    os.makedirs(folder, exist_ok=True)

    if not filename.endswith(".md"):
        filename += ".md"

    path = os.path.join(folder, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Saved: {path}")


def scrape_page_to_md(url, folder, filename, subcategory, page_type):
    html = fetch_html(url)
    soup = BeautifulSoup(html, "lxml")
    soup = make_absolute_links(soup, url)
    soup = remove_unwanted(soup)

    title = extract_title(soup, fallback=filename.replace("_", " ").title())
    main = get_main_content(soup)

    main_content = convert_html_to_md(main, url)
    related_links = extract_related_links(main, url)
    resources = extract_downloadable_resources(main, url)

    final_md = build_md(
        title=title,
        url=url,
        subcategory=subcategory,
        page_type=page_type,
        main_content=main_content,
        related_links=related_links,
        resources=resources,
    )

    save_file(folder, filename, final_md)


def extract_programs_page_text():
    html = fetch_html(START_URL)
    soup = BeautifulSoup(html, "lxml")
    soup = make_absolute_links(soup, START_URL)
    soup = remove_unwanted(soup)

    main = get_main_content(soup)
    text = main.get_text("\n", strip=True)

    return text


def make_overview_content(section_name, programs):
    lines = []
    lines.append(f"# {section_name}")
    lines.append("")
    lines.append("This section contains programs listed under the Programs of Study page.")
    lines.append("")
    lines.append("# Programs")
    lines.append("")

    for program_name, program_url in programs:
        lines.append(f"- [{program_name}]({program_url})")

    return "\n".join(lines)


def create_section_overview(section_name, config):
    folder = os.path.join(OUTPUT_DIR, config["folder"])
    filename = config["overview_filename"]

    html = fetch_html(START_URL)
    soup = BeautifulSoup(html, "lxml")
    soup = make_absolute_links(soup, START_URL)
    soup = remove_unwanted(soup)

    tab_id = config["tab_id"]
    section = soup.select_one(f"#{tab_id}")

    if not section:
        print(f"Could not find tab content: #{tab_id}")
        print("Using fallback overview content.")
        main_content = make_overview_content(section_name, config["programs"])
        related_links = config["programs"]
        resources = []
    else:
        main_content = convert_html_to_md(section, START_URL)
        related_links = extract_related_links(section, START_URL)
        resources = extract_downloadable_resources(section, START_URL)

        # Add program links manually if the website tab does not expose them cleanly
        for program_name, program_url in config["programs"]:
            if program_url not in main_content:
                main_content += f"\n- [{program_name}]({program_url})"

    final_md = build_md(
        title=f"Programs of Study / {section_name}",
        url=config["overview_url"],
        subcategory=section_name,
        page_type="Section Overview",
        main_content=main_content,
        related_links=related_links,
        resources=resources,
    )

    save_file(folder, filename, final_md)


def main():
    print("Starting DA-IICT Programs scraper...")

    for section_name, config in PROGRAM_SECTIONS.items():
        print(f"\nProcessing section: {section_name}")

        folder = os.path.join(OUTPUT_DIR, config["folder"])

        create_section_overview(section_name, config)

        for program_name, program_url in config["programs"]:
            filename = slugify(program_name)

            print(f"Scraping: {program_name}")

            try:
                scrape_page_to_md(
                    url=program_url,
                    folder=folder,
                    filename=filename,
                    subcategory=section_name,
                    page_type="Program Page",
                )
                time.sleep(1)
            except Exception as e:
                print(f"Failed: {program_name}")
                print(f"URL: {program_url}")
                print(f"Reason: {e}")

    print("\nScraping completed.")


if __name__ == "__main__":
    main()