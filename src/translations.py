import json
import os
import pandas as pd
integrations = [x for x in os.listdir("core/homeassistant/components") if os.path.isdir(f"core/homeassistant/components/{x}")]

df = pd.DataFrame(columns=[
    "translation_key",
    "value",
    "amount"
])

for domain in integrations:
    if not os.path.isfile(f"core/homeassistant/components/{domain}/strings.json"):
        continue
    with open(f"core/homeassistant/components/{domain}/strings.json") as string_file:
        strings = json.load(string_file)
        if "entity" not in strings:
            continue
        for platform, translation_keys in strings["entity"].items():
            for translation_key, translation in translation_keys.items():
                if "name" not in translation:
                    continue
                name = translation['name'].replace("%", "").replace("::", "_").replace(":", "_").replace("'", "_")
                row = df.query(f"translation_key == '{translation_key}' and value == '{name}'")
                if not row.empty:
                    df.loc[row.index, "amount"] = df.loc[row.index, "amount"] + 1
                else:
                    df.loc[len(df)] = [translation_key, translation['name'], 1]

df = df.sort_values("amount", ascending=False)
df.to_csv("output/translation_values.csv")

df = df.drop(columns=["value"])
# print(df.head())
df = df.groupby(["translation_key"]).sum()
print(df.head())

# print(df.to_frame().rename(columns={"translation_key": "amount"}).reset_index().sort_values(["amount"], ascending=False).head())
df = df.reset_index().sort_values(["amount"], ascending=False)
df.to_csv("output/translation_keys.csv")
