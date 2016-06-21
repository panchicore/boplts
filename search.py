# pyspark search.py "text like '%hello%'" "2013-01-01 TO 2013-01-02" test.json  --packages com.databricks:spark-avro_2.10:2.0.1,com.databricks:spark-csv_2.11:1.3.0

import sys, time, os
from datetime import datetime
from dateutil.rrule import rrule, DAILY
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.conf import SparkConf

LTS_BASE_DIR = os.environ.get("LTS_BASE_DIR", "fs")
LTS_RESULTS_DIR = os.environ.get("LTS_RESULTS_DIR", "./output")

start_time = time.time()

query = sys.argv[1] or "user_name = 'hello' and text like '%world%'"
date_range = sys.argv[2] or "2013-01-01 TO 2013-01-02"
output = sys.argv[3] or "output_files"

_from = datetime.strptime(date_range.split(" TO ")[0], "%Y-%m-%d").date()
_to = datetime.strptime(date_range.split(" TO ")[1], "%Y-%m-%d").date()
dirs = list(rrule(freq=DAILY, dtstart=_from, until=_to))

sc = SparkContext("local", "LTS")
sqlContext = SQLContext(sc)

data_files = []
for dir in dirs:
    data_files.append(
        os.path.join(LTS_BASE_DIR, dir.strftime("%Y/%m/%d"), "*.avro")
    )
    # TODO: not existing dir paths will generate java.io.IOException
    # for now use create_dirs.py to make entire folder structure.

df = sqlContext.read.format("com.databricks.spark.avro").load(data_files)

output_format = "csv"
if output_format == "json":
    df.filter(query).write.mode('append').json(output)
else:
    df.filter(query).write\
        .format("com.databricks.spark.csv")\
        .option("header", "true")\
        .save(output)

print time.time() - start_time, 'secs'