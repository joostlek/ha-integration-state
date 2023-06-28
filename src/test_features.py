import os
import pandas as pd
from const import ENTITY_PLATFORMS

df = pd.read_csv("output/base.csv", index_col=0)

for entity_platform in ENTITY_PLATFORMS:
    df[f"Tests: {entity_platform}"] = False

for integration_id, integration in df.iterrows():
    domain = integration["domain"]
    for feature in ENTITY_PLATFORMS:
        if os.path.isfile(f"core/homeassistant/components/{domain}/{feature}.py"):
            df.at[integration_id, f"Tests: {feature}"] = os.path.isfile(f"core/tests/components/{domain}/test_{feature}.py")


df.to_csv("output/test_features.csv")
