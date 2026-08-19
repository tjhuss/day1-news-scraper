import csv
from playwright.sync_api import sync_playwright

CATEGORY_KEYWORDS = {
    "Health": ["fda", "drug", "vaccine", "hospital", "medical", "disease", "patient", "biotech", "cancer", "clinical trial", "health"],
    "Energy": ["oil", " gas", "solar", "renewable", "nuclear", "power grid", "lng", "drilling", "energy", "opec", "barrel"],
    "Technology": ["ai ", " ai,", "artificial intelligence", "chip", "semiconductor", "software", " app", "cyber", "robot", "quantum", "tech", "iphone", "cloud", "data center", "ipad", "macbook"],
    "Politics": ["senate", "congress", "election", "president", "minister", "tariff", "sanctions", " war", "government", "regulation", "ceasefire", "gaza", "ukraine", "fcc"],
    "Markets": ["stock", "shares", "nasdaq", "dow jones", "s&p", "ipo", "etf", "dividend", "futures", "yields", "bond", "gold", "currency", "forex", "crypto", "bitcoin", "index", "rally", "selloff", "rate cut", "fed "],
}


def classify_category(title):
    lowered = title.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in lowered for keyword in keywords):
            return category
    return "Business"

#scraper for fool.com
def scrape_fool(page):
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
    return results


def scrape_marketscreener(context):
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
    page.close()
    return results

#scraper for tradingview.com
def scrape_tradingview(page):
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
    return results


all_rows = []

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    print("Scraping fool.com...")
    all_rows.extend(scrape_fool(page))

    print("Scraping tradingview.com...")
    all_rows.extend(scrape_tradingview(page))

    browser.close()

    # marketscreener.com needs a real user-agent to bypass bot detection
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        viewport={"width": 1280, "height": 800},
    )
    print("Scraping marketscreener.com...")
    all_rows.extend(scrape_marketscreener(context))

    browser.close()

with open("news_dataset.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["URL", "Title", "Category"])
    writer.writeheader()
    for row in all_rows:
        writer.writerow({
            "URL": row["url"],
            "Title": row["title"],
            "Category": classify_category(row["title"]),
        })

print(f"Saved {len(all_rows)} rows to news_dataset.csv")
