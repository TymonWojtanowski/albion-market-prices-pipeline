import requests
import pandas as pd
import json
import pyarrow
from datetime import datetime, timezone
MAX_BATCH_SIZE = 3800

item_ids = []
batches = []
current_batch = []
items_final = ""
url = ""

classic_url = (
    "https://europe.albion-online-data.com/api/v2/stats/prices/"
    "{item_ids}.json"
    #"?locations=Caerleon,Bridgewatch&qualities=2"
)

with open("items.json", mode="r", encoding="utf-8") as file:
    items = json.load(file)

for item in items:
    item_ids.append(item["UniqueName"])

for item in item_ids:
    candidate_batch = current_batch + [item]
    candidate_ids = ",".join(candidate_batch)
    test_url = classic_url.format(item_ids=candidate_ids)

    if len(test_url) > MAX_BATCH_SIZE:
        batches.append(current_batch)
        current_batch = [item]
    else:
        current_batch = candidate_batch

if len(current_batch) > 0:
    batches.append(current_batch)

all_data = []

for batch in batches:
    url_data = ",".join(batch)
    url = classic_url.format(item_ids=url_data)

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    batch_data = response.json()
    all_data.extend(batch_data)

df = pd.DataFrame(all_data)

print("Rozmiar:", df.shape)
df.info()

print("Unikalne itemy:", df["item_id"].nunique())
print("Miasta:", df["city"].nunique())
print("Jakości:")
print(df["quality"].value_counts().sort_index())
print("Braki:")
print(df.isna().sum())
print("Zerowe ceny sprzedaży:", (df["sell_price_min"] == 0).sum())
print("Zerowe ceny kupna:", (df["buy_price_max"] == 0).sum())
print("Pełne duplikaty:", df.duplicated().sum())
print(len(items))
print(len(set(item_ids)))
print(df["item_id"].nunique())


df.to_parquet(
    "prices.parquet",
    index=False
)

test_parquet = pd.read_parquet(
    "prices.parquet"
)
print(test_parquet.shape)