import sys
from pyspark.sql import SparkSession, functions, types
import pandas as pd

spark = SparkSession.builder.appName('merge all data').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

businessdf = spark.read.csv('../2-cleaned_data/business_cleaned.csv', header=True)
reviewsdf = spark.read.json('../0-raw_data/yelp_academic_dataset_review.json/')
userdf = spark.read.json('../0-raw_data/yelp_academic_dataset_user.json/')

businessdf = businessdf.select('business_id','name','stars','review_count','is_open') \
.withColumnRenamed('name','business_name') \
.withColumnRenamed('stars','business_stars') \
.withColumnRenamed('review_count', 'business_review_count')

reviewsdf = reviewsdf.select('business_id','date','review_id','stars','user_id')
reviewsdf = reviewsdf.withColumnRenamed('stars','review_stars')

joined = businessdf.join(reviewsdf, on='business_id').sort('business_id')

user_df = userdf.select('average_stars','elite','name','review_count','user_id') \
.withColumnRenamed('name','username') \
.withColumnRenamed('review_count','user_review_count')
joined = joined.join(user_df, on='user_id')

joined.toPandas().to_csv('../2-cleaned_data/business_reviews_users_merged.csv')



