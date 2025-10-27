import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd

# 1️⃣ Create the output directory if it doesn't exist
os.makedirs("output", exist_ok=True)

# 2️⃣ Define target URL + headers
url = "https://news.ycombinator.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

# 3️⃣ Fetch the page
resp = requests.get(url, headers=headers)
resp.raise_for_status()
soup = BeautifulSoup(resp.text, "html.parser")

# 4️⃣ Extract article titles & links
articles = soup.select("span.titleline > a")

data = []
for a in articles:
    title = a.get_text(strip=True)
    link = a.get("href")
    if link and link.startswith("/"):
        link = "https://news.ycombinator.com" + link
    data.append({"Title": title, "Link": link})

df = pd.DataFrame(data)

# 5️⃣ Generate timestamped filename
ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
csv_path = f"output/headlines_{ts}.csv"
json_path = f"output/headlines_{ts}.json"

# 6️⃣ Save both CSV and JSON
df.to_csv(csv_path, index=False, encoding="utf-8-sig")
df.to_json(json_path, orient="records", force_ascii=False, indent=2)

# 7️⃣ Print completion message
print(f"✅ Scraped {len(df)} headlines")
print(f"Saved to:\n - {csv_path}\n - {json_path}")
