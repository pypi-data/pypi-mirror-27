import csv
from io import StringIO


def write_row(row):
    """Change an iterable to a CSV string, for things such as file writes."""
    csv_out = StringIO()
    csv.writer(csv_out).writerow(row)
    return csv_out.getvalue()
