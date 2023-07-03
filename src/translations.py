import json
import os
import pandas as pd
integrations = [x for x in os.listdir("core/homeassistant/components") if os.path.isdir(f"core/homeassistant/components/{x}")]

df = pd.DataFrame(columns=[
    "translation_key",
    "value",
    "amount"
])
df_cf = pd.DataFrame(columns=[
    "translation_key",
    "value",
    "amount"
])

for domain in integrations:
    if not os.path.isfile(f"core/homeassistant/components/{domain}/strings.json"):
        continue
    with open(f"core/homeassistant/components/{domain}/strings.json") as string_file:
        strings = json.load(string_file)
        if "entity" in strings:
            for platform, translation_keys in strings["entity"].items():
                for translation_key, translation in translation_keys.items():
                    if "name" in translation:
                        name = translation['name'].replace("%", "").replace("::", "_").replace(":", "_").replace("'", "_")
                        row = df.query(f"translation_key == '{translation_key}' and value == '{name}'")
                        if not row.empty:
                            df.loc[row.index, "amount"] = df.loc[row.index, "amount"] + 1
                        else:
                            df.loc[len(df)] = [translation_key, name, 1]
        if "config" in strings:
            if "step" in strings["config"]:
                for step_id, step in strings["config"]["step"].items():
                    if "data" in step:
                        for translation_key, translation in step["data"].items():
                            name = translation.replace("%", "").replace("::", "_").replace(":", "_").replace("'", "_")
                            row = df_cf.query(f"translation_key == '{translation_key}' and value == '{name}'")
                            if not row.empty:
                                df_cf.loc[row.index, "amount"] = df_cf.loc[row.index, "amount"] + 1
                            else:
                                df_cf.loc[len(df_cf)] = [translation_key, name, 1]
        if "options" in strings:
            if "step" in strings["options"]:
                for step_id, step in strings["options"]["step"].items():
                    if "data" in step:
                        for translation_key, translation in step["data"].items():
                            name = translation.replace("%", "").replace("::", "_").replace(":", "_").replace("'", "_")
                            row = df_cf.query(f"translation_key == '{translation_key}' and value == '{name}'")
                            if not row.empty:
                                df_cf.loc[row.index, "amount"] = df_cf.loc[row.index, "amount"] + 1
                            else:
                                df_cf.loc[len(df_cf)] = [translation_key, name, 1]


df = df.sort_values("amount", ascending=False)
df.to_csv("output/translation_values.csv")

df = df.drop(columns=["value"])
df = df.groupby(["translation_key"]).sum()

df = df.reset_index().sort_values(["amount"], ascending=False)
df.to_csv("output/translation_keys.csv")

df_cf = df_cf.sort_values("amount", ascending=False)
df_cf.to_csv("output/translation_config_flow_values.csv")

df_cf = df_cf.drop(columns=["value"])
df_cf = df_cf.groupby(["translation_key"]).sum()

df_cf = df_cf.reset_index().sort_values(["amount"], ascending=False)
df_cf.to_csv("output/translation_config_flow_keys.csv")
