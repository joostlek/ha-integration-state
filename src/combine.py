import json
import os

import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe

base = pd.read_csv("output/base.csv", index_col=0)
manifest = pd.read_csv("output/manifest.csv", index_col=0)
code_features = pd.read_csv("output/code_features.csv", index_col=0)
test_features = pd.read_csv("output/test_features.csv", index_col=0)
python_ast = pd.read_csv("output/python_ast.csv", index_col=0)
duplicate_translations = pd.read_csv("output/translation_duplicates.csv", index_col=0)

result = pd.merge(base, manifest, how="left", on="domain")
result = pd.merge(result, code_features, how="left", on="domain")
result = pd.merge(result, test_features, how="left", on="domain")
result = pd.merge(result, python_ast, how="left", on="domain")
result = pd.merge(result, duplicate_translations, how="left", on="domain")

result.to_excel("output/state.xlsx")
scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

google_service_account = json.loads(os.environ.get("GOOGLE_SERVICE_ACCOUNT", "{}"))
credentials = Credentials.from_service_account_info(google_service_account, scopes=scopes)

gc = gspread.authorize(credentials)
gs = gc.open_by_key(os.environ.get("SHEET_KEY"))
worksheet1 = gs.worksheet("Current state")

set_with_dataframe(worksheet=worksheet1, dataframe=result, include_index=False, include_column_header=True, resize=True)

translation_key_worksheet = gs.worksheet("Translations by keys")
translation_keys = pd.read_csv("output/translation_keys.csv", index_col=0)

set_with_dataframe(worksheet=translation_key_worksheet, dataframe=translation_keys, include_index=False, include_column_header=True, resize=True)

translation_value_worksheet = gs.worksheet("Translations by values")
translation_values = pd.read_csv("output/translation_values.csv", index_col=0)

set_with_dataframe(worksheet=translation_value_worksheet, dataframe=translation_values, include_index=False, include_column_header=True, resize=True)

translation_config_flow_key_worksheet = gs.worksheet("Translations by config flow keys")
translation_config_flow_keys = pd.read_csv("output/translation_config_flow_keys.csv", index_col=0)

set_with_dataframe(worksheet=translation_config_flow_key_worksheet, dataframe=translation_config_flow_keys, include_index=False, include_column_header=True, resize=True)

translation_config_flow_value_worksheet = gs.worksheet("Translations by config flow values")
translation_config_flow_values = pd.read_csv("output/translation_config_flow_values.csv", index_col=0)

set_with_dataframe(worksheet=translation_config_flow_value_worksheet, dataframe=translation_config_flow_values, include_index=False, include_column_header=True, resize=True)