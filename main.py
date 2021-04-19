import pandas as pd
import json

df = pd.read_csv('data.csv', skiprows=range(0, 3))

old_headers = df.columns.values.tolist()
df_new = df.where(df.notnull(), None)

new_headers = []
for header in old_headers:
    if "C:" in header:
        new_headers.append(header.replace("C:", ""))
    else:
        new_headers.append(header)

df_new.columns = new_headers

reader = df_new.to_dict('records')

results = []
for row in reader:
    new_row = {}
    asperts = []
    for key in row:
        if key in ['ItemId', 'Category ID', 'Custom Label (SKU)', 'Title', 'Format','VariationSet','SiteID','Reserved1-Do not edit or delete']:
            new_row[key] = row[key]
        else:
            if row[key] is not None:
                new_aspert = {}
                new_aspert['LocalizedAspectName'] = key
                if isinstance(row[key], str) and ',' in row[key]:
                    value = row[key].split(',')
                    new_aspert['AspectValues'] = value
                else:
                    new_aspert['AspectValues'] = row[key]
                asperts.append(new_aspert)
    new_row['Aspects'] = asperts
    results.append(new_row)

with open('results.json', 'w') as outfile:
    json.dump(results, outfile)
