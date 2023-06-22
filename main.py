import pandas as pd
import os
import json
import subprocess
import re

def is_real_integration(name: str) -> bool:
    return os.path.isfile(f"homeassistant/components/{name}/__init__.py")
integrations = [x for x in os.listdir("homeassistant/components") if is_real_integration(x)]

df = pd.DataFrame(index=integrations, columns=["quality_scale", "config_flow", "sensor", "iot_class", "integration_type", "external_library", "codeowners", "has_tests", "coverage"])
def has_feature(name: str, featur: str) -> bool:
    return os.path.isfile(f"homeassistant/components/{name}/{featur}.py")
df = df.sort_index()
for integration_name, integration in df.iterrows():
    for feature in ("config_flow", "sensor"):
        df.at[integration_name, feature] = has_feature(integration_name, feature)
    with open(f"homeassistant/components/{integration_name}/manifest.json") as manifest_file:
        manifest = json.load(manifest_file)
    if "integration_type" in manifest:
        df.at[integration_name, "integration_type"] = manifest["integration_type"]
    if "iot_class" in manifest:
        df.at[integration_name, "iot_class"] = manifest["iot_class"]
    if "quality_scale" in manifest:
        df.at[integration_name, "quality_scale"] = manifest["quality_scale"]
    df.at[integration_name, "external_library"] = False
    if "requirements" in manifest:
        df.at[integration_name, "external_library"] = True
    df.at[integration_name, "codeowners"] = 0
    if "codeowners" in manifest:
        df.at[integration_name, "codeowners"] = len(manifest["codeowners"])
    has_tests = os.path.exists(f"tests/components/{integration_name}")
    df.at[integration_name, "has_tests"] = has_tests
    if has_tests:
        try:
            p = subprocess.Popen(["pytest", f"tests/components/{integration_name}", f"--cov=homeassistant.components.{integration_name}"], stdout=subprocess.PIPE)
            test, err = p.communicate()
            regex = r"TOTAL.*\s(\d*)%"
            result = re.search(regex, str(test))
            df.at[integration_name, "coverage"] = result.group(1)
        except:
            pass

df.to_excel("./state.xlsx")