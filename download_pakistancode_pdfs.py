import os
import re
import time
import requests
from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright

START_URL = "https://pakistancode.gov.pk/english/LGu0xBD.php"
OUTPUT_DIR = "documents"
BASE_DOMAIN = "pakistancode.gov.pk"

def sanitize_filename(url):
    name = os.path.basename(urlparse(url).path)
    name = re.sub(r"[^a-zA-Z0-9._-]", "_", name)
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
            .map(a => ({ href: a.href || '', text: (a.textContent || '').trim() }))
            .filter(x => x.href);
    }""")

def is_year_link(href):
    href = href.lower()
    return ("lgu0xbd" in href) and ("year=" in href)

def is_detail_link(href):
    href = href.lower()
    if "year=" in href:
        return False
    if BASE_DOMAIN not in href:
        return False
    # Heuristics for law detail pages
    keys = ["actid=", "law_id=", "doc_id=", "id=", "sid=", "view", "detail"]
    return any(k in href for k in keys)

def extract_pdf_links(page, base_url):
    pdfs = set()

    links = extract_links(page)
    for l in links:
        href = l["href"]
        text = l["text"].lower()
        if href.lower().endswith(".pdf") or "pdf" in text or "download" in text:
            pdfs.add(urljoin(base_url, href))

    html = page.content()
    for match in re.findall(r'https?://[^"\']+\.pdf', html):
        pdfs.add(match)

    return pdfs

def main():
    pdf_links = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(START_URL, wait_until="networkidle")
        page.wait_for_timeout(4000)

        # Collect year pages
        year_links = extract_links(page)
        year_urls = []
        for a in year_links:
            href = a["href"]
            if is_year_link(href):
                year_urls.append(href)
        year_urls = list(dict.fromkeys(year_urls))

        print(f"Found {len(year_urls)} year pages")

        # Visit each year page and collect law detail pages
        detail_urls = set()
        for i, url in enumerate(year_urls, start=1):
            print(f"[{i}/{len(year_urls)}] Visiting year: {url}")
            page.goto(url, wait_until="networkidle")
            page.wait_for_timeout(2000)

            links = extract_links(page)
            for l in links:
                href = l["href"]
                if is_detail_link(href):
                    detail_urls.add(href)

        detail_urls = sorted(detail_urls)
        print(f"Found {len(detail_urls)} law detail pages")

        # Visit each law detail page and extract PDF links
        for i, url in enumerate(detail_urls, start=1):
            print(f"[{i}/{len(detail_urls)}] Visiting law page: {url}")
            page.goto(url, wait_until="networkidle")
            page.wait_for_timeout(1500)

            found = extract_pdf_links(page, url)
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
            time.sleep(0.3)
        except Exception as e:
            print(f"[{i}/{len(pdf_links)}] Failed: {url} -> {e}")

    print(f"\nDone. Downloaded {downloaded} files into '{OUTPUT_DIR}'")

if __name__ == "__main__":
    main()