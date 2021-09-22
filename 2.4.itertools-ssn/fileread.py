
from collections.abc import Callable, Iterable, Iterator
from collections import namedtuple
import os
import csv
from typing import NamedTuple
import utilparse as prs
from itertools import compress

def iter_csv(file_path:str, skip_header=True)->Iterator:
    with open(file_path, 'r', newline='') as file:
        skip_header and next(file)
        yield from csv.reader(file, delimiter=',', quotechar='"')

def get_filename(file_path:str)->str:
    return os.path.splitext(
        os.path.basename(file_path)
    )[0]

def read_file(
        file_path: str,
        parser: Callable = lambda x: x,
    )->Iterator:
    return prs.parse_lines(iter_csv(file_path), parser)


# ====================================
#  FROM CONFIG
# ====================================

from constants import (
    FPATH, # file path
    TPNAME, # tuplename
    TPFIELDS, # tuplename
    DTYPES, # data types
    MASK, # bool filter to compress imputs
)
def make_namedtuple_from_config(
        cfg:dict, name:str = None,
        fields:Iterable=None)->NamedTuple:
    tuplename = name or cfg.get(TPNAME, None) \
        or prs.std_tuplename(get_filename(cfg.get(FPATH)))
    tuplefields = fields or cfg.get(TPFIELDS, None) \
        or map(
            prs.std_fieldname,
            next(iter_csv(
                cfg.get(FPATH),
                skip_header=False
            ))
        )
    return namedtuple(tuplename, tuplefields)

def make_extractor_from_config(cfg:dict)->Callable:
    return prs.make_extractor(
        dtypes = cfg.get(DTYPES, None),
        mask = cfg.get(MASK, None)
    )

def make_parser_from_config(cfg:dict)->Callable:
    ntp_class = make_namedtuple_from_config(cfg)
    extractor = make_extractor_from_config(cfg)
    return prs.make_lineparser(ntp_class, extractor)

def from_config(cfg:dict)->Iterator:
    file_path = cfg.get(FPATH)
    parser = make_parser_from_config(cfg)
    return read_file(file_path, parser)


# ====================================
#  OBJECT ORIENTED
# ====================================

class Filereader():
    def __init__(self, file_path:str, cast_types:tuple)->None:
        self.file_path = file_path
        self.cast_types = cast_types
        self._Tupleclass = None
    
    @property
    def Tupleclass(self)->NamedTuple:
        if self._Tupleclass is None:
            header = next(iter_csv(self.file_path, skip_header=False))
            tuplename = prs.std_tuplename(prs.get_filename(self.file_path))
            self._Tupleclass = namedtuple(tuplename,
                tuple(map(prs.std_fieldname, header))
            )
        return self._Tupleclass
    
    def __iter__(self)->Iterator:
        for row in iter_csv(self.file_path):
            yield self.Tupleclass(*tuple(
                cast(val) for val, cast
                in zip(row, self.cast_types)
            ))


