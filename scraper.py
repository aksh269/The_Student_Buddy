import os
import time
import requests
import pandas as pd

from bs4 import BeautifulSoup
from urllib.parse import urljoin

# ==========================================
# CONFIG
# ==========================================

BASE_URL = "https://intranet.daiict.ac.in/~daiict_nt01/"

ROOT_FOLDERS = [
    "Academic/",
    "Announcement/",
    "coe/"      # change to COE/ if needed
]

SAVE_DIR = "daiict_documents"

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".doc",
    ".docx",
    ".ppt",
    ".pptx",
    ".xls",
    ".xlsx"
}

REQUEST_DELAY = 1

# ==========================================
# GLOBALS
# ==========================================

session = requests.Session()

visited = set()

files_found = []

# ==========================================
# CRAWLER
# ==========================================

def crawl(url, root_url):

    if url in visited:
        return

    if not url.startswith(root_url):
        return

    visited.add(url)

    print(f"Scanning: {url}")

    try:

        r = session.get(url, timeout=30)

        soup = BeautifulSoup(
            r.text,
            "html.parser"
        )

        for link in soup.find_all("a"):

            href = link.get("href")

            if not href:
                continue

            if href == "../":
                continue

            next_url = urljoin(
                url,
                href
            )

            if not next_url.startswith(root_url):
                continue

            # FOLDER
            if href.endswith("/"):

                crawl(
                    next_url,
                    root_url
                )

                continue

            ext = os.path.splitext(
                href
            )[1].lower()

            if ext not in ALLOWED_EXTENSIONS:
                continue

            files_found.append(
                {
                    "file_name": href,
                    "file_url": next_url,
                    "folder": url
                }
            )

        time.sleep(
            REQUEST_DELAY
        )

    except Exception as e:

        print(
            f"ERROR: {url}"
        )

        print(e)

# ==========================================
# DOWNLOAD
# ==========================================

def download_file(url):

    relative = url.split(
        "~daiict_nt01/"
    )[-1]

    local_path = os.path.join(
        SAVE_DIR,
        relative
    )

    os.makedirs(
        os.path.dirname(local_path),
        exist_ok=True
    )

    if os.path.exists(
        local_path
    ):
        return

    try:

        r = session.get(
            url,
            stream=True,
            timeout=60
        )

        with open(
            local_path,
            "wb"
        ) as f:

            for chunk in r.iter_content(
                8192
            ):

                if chunk:
                    f.write(chunk)

        print(
            f"Downloaded: {local_path}"
        )

    except Exception as e:

        print(
            f"Failed: {url}"
        )

        print(e)

# ==========================================
# MAIN
# ==========================================

print("\nStarting crawl...\n")

for folder in ROOT_FOLDERS:

    root_url = urljoin(
        BASE_URL,
        folder
    )

    crawl(
        root_url,
        root_url
    )

df = pd.DataFrame(
    files_found
)

print(
    "\nTotal files found:",
    len(df)
)

df.to_csv(
    "inventory.csv",
    index=False
)

print(
    "\nInventory saved as inventory.csv"
)

print(
    "\nFirst 20 files:"
)

print(
    df.head(20)
)

choice = input(
    "\nDownload files? (y/n): "
)

if choice.lower() == "y":

    for _, row in df.iterrows():

        download_file(
            row["file_url"]
        )

print("\nDone.")