import os
import re
import time
import requests
from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

START_URL = "https://pakistancode.gov.pk/english/LGu0xAD.php"
OUTPUT_DIR = "documents"

PDF_REGEX = r"https?://pakistancode\.gov\.pk/pdffiles/[^\"']+\.pdf"

def sanitize_filename(url):
    name = os.path.basename(urlparse(url).path)
    return name or "download.pdf"

def download_file(url, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    filename = sanitize_filename(url)
    path = os.path.join(out_dir, filename)
    if os.path.exists(path):
        return False
    r = requests.get(url, stream=True, timeout=60)
    r.raise_for_status()
    with open(path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    return True

def extract_links(page):
    return page.evaluate("""() => {
        return Array.from(document.querySelectorAll('a'))
            .map(a => a.href)
            .filter(Boolean);
    }""")

def find_pdf_in_html(html):
    return set(re.findall(PDF_REGEX, html))

def is_valid_detail_link(href):
    if not href.startswith("https://pakistancode.gov.pk/english/"):
        return False
    if "LGu0xAD.php" in href:
        return False
    # Filter out obfuscated slugs that cause timeouts
    if "UY2F" in href:
        return False
    # Must include php or query params (real detail pages usually do)
    return (".php" in href) or ("?" in href)

def main():
    pdf_links = set()
    detail_pages = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(START_URL, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(2000)

        # Collect A-Z links
        alpha_links = [l for l in extract_links(page) if "LGu0xAD" in l]
        alpha_links = list(dict.fromkeys(alpha_links)) or [START_URL]

        # Visit each alphabet page and collect law detail links
        for i, url in enumerate(alpha_links, start=1):
            print(f"[{i}/{len(alpha_links)}] Visiting alpha: {url}")
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=60000)
                page.wait_for_timeout(1500)
            except PlaywrightTimeout:
                print(f"  ⚠️ Timeout alpha: {url}")
                continue

            links = extract_links(page)
            for l in links:
                if is_valid_detail_link(l):
                    detail_pages.add(l)

        detail_pages = sorted(detail_pages)
        print(f"Found {len(detail_pages)} law detail pages")

        # Visit each law page and extract PDF links
        for i, url in enumerate(detail_pages, start=1):
            print(f"[{i}/{len(detail_pages)}] Visiting law: {url}")
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=60000)
                page.wait_for_timeout(1000)
            except PlaywrightTimeout:
                print(f"  ⚠️ Timeout law: {url}")
                continue

            html = page.content()
            found = find_pdf_in_html(html)
            if found:
                pdf_links.update(found)

        browser.close()

    print(f"Found {len(pdf_links)} PDFs")

    downloaded = 0
    for i, url in enumerate(sorted(pdf_links), start=1):
        try:
            ok = download_file(url, OUTPUT_DIR)
            if ok:
                downloaded += 1
                print(f"[{i}/{len(pdf_links)}] Downloaded: {url}")
            else:
                print(f"[{i}/{len(pdf_links)}] Skipped (exists): {url}")
            time.sleep(0.2)
        except Exception as e:
            print(f"[{i}/{len(pdf_links)}] Failed: {url} -> {e}")

    print(f"\nDone. Downloaded {downloaded} files into '{OUTPUT_DIR}'")

if __name__ == "__main__":
    main()