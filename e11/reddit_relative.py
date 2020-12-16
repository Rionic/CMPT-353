import sys
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('reddit relative scores').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

comments_schema = types.StructType([
    # types.StructField('archived', types.BooleanType()),
    types.StructField('author', types.StringType()),
    # types.StructField('author_flair_css_class', types.StringType()),
    # types.StructField('author_flair_text', types.StringType()),
    # types.StructField('body', types.StringType()),
    # types.StructField('controversiality', types.LongType()),
    # types.StructField('created_utc', types.StringType()),
    # types.StructField('distinguished', types.StringType()),
    # types.StructField('downs', types.LongType()),
    # types.StructField('edited', types.StringType()),
    # types.StructField('gilded', types.LongType()),
    # types.StructField('id', types.StringType()),
    # types.StructField('link_id', types.StringType()),
    # types.StructField('name', types.StringType()),
    # types.StructField('parent_id', types.StringType()),
    # types.StructField('retrieved_on', types.LongType()),
    types.StructField('score', types.LongType()),
    # types.StructField('score_hidden', types.BooleanType()),
    types.StructField('subreddit', types.StringType()),
    # types.StructField('subreddit_id', types.StringType()),
    # types.StructField('ups', types.LongType()),
    #types.StructField('year', types.IntegerType()),
    #types.StructField('month', types.IntegerType()),
])


def main(in_directory, out_directory):
    comments = spark.read.json(in_directory, schema=comments_schema)
    
    # TODO
    groups = comments.groupby('subreddit')
    avg = groups.agg(functions.avg(comments['score']))
    avg = avg.filter(avg['avg(score)'] > 0)
    avg = avg.cache()

    joined_data = comments.join(functions.broadcast(avg), on=['subreddit'])
    joined_data = joined_data.cache()
    joined_data = joined_data.withColumn('rel_score',  joined_data['score'] / joined_data['avg(score)'])
    joined_data = joined_data.cache()

    groups = joined_data.groupby('subreddit')
    max_rel_score = groups.agg(functions.max(joined_data['rel_score'])).withColumnRenamed('max(rel_score)', 'rel_score')
    max_rel_score = max_rel_score.cache()

    best_author = joined_data.join(functions.broadcast(max_rel_score), on=['rel_score']).drop(max_rel_score.subreddit)
    best_author = best_author.cache()
    best_author = best_author.drop('avg(score)', 'score')
    best_author = best_author.cache()
    best_author = best_author.select('subreddit', 'author', 'rel_score')

    best_author.write.json(out_directory, mode='overwrite')


if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)
