import csv
    
# parsing
def parse_rows(rows, row_parser):
    return (
        row_parser(row)
        for row in rows
    )

# filtering
def filter_rows(rows, filter_func):
    return (
        row for row in rows
        if filter_func(row)
    )

# yield from file
def csv_yielder(fpath, skip_header=True,
        row_parser=None,
        row_filter=None):
    with open(fpath) as file:
        dialect = csv.Sniffer().sniff(file.read(2000))
        file.seek(0)
        rows = csv.reader(file, dialect=dialect)
        if skip_header:
            next(rows)
        if row_parser is not None:
            rows = parse_rows(rows, row_parser)
        if row_filter is not None:
            rows = filter_rows(rows, row_filter)
        yield from rows