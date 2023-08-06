import os
import csv
import StringIO





class CSVRenderer(object):
    def __init__(self, info):
        pass

    def __call__(self, value, system):

        resp = system['request'].response
        resp.content_type = 'text/csv'
        resp.content_disposition = 'attachment;filename="report.csv"'

        if type(value) == str:
            return value

        formatted_output = StringIO.StringIO()
        writer = csv.writer(formatted_output, delimiter=',', quoting=csv.QUOTE_ALL)

        writer.writerow(value['header'])
        writer.writerows(value['rows'])

        return formatted_output.getvalue()
