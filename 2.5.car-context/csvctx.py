
import csv
from collections import namedtuple
from collections.abc import Iterator, Iterable, Callable
from typing import TextIO, NamedTuple

import os
def fpath_to_classname(fpath:str)->str:
    words = os.path.splitext(os.path.basename(fpath))[0]\
        .strip().replace(' ','_').split('_')
    return ''.join(word.capitalize() for word in words)

def infer_dialect(fpath:str)->csv.Dialect:
    with open(fpath) as file:
        sample = file.read(500)
        dialect = csv.Sniffer().sniff(sample, delimiters=",;")
    return dialect

# can be iterated more than once
class CsvContext:
    def __init__(self, fpath:str, tp_name:str=None, dialect:csv.Dialect=None):
        self._fpath = fpath
        self._file = None
        self._tp_name = tp_name or fpath_to_classname(fpath)
        self._dialect = dialect or infer_dialect(fpath)
        self._ntp_class = None
    
    @property
    def ntp_class(self)->NamedTuple:
        if self._ntp_class is None:
            with open(self._fpath) as file:
                header = next(self.raw_lines(file))
                standardize = lambda name: str(name).strip().lower().replace(' ','_')
                self._ntp_class = namedtuple(self._tp_name, map(standardize, header))
        return self._ntp_class
    
    def raw_lines(self, file:TextIO)->Iterator:
        return csv.reader(file, dialect=self._dialect)
    
    def __enter__(self)->Iterator:
        self._file = open(self._fpath)
        return iter(self)
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._file.close()
        return False
    
    def __iter__(self)->Iterator:
        lines = self.raw_lines(self._file)
        next(lines) # skip header
        return ( self.ntp_class(*line) for line in lines)

# disposable 
class CsvReader:
    def __init__(self, fpath:str, tp_name:str=None, dialect:csv.Dialect=None):
        self._fpath = fpath
        self._tp_name = tp_name or fpath_to_classname(fpath)
        self._dialect = dialect or infer_dialect(fpath)
    
    def __enter__(self)->Iterator:
        self._file = open(self._fpath)
        self._reader = csv.reader(self._file, self._dialect)
        standardize = lambda name: str(name).strip().lower().replace(' ','_')
        self.ntp_class = namedtuple(self._tp_name,
            map(standardize, next(self._reader))
        )
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._file.close()
        return False
    
    def __iter__(self)->Iterator:
        return self
    
    def __next__(self):
        if self._file.closed:
            raise StopIteration
        return self.ntp_class(*next(self._reader))

from contextlib import contextmanager

@contextmanager
def read_csv(fpath:str, tp_name:str=None, dialect:csv.Dialect=None):
    try:
        # setup reader
        file = open(fpath)
        dialect = dialect or csv.Sniffer().sniff(file.read(500))
        file.seek(0)
        reader = csv.reader(file, dialect)
        #setup parser
        tp_name = tp_name or fpath_to_classname(fpath)
        standardize = lambda name: str(name).strip().lower().replace(' ','_')
        ntp_class = namedtuple(tp_name,
            map(standardize, next(reader))
        )
        yield ( ntp_class(*line) for line in reader)
    finally:
        file.close()

    
if __name__ == '__main__':
    from itertools import islice, product
    
    def print_head(rows:Iterable, n:int=5)->None:
        [print(row) for row in islice(rows, 5)]
    
    for ctx, fpath in product(
            (CsvReader, read_csv,),
            ('data/cars.csv', 'data/personal_info.csv',)
        ):
        with ctx(fpath) as rows:
            print(f"\n\n{ctx.__name__}({fpath}):\n{50*'-'}")
            print_head(rows)