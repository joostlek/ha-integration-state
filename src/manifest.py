import json
import os
import pandas as pd

df = pd.read_csv("output/base.csv", index_col=0)

df["Name"] = None
df["Quality scale"] = None
df["IoT class"] = None
df["Integration type"] = None
df["Codeowners"] = 0
df["External library"] = False
df["Bluetooth zeroconf"] = False
df["Network zeroconf"] = False
df["Application credentials"] = False

for integration_id, integration in df.iterrows():
    domain = integration["domain"]
    with open(f"core/homeassistant/components/{domain}/manifest.json") as manifest_file:
        manifest = json.load(manifest_file)
        df.at[integration_id, "Name"] = manifest.get("name")
        df.at[integration_id, "Quality scale"] = manifest.get("quality_scale")
        df.at[integration_id, "External library"] = "requirements" in manifest
        df.at[integration_id, "Codeowners"] = len(manifest.get("codeowners", []))
        df.at[integration_id, "Integration type"] = manifest.get("integration_type")
        df.at[integration_id, "IoT class"] = manifest.get("iot_class")
        df.at[integration_id, "Bluetooth zeroconf"] = "bluetooth" in manifest
        df.at[integration_id, "Network zeroconf"] = "zeroconf" in manifest
        df.at[integration_id, "Application credentials"] = "application_credentials" in manifest.get("dependencies", [])


df.to_csv("output/manifest.csv")
