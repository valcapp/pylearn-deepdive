from collections import namedtuple
from collections.abc import Iterable, Iterator
from typing import NamedTuple
import datetime as dt

def read_line(line:str)->list:
    return line.strip('\n').split(',')

def parse_date(str_date:str)->dt.date:
    return dt.datetime.strptime(str_date, "%m/%d/%Y").date()

# example = (4006478550, 'VAD7274', 'VA', 'PAS', '10/5/2016', 5, '4D', 'BMW', 'BUS LANE VIOLATION',)
dtypes =    (int,       str,        str,  str,  parse_date,  int, str,  str,     str )
def type_cast(data: Iterable)->Iterator:
    return ( dtype(item) for dtype, item in zip(dtypes, data) )

def make_namedtuple_from_header( tuple_name:str, header:str)->NamedTuple:
    field_names = ( 
        name.replace(' ','_').lower()
        for name in read_line(header)
    )
    return namedtuple(tuple_name, field_names)

def parse_tickets(
        lines: Iterable,
        tuple_class: NamedTuple,
        )->Iterator:
    return (
        tuple_class(
            *type_cast(
                read_line(line)
            )
        ) for line in lines
    )

def count_in_field(tickets: Iterator, field_name: str)->dict:
    count = {}
    for ticket in tickets:
        field_value = getattr(ticket, field_name)
        count[field_value] = count.get(field_value, 0) + 1
    return count

def sort_dict(dct:dict)->dict:
    dict(sorted(
        dct.items(),
        key = lambda item: item[1],
        reverse= True
    ))

def count_tickets_by_make(
        file_path: str,
        *, sort = True
    )->dict:
    with open(file_path) as file:
        Ticket = make_namedtuple_from_header('Ticket', next(file))
        tickets = parse_tickets(file, Ticket)
        count = count_in_field(tickets, 'vehicle_make')
    count = sort and sort_dict(count) or count
    return count

if __name__ == '__main__':
    count_by_maker = count_tickets_by_make('nyc_parking_tickets_extract.csv')
    [print(f'{maker}\t{times}') for maker, times in count_by_maker.items()]
