import sqlite3
import pandas as pd

df = pd.read_csv("news_dataset_cleaned.csv")

conn = sqlite3.connect("news_dataset_cleaned.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS articles (
    url TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT NOT NULL
)
""")

rows = list(df[["URL", "Title", "Category"]].itertuples(index=False, name=None))
cursor.executemany("""
INSERT OR IGNORE INTO articles (url, title, category)
VALUES (?, ?, ?)
""", rows)

conn.commit()

cursor.execute("SELECT COUNT(*) FROM articles")
print("Total rows in database:", cursor.fetchone()[0])

cursor.execute("SELECT category, COUNT(*) FROM articles GROUP BY category ORDER BY COUNT(*) DESC")
print("\nCategory breakdown:")
for category, count in cursor.fetchall():
    print(f"{category}: {count}")
cursor.execute("SELECT * FROM articles LIMIT 3")
print("\nSample rows:")
for row in cursor.fetchall():
    print(row)

conn.close()