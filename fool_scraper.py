from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://www.fool.com/investing/", wait_until="domcontentloaded")

    articles = page.locator("a:has(h5)").all()

    seen_urls = set()
    results = []

    for a in articles:
        href = a.get_attribute("href")
        url = "https://www.fool.com" + href

        if url in seen_urls:
            continue
        seen_urls.add(url)

        title = a.locator("h5").inner_text()
        results.append({"url": url, "title": title})

    print(len(results))
    for r in results:
        print(r["url"])
        print(r["title"])
        print()

    browser.close()
