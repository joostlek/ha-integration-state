import os
import pandas as pd

from const import ENTITY_PLATFORMS

df = pd.read_csv("output/base.csv", index_col=0)
files = ["config_flow", *ENTITY_PLATFORMS]
for entity_platform in files:
    df[entity_platform] = False

for integration_id, integration in df.iterrows():
    domain = integration["domain"]
    for feature in files:
        df.at[integration_id, feature] = os.path.isfile(f"core/homeassistant/components/{domain}/{feature}.py")


df.to_csv("output/code_features.csv")
