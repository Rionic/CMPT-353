import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from scipy import stats

# pd.set_option("display.max_rows", None, "display.max_columns", None)

tweets = pd.read_csv('dog_rates_tweets.csv', index_col=0, 
                     usecols=[0,1,2], parse_dates=True)
df = tweets
df2 = df
df3 = df
#df
# df = df[df['text'].str.contains(r'(\d+(\.\d+)?)/10')]
df = df['text'].str.extractall(r'(\d+(\.\d+)?)/10')
df[0] = pd.to_numeric(df[0])
remove_outliers = df[0] <=25
df = df[remove_outliers]
df = df.reset_index(level=1, drop=True)
df = df[0]
# tweets['rating'] = df[0]
tweets = tweets.merge(df, left_on='id', right_on='id')
tweets = tweets.drop(['text'], axis=1)
plt.figure(figsize=(10, 5)) # change the size to something sensible
plt.xlabel("Created at")
plt.ylabel("Rating")
plt.title("Daily correlation")
plt.scatter(tweets['created_at'].values, tweets[0].values)
plt.show()