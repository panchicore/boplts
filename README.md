##LTS
Long time storage for the billion object platform.
After enrich tweets Kafta will be writing the files into this machine in a simple time sorted/organized structure:

`<LTS_BASE_DIR>/<YEAR>/<MONTH>/<DAY>/*.avro`

##Filter and Export Script
This is a Spark program to filter/export tweets using a distributed collection of data organized into a Tweet DataFrame.

This search is done by creating the DataFrame on-the-fly for the avro files stored in the path provided by parsing the date range to the folder structure.

set enviroment `LTS_BASE_DIR` to the path where LTS is located and execute the script with the following parameters:

`pyspark search.py "SQL" "RANGE" OUTPUT_RESULTS_PATH --packages com.databricks:spark-avro_2.10:2.0.1`

for instance: search between 2013-1-1 and 2013-2-1 tweets that contains "hello" in text and export results into /tmp/hello:

`pyspark search.py "text like '%hello%'" "2013-1-1 TO 2013-2-1" /tmp/hello  --packages com.databricks:spark-avro_2.10:2.0.1`

results will be stored in JSON format.

Bellow the explanation for each part of the command:

####pyspark
The Spark Python API
\#TODO: use sbin/spark-submit

####search.py
Loads the arguments and starts the Spark SQL context.

####SQL
[Spark SQL](http://spark.apache.org/sql/) lets you query structured data inside Spark programs, execute SQL queries written using either a basic SQL syntax:

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

#Swagger export request URL
This command receives the swagger request URL to export the data as Sorl does.
`python lts.py "http://54.158.101.33:8080/bopws/tweets/export?q.time=*&q.geo=%5B-90%2C-180%20TO%2090%2C180%5D&q.text=test&q.user=panchicore"`
Output will be a Sorl-style CSV file.

## Benchmark
on 300 millions tweets, search a keyword takes 15 minutes.
machine: 2.9 Intel Core i7, 8G RAM, SSD disk.
ram used: 1G and one complete CPU core. *No tuned enviroment.*

##Disk capacity and Redundancy

- 1M tweets = 85M // *compressed avro file with id,created_at,coord,user_name and text*
- \#TODO: Machine specs here.
- \#TODO: Disks specs here.
- RAID is a good options to have mirrored the stored data.

## Tuning
`--driver-memory 2g`

[Tuning spark guide](https://spark.apache.org/docs/1.6.1/tuning.html)

