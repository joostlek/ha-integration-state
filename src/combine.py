import json
import os

import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe

base = pd.read_csv("../output/base.csv", index_col=0)
manifest = pd.read_csv("../output/manifest.csv", index_col=0)
code_features = pd.read_csv("../output/code_features.csv", index_col=0)
test_features = pd.read_csv("../output/test_features.csv", index_col=0)

result = pd.merge(base, manifest, how="left", on="domain")
result = pd.merge(result, code_features, how="left", on="domain")
result = pd.merge(result, test_features, how="left", on="domain")

result.to_excel("../output/state.xlsx")
scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
google_service_account = json.loads(os.environ.get("GOOGLE_SERVICE_ACCOUNT", "{}"))
credentials = Credentials.from_service_account_info(google_service_account, scopes=scopes)

gc = gspread.authorize(credentials)
gs = gc.open_by_key(os.environ.get("sheet_key"))
worksheet1 = gs.worksheet("Current state")

set_with_dataframe(worksheet=worksheet1, dataframe=result, include_index=False, include_column_header=True, resize=True)