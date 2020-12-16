import sys
from pyspark.sql import SparkSession, functions, types
import string, re


spark = SparkSession.builder.appName('wordcount').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

# comments_schema = types.StructType([
#     types.StructField('author', types.StringType()),

# ])


def main(in_directory, out_directory):
    df = spark.read.text(in_directory);
    wordbreak = r'[%s\s]+' % (re.escape(string.punctuation),)  # regex that matches spaces and/or punctuation
    # df = functions.lower(functions.explode(functions.split(df.value, wordbreak)))
    df = df.select(functions.split(df.value, wordbreak).alias('split'))
    df = df.select(functions.explode(df.split).alias('exploded'))
    df = df.select(functions.lower(df.exploded).alias('word'))
    df = df.groupby('word').agg(functions.count(df.word)).withColumnRenamed('count(word)', 'count')
    df = df.sort(df['count'].desc())
    df = df.filter(df.word != '')
    df.show()
    df.write.csv(out_directory, mode='overwrite')


if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)
