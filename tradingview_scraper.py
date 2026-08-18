from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://www.tradingview.com/news/", wait_until="domcontentloaded")

    articles = page.locator("a:has([data-qa-id='news-headline-title'])").all()

    seen_urls = set()
    results = []

    for a in articles:
        href = a.get_attribute("href")
        url = "https://www.tradingview.com" + href

        if url in seen_urls:
            continue
        seen_urls.add(url)

        title = a.locator("[data-qa-id='news-headline-title']").inner_text()
        results.append({"url": url, "title": title})

    print(len(results))
    for r in results:
        print(r["url"])
        print(r["title"])
        print()

    browser.close()
