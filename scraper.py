import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Create output folder if it doesn't exist
os.makedirs("output", exist_ok=True)

URL = "https://www.bbc.com/news"
response = requests.get(URL)
response.raise_for_status()  # Ensure successful request

soup = BeautifulSoup(response.text, "html.parser")

headlines = []
for item in soup.select("a.gs-c-promo-heading"):
    title = item.get_text(strip=True)
    link = item.get("href")
    if link and not link.startswith("http"):
        link = "https://www.bbc.com" + link
    headlines.append({"title": title, "link": link})

# Convert to DataFrame and save
df = pd.DataFrame(headlines)
df.to_csv("output/headlines.csv", index=False)
print(f"✅ Saved {len(df)} headlines to output/headlines.csv")
