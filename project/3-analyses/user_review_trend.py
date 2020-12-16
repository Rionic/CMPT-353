import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn
seaborn.set()

# Getting data into a form we want
df = pd.read_csv('../2-cleaned_data/business_reviews_users_merged.csv')
df = df.drop(columns=['Unnamed: 0', 'business_id', 'business_name', 'is_open', 'business_stars', 'business_review_count', 'review_id', 'username', 'average_stars'])

# Filter out unknown id name for accurate results
df = df[df['user_id'] != '#NAME?']

# Include users who have at least 100 reviews
df = df[df['user_review_count'] >= 100]

non = df[df['elite'].isnull()]
elite = df[df['elite'].notnull()]

group_non = non.drop(columns=['review_stars', 'date', 'user_review_count', 'elite'])
group_elite = elite.drop(columns=['review_stars', 'date', 'user_review_count', 'elite'])

# Sort by day of review for each user
non = non.groupby(['user_id', 'date']).first().reset_index()
non['review_order'] = non.groupby(['user_id']).cumcount()+1

elite = elite.groupby(['user_id', 'date']).first().reset_index()
elite['review_order'] = elite.groupby(['user_id']).cumcount()+1

df = df.groupby(['user_id', 'date']).first().reset_index()
df['review_order'] = df.groupby(['user_id']).cumcount()+1

# Average rating of each user by user review order
avg = df.drop(columns=['user_id', 'date', 'user_review_count', 'elite'])
avg = avg[avg['review_order'] <= 100]
avg = avg.groupby(['review_order']).mean().reset_index()

fit = stats.linregress(avg['review_order'], avg['review_stars'])
avg['prediction'] = avg['review_order']*fit.slope + fit.intercept

plt.plot(avg['review_order'], avg['review_stars'], 'b.', alpha=1.0, label='Rating Observation')
plt.plot(avg['review_order'], avg['prediction'], 'r-', linewidth=3, label ='Best Fit Line')
plt.title('Average User Ratings vs Review Count')
plt.xlabel('Count')
plt.ylabel('Average Ratings')
x1,x2,y1,y2 = plt.axis()
plt.axis((x1,x2,3.2,4.0))
plt.legend(loc="lower left")
plt.savefig('../4-figures/user_review_trend/user_rating.png')
plt.clf()

# Average rating of each non-elite user by user review order
non = non.drop(columns=['user_id', 'date', 'user_review_count', 'elite'])
non = non[non['review_order'] <= 100]
non_elite = non.groupby(['review_order']).mean().reset_index()

fit = stats.linregress(non_elite['review_order'], non_elite['review_stars'])
non_elite['prediction'] = non_elite['review_order']*fit.slope + fit.intercept

plt.plot(non_elite['review_order'], non_elite['review_stars'], 'b.', alpha=1.0, label='Rating Observation')
plt.plot(non_elite['review_order'], non_elite['prediction'], 'r-', linewidth=3, label ='Best Fit Line')
plt.legend(['Rating Observation', 'Best Fit Line'])
plt.title('Average Non Elite Ratings vs Review Count')
plt.xlabel('Count')
plt.ylabel('Average Ratings')
x1,x2,y1,y2 = plt.axis()
plt.axis((x1,x2,3.2,4.0))
plt.legend(loc="lower left")
plt.savefig('../4-figures/user_review_trend/non_elite_rating.png')
plt.clf()

# Average rating of each elite user by user review order
elite = elite.drop(columns=['user_id', 'date', 'user_review_count', 'elite'])
elite = elite[elite['review_order'] <= 100]
avg_elite = elite.groupby(['review_order']).mean().reset_index()

fit = stats.linregress(avg_elite['review_order'], avg_elite['review_stars'])
avg_elite['prediction'] = avg_elite['review_order']*fit.slope + fit.intercept

plt.plot(avg_elite['review_order'], avg_elite['review_stars'], 'b.', alpha=1.0, label='Rating Observation')
plt.plot(avg_elite['review_order'], avg_elite['prediction'], 'r-', linewidth=3, label ='Best Fit Line')
plt.legend(['Rating Observation', 'Best Fit Line'])
plt.title('Average Elite Ratings vs Review Count')
plt.xlabel('Count')
plt.ylabel('Average Ratings')
x1,x2,y1,y2 = plt.axis()
plt.axis((x1,x2,3.2,4.0))
plt.legend(loc="lower left")
plt.savefig('../4-figures/user_review_trend/elite_rating.png')


