import json
import os
import pandas as pd

df = pd.read_csv("output/base.csv", index_col=0)

df["Duplicate entity naming"] = 0
df["Duplicate config flow naming"] = 0

for integration_id, integration in df.iterrows():
    domain = integration["domain"]
    if not os.path.isfile(f"core/homeassistant/components/{domain}/strings.json"):
        continue
    with open(f"core/homeassistant/components/{domain}/strings.json") as string_file:
        strings = json.load(string_file)
        entity_naming = []
        duplicate_entity_naming = 0
        config_flow_naming = []
        duplicate_config_flow_naming = 0
        if "entity" in strings:
            for platform, translation_keys in strings["entity"].items():
                for translation_key, translation in translation_keys.items():
                    if translation.startswith('['):
                        continue
                    if translation in entity_naming:
                        duplicate_entity_naming = duplicate_entity_naming + 1
                    else:
                        entity_naming.append(translation)
        if "config" in strings:
            if "step" in strings["config"]:
                for step_id, step in strings["config"]["step"].items():
                    if "data" in step:
                        for translation_key, translation in step["data"].items():
                            if translation.startswith('['):
                                continue
                            if translation in config_flow_naming:
                                duplicate_config_flow_naming = duplicate_config_flow_naming + 1
                            else:
                                config_flow_naming.append(translation)
        if "options" in strings:
            if "step" in strings["options"]:
                for step_id, step in strings["options"]["step"].items():
                    if "data" in step:
                        for translation_key, translation in step["data"].items():
                            if translation.startswith('['):
                                continue
                            if translation in config_flow_naming:
                                duplicate_config_flow_naming = duplicate_config_flow_naming + 1
                            else:
                                config_flow_naming.append(translation)
        df.at[integration_id, "Duplicate entity naming"] = duplicate_entity_naming
        df.at[integration_id, "Duplicate config flow naming"] = duplicate_config_flow_naming


df.to_csv("output/translation_duplicates.csv")