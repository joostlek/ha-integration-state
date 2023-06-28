import os
from _ast import ImportFrom

import pandas as pd
import ast

df = pd.read_csv("output/base.csv", index_col=0)

df["Base entity in init"] = None
df["Coordinator in init"] = None
df["Sensor descriptions in const"] = None


for integration_id, integration in df.iterrows():
    domain = integration["domain"]
    if os.path.isfile(f"core/homeassistant/components/{domain}/__init__.py"):
        df.at[integration_id, "Base entity in init"] = False
        df.at[integration_id, "Coordinator in init"] = False
        with open(f"core/homeassistant/components/{domain}/__init__.py") as init_file:
            structure = ast.parse(init_file.read())

            for expression in structure.body:
                if isinstance(expression, ImportFrom):
                    if expression.module == "homeassistant.helpers.entity":
                        for imported_name in expression.names:
                            if imported_name.name == "Entity":
                                df.at[integration_id, "Base entity in init"] = True
                                break

            for expression in structure.body:
                if isinstance(expression, ImportFrom):
                    if expression.module == "homeassistant.helpers.update_coordinator":
                        for imported_name in expression.names:
                            if imported_name.name == "DataUpdateCoordinator":
                                df.at[integration_id, "Coordinator in init"] = True
                                break
    if os.path.isfile(f"core/homeassistant/components/{domain}/const.py"):
        df.at[integration_id, "Sensor descriptions in const"] = False
        with open(f"core/homeassistant/components/{domain}/const.py") as const_file:
            structure = ast.parse(const_file.read())

            for expression in structure.body:
                if isinstance(expression, ImportFrom):
                    if expression.module == "homeassistant.components.sensor":
                        for imported_name in expression.names:
                            if imported_name.name == "SensorEntityDescription":
                                df.at[integration_id, "Sensor descriptions in const"] = True
                                break


df.to_csv("output/python_ast.csv")
