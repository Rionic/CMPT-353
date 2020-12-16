import sys
from pyspark.sql import SparkSession, functions, types
import re

spark = SparkSession.builder.appName('wikipedia popular').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+


pages_schema = types.StructType([
    types.StructField('language', types.StringType()),
    types.StructField('title', types.StringType()),
    types.StructField('requests', types.LongType()),
    types.StructField('bytes', types.LongType()),
])


def main(in_directory, out_directory):
    pages = spark.read.csv(in_directory, sep=' ', schema=pages_schema).withColumn('filename', functions.input_file_name())

    pages = pages.filter(pages['language']=='en')
    pages = pages.filter(pages['title']!='Main_Page')
    pages = pages.filter(pages['title'].startswith('Special:')==False)

    path_to_hour = functions.udf(converter, returnType=types.StringType())

    pages = pages.withColumn('time', path_to_hour(pages.filename))
    pages = pages.drop('language', 'bytes', 'filename')

    pages = pages.cache()
    top_pages = pages.groupby(pages.time).agg(functions.max(pages.requests)).withColumnRenamed('max(requests)', 'requests')

    joined_pages = pages.join(top_pages, on=['time', 'requests'])
    joined_pages = joined_pages.sort('time', 'title')
    joined_pages = joined_pages.select('time', 'title', 'requests')

    joined_pages.write.csv(out_directory, mode='overwrite')
    
def converter(pathname):
    return re.search('\d+\-[0-9]{2}', pathname).group(0)

if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)
