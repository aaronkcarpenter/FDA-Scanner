import requests
import json
import api
import numpy as np
import pandas as pd

# Call The API
r = requests.get(url=api.api_url)
print("Status Code", r.status_code)
print("*" * 20)
print(r.headers)

html_response = r.text

# Read and Save the Raw API Response as JSON in a File
with open("raw_pushshift_response.json", "w") as outfile:
    outfile.write(html_response)

json_dict = json.loads(html_response)
json_dict.keys()

json_dict["metadata"]

# View The JSON Data
json_dict['data'][0]


# Creating the Request JSON
date_list = []
comment_list = []
rows_list = []

for i in range(len(json_dict['data'])):
    temp_dict = {}
    temp_dict['id'] = i
    temp_dict['text'] = json_dict['data'][i]['body']
    rows_list.append(temp_dict)
    date_list.append(json_dict['data'][i]['created_utc'])
    comment_list.append(json_dict['data'][i]['body'])

sample_dict = {}
sample_dict['documents'] = rows_list
payload = json.dumps(sample_dict)

with open('sentiments_payload.json', 'w') as outfile:
    outfile.write(payload)
    

# Viewing the Sentiments Data
# Loading the Response of the request in a Pandas dataframe
# look at the first row and get an idea of the output
df_sent = pd.DataFrame(json.loads(response.text)['result']['documents'])
df_sent.head(1)

# Convert the Sentiment Score into A label
def get_sentiments(score):
    if score > 0.6:
        return 'Positive'
    elif score < 0.4:
        return 'Negative'
    else:
        return 'Neutral'
    
df_sent['sentiments'] = df_sent['sentiments_score'].apply(get_sentiments)
df_sent.head(1)