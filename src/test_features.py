import os
import pandas as pd

df = pd.read_csv("output/base.csv", index_col=0)

df["test_sensor"] = None
df["test_binary_sensor"] = None
df["test_config_flow"] = None
df["test_diagnostics"] = None
df["test_light"] = None
df["test_scene"] = None
df["test_switch"] = None

for integration_id, integration in df.iterrows():
    domain = integration["domain"]
    for feature in ("config_flow", "sensor", "binary_sensor", "diagnostics", "light", "scene", "switch"):
        if os.path.isfile(f"core/homeassistant/components/{domain}/{feature}.py"):
            df.at[integration_id, f"test_{feature}"] = os.path.isfile(f"core/tests/components/{domain}/test_{feature}.py")


df.to_csv("output/test_features.csv")
