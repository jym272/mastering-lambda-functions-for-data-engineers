#%%
import pandas as pd
#%%
df = pd.read_json('scripts/data/2022-06-05-0.json.gz', lines=True)

#%%
df.columns
df.dtypes
df['org']
