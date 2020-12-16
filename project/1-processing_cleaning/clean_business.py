import pandas as pd

df = pd.read_json('../0-raw_data/yelp_academic_dataset_business.json', lines=True) # Needs raw data file to work. Add later
df = df[df.categories.str.contains('Restaurants', regex=False, na=False)]
top_city = df.groupby(df.city).count()
top_city = top_city.sort_values(by=['business_id']).iloc[-1].name
df = df[df.city == top_city]
df = df[df.is_open == 1]
df.to_csv('../2-cleaned_data/business_cleaned.csv')