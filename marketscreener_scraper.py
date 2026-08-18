from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        viewport={"width": 1280, "height": 800},
    )
    page = context.new_page()
    page.goto("https://www.marketscreener.com/news/", wait_until="domcontentloaded")

    articles = page.locator("a:has(b)").all()

    seen_urls = set()
    results = []

    for a in articles:
        href = a.get_attribute("href")
        url = "https://www.marketscreener.com" + href

        if url in seen_urls:
            continue
        seen_urls.add(url)

        title = a.locator("b").inner_text()
        results.append({"url": url, "title": title})

    print(len(results))
    for r in results:
        print(r["url"])
        print(r["title"])
        print()

    browser.close()
