from checkbooknyc import CheckbookNYC
import json
import pandas as pd

search_criteria = {
    "issue_date": "2011-07-13",
}

c = CheckbookNYC(type_name="Spending", search_criteria=search_criteria)
a = c()
results = []
for i in a:
    results += i['response']['result_records']['spending_transactions']['transaction']

df = pd.DataFrame(results)
print(df.shape)
df.to_csv('test.csv')
with open('test.json', 'w') as f:
    json.dump(a, f, indent=4)
