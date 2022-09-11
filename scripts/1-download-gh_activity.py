#%%
import requests
#%%
response = requests.get('https://data.gharchive.org/2022-06-05-0.json.gz')

#%%
file_name = '2022-06-05-0.json.gz'
path = 'scripts/data/' + file_name
with open(path, 'wb+') as f:
    f.write(response.content)


