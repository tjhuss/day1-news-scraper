# News Scraper Pipeline

A small end-to-end pipeline that scrapes financial news headlines from three
sites, cleans the data, and loads it into a SQLite database.

## Setup

```
pip install -r requirements.txt
playwright install chromium
```

## Usage

Run each script in order from the project folder:

```
python3 day1_news_scraper.py     # scrapes fool.com, marketscreener.com, and
                                  # tradingview.com; classifies each headline
                                  # into a category; writes news_dataset.csv

python3 day2_data_cleaning.py    # checks for missing values/duplicates,
                                  # normalizes text, converts Category to a
                                  # proper dtype; writes news_dataset_cleaned.csv

python3 day3_database.py         # loads the cleaned dataset into a SQLite
                                  # database (news_dataset_cleaned.db)
```

## Output files

| File | Description |
| --- | --- |
| `news_dataset.csv` | Raw scraped data: URL, Title, Category |
| `news_dataset_cleaned.csv` | Cleaned version of the above |
| `news_dataset_cleaned.db` | SQLite database with an `articles` table (`url` as primary key) |

## Categories

Each headline is classified into one of: Technology, Markets, Business,
Politics, Health, Energy.
