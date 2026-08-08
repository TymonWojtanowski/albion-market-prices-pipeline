import pandas as pd
import json
from datetime import datetime, timezone

items_metadata = []
with open("items.json", mode="r", encoding="utf-8") as file:
    items = json.load(file)

for item in items:
    items_metadata.append({
        "item_id": item["UniqueName"],
        "item_name_en": (item.get("LocalizedNames") or {}).get("EN-US"),
        "item_name_pl": (item.get("LocalizedNames") or {}).get("PL-PL")
    })

df = pd.DataFrame(items_metadata)
df.to_parquet(
    "items_metadata.parquet",
    index=False
)

test_parquet = pd.read_parquet("items_metadata.parquet")
print(test_parquet.shape)