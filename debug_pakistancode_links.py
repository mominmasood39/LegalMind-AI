from playwright.sync_api import sync_playwright

URL = "https://pakistancode.gov.pk/english/LGu0xBD.php"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(5000)

    # Save HTML
    html = page.content()
    with open("page_dump.html", "w", encoding="utf-8") as f:
        f.write(html)

    # Print first 50 links
    links = page.eval_on_selector_all("a", "els => els.map(a => a.href)")
    print("Total links:", len(links))
    for i, l in enumerate(links[:50], start=1):
        print(i, l)

    browser.close()