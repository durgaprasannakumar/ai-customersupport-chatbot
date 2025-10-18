import pandas as pd

# Load full Kaggle dataset
df = pd.read_csv("data/customer_support_tweets.csv")


# Normalize and clean
print(f"Loaded {len(df):,} rows")


df["brand"] = df["author_id"].astype(str).str.lower()
df = df[df["inbound"] == True] # customer messages only
df = df[["brand", "created_at", "text"]].dropna(subset=["text"])
df = df.drop_duplicates(subset=["text"])


# Optional: keep top brands (for smaller prototype)
top_brands = df["brand"].value_counts().nlargest(10).index
df = df[df["brand"].isin(top_brands)]


# Save cleaned dataset
df.to_csv("data/support_tweets_sample.csv", index=False)
print(f"Saved {len(df):,} cleaned rows for indexing.")