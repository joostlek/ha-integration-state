import os
import pandas as pd

df = pd.read_csv("../output/base.csv", index_col=0)

df["sensor"] = False
df["coordinator"] = False
df["binary_sensor"] = False
df["config_flow"] = False
df["diagnostics"] = False
df["light"] = False
df["scene"] = False
df["switch"] = False

for integration_id, integration in df.iterrows():
    domain = integration["domain"]
    for feature in ("config_flow", "sensor", "coordinator", "binary_sensor", "diagnostics", "light", "scene", "switch"):
        df.at[integration_id, feature] = os.path.isfile(f"../core/homeassistant/components/{domain}/{feature}.py")


df.to_csv("../output/code_features.csv")
