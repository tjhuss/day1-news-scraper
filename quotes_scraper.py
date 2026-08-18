import csv
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://quotes.toscrape.com/js")

    all_quotes = []

    while True:
        quotes = page.locator(".quote").all()
        for quote in quotes:
            text = quote.locator(".text").inner_text()
            author = quote.locator(".author").inner_text()
            tags = quote.locator(".tag").all_inner_texts()
            all_quotes.append({"text": text, "author": author, "tags": tags})

        next_button = page.locator("a:has-text('Next')")
        if next_button.count() == 0:
            break

        next_button.click()
        page.wait_for_selector(".quote")

    browser.close()

with open("quotes.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["text", "author", "tags"])
    writer.writeheader()
    for quote in all_quotes:
        writer.writerow({
            "text": quote["text"],
            "author": quote["author"],
            "tags": ", ".join(quote["tags"]),
        })

print(f"Saved {len(all_quotes)} quotes to quotes.csv")
