# News Scraper Pipeline

A small end-to-end pipeline that scrapes financial news headlines from three
sites, cleans the data, and loads it into a SQLite database.

## Setup

```
pip install -r requirements.txt
playwright install chromium
```

## Usage

Each day's work lives in its own folder. Run them in order, `cd`-ing into
each folder first (every script reads its input from the previous day's
folder using a relative path):

```
cd day1
python3 day1_news_scraper.py     # scrapes fool.com, marketscreener.com, and
                                  # tradingview.com; classifies each headline
                                  # into a category; writes news_dataset.csv

cd ../day2
python3 day2_data_cleaning.py    # checks for missing values/duplicates,
                                  # normalizes text, converts Category to a
                                  # proper dtype; writes news_dataset_cleaned.csv

cd ../day3
python3 day3_database.py         # loads the cleaned dataset into a SQLite
                                  # database (news_dataset_cleaned.db)
```

## Project structure

| Folder | Contents |
| --- | --- |
| `day1/` | `day1_news_scraper.py` and its output, `news_dataset.csv` (raw scraped data: URL, Title, Category) |
| `day2/` | `day2_data_cleaning.py` and its output, `news_dataset_cleaned.csv` |
| `day3/` | `day3_database.py` and its output, `news_dataset_cleaned.db` (SQLite database with an `articles` table, `url` as primary key) |

## Categories

Each headline is classified into one of: Technology, Markets, Business,
Politics, Health, Energy.
