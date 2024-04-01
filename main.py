import json
import pandas as pd
from parser import ParsedHabr

with open("configurations.json", "r") as f:
    parsing_data = json.load(f)

links_scientist = parsing_data.get('links_scientist')
links_analytic = parsing_data.get('links_analytic')

parsed_scientists = ParsedHabr(links_scientist, parsing_data)
scientists = parsed_scientists.get_dataframe()

parsed_analytics = ParsedHabr(links_analytic, parsing_data)
analytics = parsed_analytics.get_dataframe()

with pd.ExcelWriter('parsing_results.xlsx') as writer:
    scientists.to_excel(writer, sheet_name='Scientists')
    analytics.to_excel(writer, sheet_name='Analytics')
