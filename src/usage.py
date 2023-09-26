import json
import os
import pandas as pd
from const import ENTITY_PLATFORMS

df = pd.read_csv("output/base.csv", index_col=0)

df["Users"] = None

with open("data.json") as analytics:
    data = json.load(analytics)
    integration_data = data["current"]["integrations"]
    for integration_id, integration in df.iterrows():
        domain = integration["domain"]
        if domain in integration_data:
            df["Users"] = integration_data[domain]


df.to_csv("output/usage.csv")
