import pandas as pd

df = pd.read_csv("../day1/news_dataset.csv")

print("Loaded:", len(df), "rows")
print()

# --- Missing values check ---
print("Missing values:")
print(df.isnull().sum())
print()

# --- Duplicate check (exact URL/Title matches) ---
print("Duplicate URLs:", df["URL"].duplicated().sum())
print("Duplicate Titles:", df["Title"].duplicated().sum())
print()

# --- Text cleaning ---
# Strip stray leading/trailing whitespace defensively, and normalize
# "smart" typographic characters (curly quotes, en/em dashes) to their
# plain ASCII equivalents for consistency across the dataset.
def clean_text(text):
    text = text.strip()
    replacements = {
        "’": "'",   # right single quote
        "‘": "'",   # left single quote
        "“": '"',   # left double quote
        "”": '"',   # right double quote
        "–": "-",   # en dash
        "—": "-",   # em dash
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

df["Title"] = df["Title"].apply(clean_text)
df["URL"] = df["URL"].str.strip()

# --- Data type conversion ---
# Category is a fixed set of 6 values, so store it as a pandas
# "category" dtype instead of a plain string. This is more memory
# efficient and enforces that only known categories are allowed.
df["Category"] = df["Category"].astype("category")

print("Category dtype:", df["Category"].dtype)
print("Category options:", list(df["Category"].cat.categories))
print()

df.to_csv("news_dataset_cleaned.csv", index=False)
print(f"Saved {len(df)} cleaned rows to news_dataset_cleaned.csv")
