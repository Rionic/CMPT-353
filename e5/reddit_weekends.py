import pandas as pd
import numpy as np
import sys
from datetime import date
from scipy import stats
import matplotlib.pyplot as plt
pd.options.mode.chained_assignment = None  # default='warn'

OUTPUT_TEMPLATE = (
    "Initial T-test p-value: {initial_ttest_p:.3g}\n"
    "Original data normality p-values: {initial_weekday_normality_p:.3g} {initial_weekend_normality_p:.3g}\n"
    "Original data equal-variance p-value: {initial_levene_p:.3g}\n"
    "Transformed data normality p-values: {transformed_weekday_normality_p:.3g} {transformed_weekend_normality_p:.3g}\n"
    "Transformed data equal-variance p-value: {transformed_levene_p:.3g}\n"
    "Weekly data normality p-values: {weekly_weekday_normality_p:.3g} {weekly_weekend_normality_p:.3g}\n"
    "Weekly data equal-variance p-value: {weekly_levene_p:.3g}\n"
    "Weekly T-test p-value: {weekly_ttest_p:.3g}\n"
    "Mann-Whitney U-test p-value: {utest_p:.3g}"
)

counts = pd.read_json(sys.argv[1], lines=True)

counts = counts[counts['subreddit'] == 'canada']

counts['date'] = counts['date'].dt.strftime('%Y-%m-%d')

dates = counts['date'].str.split('-').str[0].astype(int)
counts = counts[(dates ==  2013) | (dates == 2012)]

counts['date'] = pd.to_datetime(counts['date'])

counts['day'] = counts['date'].dt.dayofweek

weekdays = (counts['day'] == 0) | (counts['day'] == 1) | (counts['day'] == 2) | (counts['day'] == 3) | (counts['day'] == 4)
weekdaysdf = counts[weekdays]

weekends = (counts['day'] == 5) | (counts['day'] == 6)
weekendsdf = counts[weekends]

x = weekdaysdf.comment_count
y = weekendsdf.comment_count

initial_ttest_p = stats.ttest_ind(x, y).pvalue
initial_weekday_normality_p = stats.normaltest(x).pvalue
initial_weekend_normality_p = stats.normaltest(y).pvalue
initial_levene_p = stats.levene(x,y).pvalue

# fix 1: transformation. Sqrt works the best due to highest p-values on the normal test & levene
transformed_weekday_normality_p = stats.normaltest(np.sqrt(x)).pvalue
transformed_weekend_normality_p = stats.normaltest(np.sqrt(y)).pvalue
transformed_levene_p = stats.levene(np.sqrt(x), np.sqrt(y)).pvalue

# fix 2: central limit theorem
weekday_dates = weekdaysdf.date.apply(date.isocalendar)
weekdaysdf['year-week'] = weekday_dates.str[0:2]
weekdaysdf2 = weekdaysdf.groupby(['year-week']).mean()

weekend_dates = weekendsdf.date.apply(date.isocalendar)
weekendsdf['year-week'] = weekend_dates.str[0:2]
weekendsdf2 = weekendsdf.groupby(['year-week']).mean()

x2 = weekdaysdf2.comment_count
y2 = weekendsdf2.comment_count

weekly_weekday_normality_p = stats.normaltest(x2).pvalue
weekly_weekend_normality_p = stats.normaltest(y2).pvalue
weekly_levene_p = stats.levene(x2,y2).pvalue
weekly_ttest_p = stats.ttest_ind(x2,y2).pvalue

# fix 3: non-parametric test
utest_p = stats.mannwhitneyu(x,y).pvalue*2

print(OUTPUT_TEMPLATE.format(
        initial_ttest_p=initial_ttest_p,
        initial_weekday_normality_p=initial_weekday_normality_p,
        initial_weekend_normality_p=initial_weekend_normality_p,
        initial_levene_p=initial_levene_p,
        transformed_weekday_normality_p=transformed_weekday_normality_p,
        transformed_weekend_normality_p=transformed_weekend_normality_p,
        transformed_levene_p=transformed_levene_p,
        weekly_weekday_normality_p=weekly_weekday_normality_p,
        weekly_weekend_normality_p=weekly_weekend_normality_p,
        weekly_levene_p=weekly_levene_p,
        weekly_ttest_p=weekly_ttest_p,
        utest_p=utest_p,
    ))