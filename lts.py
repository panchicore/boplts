#!/ usr/bin/python

import os
import uuid

import click
from urlparse import parse_qs


@click.command()
@click.argument('query')
@click.option('--output_file', default="/tmp/{0}".format(uuid.uuid4()))
def search(query, output_file):
    """
    take query from http://54.158.101.33:8080/bopws/swagger/#!/default/export
    python lts.py "http://54.158.101.33:8080/bopws/tweets/export?q.time=*&q.geo=%5B-90%2C-180%20TO%2090%2C180%5D&q.text=test&q.user=panchicore"
    python lts.py "q.time=%5B2013-03-01%20TO%202013-04-01T00%3A00%3A00%5D&q.geo=%5B-90%2C-180%20TO%2090%2C180%5D&q.text=test&q.user=panchicore&d.docs.limit=100'"
    params = {
        'd.docs.limit': ['100'],
        'q.geo': ['[-90,-180 TO 90,180]'],
        'q.text': ['test'],
        'q.time': ['[2013-03-01 TO 2013-04-01T00:00:00]'],
        'q.user': ['panchicore']
    }
    """

    # if query contains more than url params.
    if query.count("?") > 0:
        query = query.split("?")[1]

    params = parse_qs(query)

    text = None
    if params.get('q.text'):
        text = params.get('q.text')[0]

    time_range = None
    if params.get('q.time'):
        time_range = params.get('q.time')[0]
        if time_range == "*":
            time_range = "2013-01-01 TO 2013-01-01"
        else:
            # TODO: better parse with dateutils
            time_range = time_range.replace("[", "").replace("]", "")[:24]

    user_name = None
    if params.get('q.user'):
        user_name = params.get('q.user')[0]

    geo = None
    if params.get('q.geo'):
        geo = params.get('q.geo')[0]

    limit = None
    if params.get('d.docs.limit'):
        limit = params.get('d.docs.limit')[0]

    command_params = {
        "sql_query": "text like '%{0}%'".format(text),
        "time_range": time_range,
        "output_file": output_file
    }

    command = 'spark-submit --packages com.databricks:spark-avro_2.10:2.0.1,com.databricks:spark-csv_2.11:1.3.0 ' \
              'search.py "{sql_query}" "{time_range}" {output_file}  ' \
              .format(**command_params)

    click.echo("-" * 100)
    click.echo(command)
    click.echo("-" * 100)

    os.system(command)

    click.echo("-" * 100)
    click.echo("Collect all data with the following command:")
    click.echo("cat {}/*".format(output_file))

if __name__ == '__main__':
    search()