import os
import pandas as pd

integrations = [x for x in os.listdir("../core/homeassistant/components") if os.path.isdir(f"../core/homeassistant/components/{x}")]

df = pd.DataFrame({"domain": integrations})
df = df.sort_values("domain")
df.reset_index(inplace=True)
df = df.drop(columns=["index"])
df.to_csv("../output/base.csv")
