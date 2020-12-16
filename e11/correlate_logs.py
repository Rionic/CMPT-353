import sys
from pyspark.sql import SparkSession, functions, types, Row
from pprint import pprint
import re
import math

spark = SparkSession.builder.appName('correlate logs').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

line_re = re.compile(r"^(\S+) - - \[\S+ [+-]\d+\] \"[A-Z]+ \S+ HTTP/\d\.\d\" \d+ (\d+)$")


def line_to_row(line):
    """
    Take a logfile line and return a Row object with hostname and bytes transferred. Return None if regex doesn't match.
    """
    m = line_re.match(line)
    if m:
        return Row(hostname=m.group(1), bytes=m.group(2))
    else:
        return None


def not_none(row):
    """
    Is this None? Hint: .filter() with it.
    """
    return row is not None


def create_row_rdd(in_directory):
    log_lines = spark.sparkContext.textFile(in_directory)
    # pprint(log_lines.take(5))
    rows = log_lines.map(line_to_row)
    rows = rows.filter(not_none)
    # TODO: return an RDD of Row() objects
    return rows
def main(in_directory):
    logs = spark.createDataFrame(create_row_rdd(in_directory))
    # TODO: calculate r.
    groups = logs.groupby(logs.hostname)
    hosts1 = groups.agg({'bytes': 'count'})
    hosts1 = hosts1.cache()
    hosts2 = groups.agg({'bytes': 'sum'})
    hosts2 = hosts2.cache()
    hosts = hosts1.join(hosts2, on='hostname')
    hosts.show()
    groups = hosts.groupby().agg(
        functions.count(hosts.hostname),
        functions.sum(hosts['count(bytes)']),
        functions.sum(functions.pow(hosts['count(bytes)'], 2)),
        functions.sum(hosts['sum(bytes)']),
        functions.sum(functions.pow(hosts['sum(bytes)'], 2)),
        functions.sum(hosts['count(bytes)']*hosts['sum(bytes)'])
        )

    groups.show()

    # n = logs.count()
    # x = functions.sum(hosts['count(bytes)']).first()
    # x2 = functions.sum(functions.pow(hosts['count(bytes)'], 2)).first()
    # y = functions.sum(hosts['sum(bytes)']).first()
    # y2 = functions.sum(functions.pow(hosts['sum(bytes)'], 2)).first()
    # xy = functions.sum(hosts['count(bytes)'] * hosts['sum(bytes)']).first()

    a = groups.first()
    n = a[0]
    x = a[1]
    x2 = a[2]
    y = a[3]
    y2 = a[4]
    xy = a[5]

    r = (n*xy - x*y)/(math.sqrt(n*x2 - x**2) * math.sqrt(n*y2 - y**2))
    print("r = %g\nr^2 = %g" % (r, r**2))


if __name__=='__main__':
    in_directory = sys.argv[1]
    main(in_directory)
