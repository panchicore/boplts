##BOP Long Term Storage
Put file into this structure:

`<LTS_BASE_DIR>/<year>/<month>/<day>/*.avro`


##Disk capacity

1 million tweets = 85M
*compressed avro file with id,created_at,coord,user_name and text*

##Filter and Export Script
This is a Spark program to filter/export tweets using a distributed collection of data organized into a Tweet DataFrame.

This search is done by creating the DataFrame on-the-fly for the avro files stored in the path provided by parsing the date range to the folder structure.

set enviroment `LTS_BASE_DIR` to the path where LTS is located and execute the script with the following parameters:

`pyspark search.py "SQL" "RANGE" OUTPUT_RESULTS_PATH --packages com.databricks:spark-avro_2.10:2.0.1`

for instance, search between 2013-1-1 and 2013-2-1 tweets that contains "hello" in the text and export results to /tmp/hello:

`pyspark search.py "text like '%hello%'" "2013-1-1 TO 2013-2-1" /tmp/hello  --packages com.databricks:spark-avro_2.10:2.0.1`

results will be stored in JSON format.

Bellow the explanation for each part of the command:

####pyspark
The Spark Python API
\#TODO: use sbin/spark-submit

####search.py
Loads the arguments and starts the Spark SQL context.

####SQL
Spark SQL lets you query structured data inside Spark programs, execute SQL queries written using either a basic SQL syntax:

`"user_name = 'hello' AND text like '%world%'"`

`"text like '%soccer%' OR text like '%football%'"`

####RANGE and OUTPUT_RESULTS_PATH
Range is a date-to-date string to filter the results what are already ordered by the folder structure, it inserts to the DataFrame all avro files contained in those folder paths.

The script will parse the given dates range into multiple paths in the folder structure:

For instance: 2013-01-01 TO 2014-01-01 will search on:

`<LTS_BASE_DIR>/2013/01/01/*.avro`
`<LTS_BASE_DIR>/2013/01/02/*.avro`
`<LTS_BASE_DIR>/2013/01/03/*.avro`
`...`
`<LTS_BASE_DIR>/2013/02/01/*.avro`
`...`
`<LTS_BASE_DIR>/2014/01/01/*.avro`

Results will be store in JSON format and splited in multiple parts, to get a single file aggregate them with `cat /tmp/hello/* > hello.json`

####--packages
- `com.databricks:spark-avro_2.10:2.0.1` is a required dependencies for Spark to work with avro files.

##Requirements
- install java spark and pyspark bindings
- install requirements.txt

## Benchmark
on 300 millions tweets, search a keyword takes 15 minutes.

## Tuning
`--driver-memory 2g`
[Tuning spark guide](https://spark.apache.org/docs/1.6.1/tuning.html)

