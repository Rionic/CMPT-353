# Chi-Squared Test with restaurant nationalities as categories and their corresponding ratings

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn
seaborn.set()
import matplotlib.patches as mpatches
from statsmodels.stats.multicomp import pairwise_tukeyhsd


df = pd.read_csv('../2-cleaned_data/business_cleaned.csv')

df = df.drop(columns=['Unnamed: 0', 'is_open', 'hours', 'address', 'attributes', 'latitude', 'longitude', 'postal_code', 'city', 'state'])

american = df[df.categories.str.contains('American')].groupby('stars').count().iloc[:,0]
thai = df[df.categories.str.contains('Thai')].groupby('stars').count().iloc[:,0]
indian = df[df.categories.str.contains('Indian')].groupby('stars').count().iloc[:,0]
chinese = df[df.categories.str.contains('Chinese')].groupby('stars').count().iloc[:,0]
mexican = df[df.categories.str.contains('Mexican')].groupby('stars').count().iloc[:,0]
italian = df[df.categories.str.contains('Italian')].groupby('stars').count().iloc[:,0]
japanese = df[df.categories.str.contains('Japanese')].groupby('stars').count().iloc[:,0]

contingency = pd.concat([american, thai, indian, chinese, mexican, italian, japanese], axis=1, 
                        keys=['American', 'Thai', 'Indian', 'Chinese', 'Mexican', 'Italian', 'Japanese'])
contingency = contingency.fillna(0)
contingency = contingency.T
# Each category has > 5 observations, so we can proceed
print(contingency)

chi2, p, dof, expected = stats.chi2_contingency(contingency.values)
print("P-value:", p)
print("We can conclude the nationality of the restaurant has an effect on the rating")
print("Expected values:")
expected = pd.DataFrame(expected.round(1), columns=['1.0', '1.5', '2.0', '2.5', '3.0', '3.5', '4.0', '4.5', '5.0'], 
                        index=['American', 'Thai', 'Indian', 'Chinese', 'Mexican', 'Italian', 'Japanese'])
print(expected)

american = df[df.categories.str.contains('American')]
thai = df[df.categories.str.contains('Thai')]
indian = df[df.categories.str.contains('Indian')]
chinese = df[df.categories.str.contains('Chinese')]
mexican = df[df.categories.str.contains('Mexican')]
italian = df[df.categories.str.contains('Italian')]
japanese = df[df.categories.str.contains('Japanese')]

plt.hist([american.stars, thai.stars, indian.stars, chinese.stars, mexican.stars, italian.stars, japanese.stars],
        bins=[1,1.5,2,2.5,3,3.5,4,4.5,5])
plt.title('Restaurant Ratings by Nationality', fontsize=14)
plt.xlabel('Rating')
plt.ylabel('Frequency')
blue_patch = mpatches.Patch(color='blue', label='American')
orange_patch = mpatches.Patch(color='orange', label='Thai')
green_patch = mpatches.Patch(color='green', label='Indian')
red_patch = mpatches.Patch(color='red', label='Chinese')
purple_patch = mpatches.Patch(color='purple', label='Mexican')
brown_patch = mpatches.Patch(color='brown', label='Italian')
pink_patch = mpatches.Patch(color='pink', label='Japanese')

plt.legend(handles=[blue_patch, orange_patch, green_patch, red_patch, purple_patch, brown_patch, pink_patch])
plt.savefig('../4-figures/nationality_comparison/nationality_ratings.png')

# P-value < 0.05 means we can conduct a post-hoc analysis 
anova = stats.f_oneway(american.stars, thai.stars, indian.stars, chinese.stars, mexican.stars, italian.stars, japanese.stars)
print('ANOVA P-value:', anova.pvalue)

df2 = pd.concat([american.stars, thai.stars, indian.stars, chinese.stars, mexican.stars, italian.stars, japanese.stars],
                axis=1, keys=['American', 'Thai', 'Indian', 'Chinese', 'Mexican', 'Italian', 'Japanese'])
melt = pd.melt(df2)
melt = melt.dropna()
posthoc = pairwise_tukeyhsd(melt['value'], melt['variable'], alpha=0.5)
print(posthoc)
graph = posthoc.plot_simultaneous() # Shows up in Jupyter only