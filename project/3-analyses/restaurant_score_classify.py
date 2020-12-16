import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

import json
import ast

df = pd.read_csv('../2-cleaned_data/business_cleaned.csv')
df = df[['business_id','name','stars','review_count','attributes','categories','hours']]

df['attributes'] = df[~df['attributes'].isna()]['attributes'].apply(lambda x: eval(x)) #https://www.reddit.com/r/learnpython/comments/4599hl/module_to_guess_type_from_a_string/

# https://stackoverflow.com/a/38231651
attr_df = pd.concat([df.drop(['attributes'], axis=1), df['attributes'].apply(pd.Series)], axis=1)
attr_df = attr_df[~attr_df['Ambience'].isna()]
attr_df = pd.concat([attr_df.drop(['Ambience'], axis=1), attr_df['Ambience'].apply(lambda x: eval(x)).apply(pd.Series)], axis=1)
# attr_df[['romantic',]].fillna(False, inplace=True)

attr_df = attr_df[~attr_df['RestaurantsPriceRange2'].isna()] # We lost 36 from the original 4398 rows
attr_df['RestaurantsPriceRange2'] = attr_df['RestaurantsPriceRange2'].apply(lambda x: eval(x))
attr_df = attr_df[~attr_df['RestaurantsPriceRange2'].isna()]
attr_df['RestaurantsPriceRange2'] = attr_df['RestaurantsPriceRange2'].astype(int)

attr_df['RestaurantsAttire'].fillna("'casual'", inplace=True)
attr_df['RestaurantsAttire'] = attr_df['RestaurantsAttire'].apply(lambda x: eval(x)).replace({'casual':0, np.nan:0, 'dressy':1, 'formal':1}) #one-hot encode


#filter out completely empty Ambience
attr_df = attr_df[~(attr_df['romantic'].isna() & 
          attr_df['intimate'].isna() & 
          attr_df['classy'].isna() & 
          attr_df['hipster'].isna() & 
          attr_df['divey'].isna() & 
          attr_df['touristy'].isna() & 
          attr_df['trendy'].isna() & 
          attr_df['upscale'].isna() & 
          attr_df['casual'].isna())]

attr_df['romantic'].fillna(value=False, inplace=True)
attr_df['upscale'].fillna(value=False, inplace=True)

# attr_df['stars'] = (attr_df['stars']*2).astype(int) # Double the ratings to consider int rather than float

attr_df['successful'] = df['stars'] >= 3.5

X = attr_df[['review_count','RestaurantsPriceRange2']]
y = attr_df['successful']

model = GaussianNB()
X_train, X_valid, y_train, y_valid = train_test_split(X,y)
model.fit(X_train, y_train)
print(f'classifier accuracy score: {model.score(X_valid, y_valid)}')