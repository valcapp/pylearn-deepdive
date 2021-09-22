
import datetime as dt
from collections.abc import Callable, Iterable, Iterator
from typing import NamedTuple
from itertools import compress, groupby
from itertools import groupby
from collections import Counter

def std_fieldname(name:str)->str:
    return str(name).strip().lower().replace(" ","_")

def std_tuplename(name:str)->str:
    return ''.join(
        piece.capitalize() for piece
        in std_fieldname(name).split('_')
    )

def iso_datetime(str_date:str)->dt.date:
    return dt.datetime.fromisoformat(str(str_date).rstrip('Z'))

def extract(
        line:Iterable,
        dtypes: Iterable = None,
        mask: Iterable = None
    )->Iterable:
    masked = mask \
        and compress(line, mask) \
        or line
    typed = dtypes \
        and map(
            lambda dtype, val: dtype(val),
            dtypes, masked
        ) \
        or masked
    return typed

def make_extractor(
        dtypes: Iterable = None,
        mask: Iterable = None
    )->Callable:
    dtypes = tuple(dtypes) if dtypes else None
    mask = tuple(mask) if mask else None
    def extractor(line: Iterable)->Iterable:
        return extract(line, dtypes, mask)
    return extractor

def parse_line(
        line: Iterable, 
        ntp_class: NamedTuple = lambda *args: tuple(args),
        extractor: Callable = lambda x: x,
    )->NamedTuple:
    return ntp_class(*extractor(line))

def make_lineparser(
        ntp_class: NamedTuple = lambda *args: tuple(args),
        extractor: Callable = lambda x: x
        )->Callable:
    def lineparser(line:Iterable):
        return parse_line(line, ntp_class, extractor)
    return lineparser

def parse_lines(
        lines: Iterable,
        parser: Callable = lambda x: x,
    )->Iterator:
    return map(parser, lines)

def filtered(lines:Iterable, key:Callable = lambda x: x)->Iterator:
    return filter(key, lines)

def filter_nonstale(
        lines:Iterable,
        threshold: dt.datetime = None,
        time_col:str = 'last_updated',
    )->Iterator:
    return filtered(lines,
        key = lambda line: \
            getattr(line, time_col) >= threshold
    ) if threshold else lines

def count_x_by_y(lines:Iterable, x:str, y:str):
    sorted_data = sorted(lines, key= \
        lambda line: (getattr(line, y), getattr(line, x),)
    )
    grouped_by_y = groupby(sorted_data, key=lambda line: getattr(line, y))
    counts = {
        y_key: Counter(
            getattr(line, x)
            for line in y_data
        )
        for y_key, y_data in grouped_by_y
    }
    return {
        key: cnt.most_common()
        for key, cnt in counts.items()
    }