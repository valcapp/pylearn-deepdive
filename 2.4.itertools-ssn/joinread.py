from collections import namedtuple
from itertools import chain, islice, compress
from collections.abc import Callable, Iterable, Iterator
from typing import NamedTuple

import utilparse as prs
import fileread as fr

def unrepeated(items)->Iterable:
    unrepeated = list()
    mask = list()
    for item in items:
        is_unrepeated = item not in unrepeated
        mask.append(item not in unrepeated)
        is_unrepeated and unrepeated.append(item)
    return tuple(unrepeated), tuple(mask)

def combine_extractors(
        fields:Iterable,
        extractors:Iterable,
        mask:Iterable = None
        )->Callable:
    slices_size = tuple(map(len,fields))
    extractors = tuple(extractors)
    mask = tuple(mask) if mask else None
    def extractor(line:Iterable)->Iterator:
        iter_line = iter(line)
        slices = (islice(iter_line, size) for size in slices_size )
        full = chain.from_iterable(map(
            lambda extr, chunk: extr(chunk),
            extractors, slices
        ))
        return compress(full, mask) if mask else full
    return extractor

def combine_parsers(
        tp_name: str,
        ntp_classes: Iterable = tuple(),
        extractors: Iterable = tuple(),
    )->Callable:
    # original fields
    fields_subsets = tuple( ntp._fields for ntp in ntp_classes)
    all_fields = chain.from_iterable( fields_subsets )
    # make named tuple
    fields, mask = unrepeated(all_fields)
    ntp_class = namedtuple(tp_name, fields)
    # make extractor
    extractor = combine_extractors(fields_subsets, extractors, mask)
    # make parser
    parser = prs.make_lineparser(ntp_class, extractor)
    return parser

def combine_lines(tables:Iterable)->Iterator:
    return (
        chain.from_iterable(tables_row)
        for tables_row in zip(*tables) 
    )

def parse_join(tables:Iterable, parser:Callable)->Iterator:
    return prs.parse_lines(
        combine_lines(tables),
        parser
    )

def read_files(
        file_paths:Iterable,
        parser:Callable
        )->Iterator:
    return parse_join(
        map(fr.iter_csv, file_paths),
        parser
    )


# ====================================
#  FROM CONFIG
# ====================================
from constants import FPATH

def from_configs(name:str, configs:Iterable)->Iterator:
    cfgs = tuple(configs)
    file_paths = ( cfg.get(FPATH) for cfg in cfgs )
    parser = combine_parsers(
        tp_name = name,
        ntp_classes = map(fr.make_namedtuple_from_config, cfgs),
        extractors = map(fr.make_extractor_from_config, cfgs)
    )
    return read_files(file_paths, parser)

# ====================================
#  OBJECT ORIENTED
# ====================================
class Joinreader():
    
    def __init__(self, name:str, readers:Iterable)->None:
        self.name = name
        self._readers = tuple(readers)
        self._fields = None
        self._cast_types = None
        self._Tupleclass = None

    @property
    def fields(self)->dict:
        if self._fields is None:
            all_fields = sum((
                reader.Tupleclass._fields
                for reader in self._readers
            ),tuple())
            # remove repetiitions by overwriting repeated keys
            self._fields = {
                fld: idx for idx, fld
                in enumerate(all_fields)
            }
        return self._fields

    @property
    def Tupleclass(self)->NamedTuple:
        if self._Tupleclass is None:
            fields = tuple(self.fields.keys())
            self._Tupleclass = namedtuple(self.name, fields)
        return self._Tupleclass
        
    def extract_values(self, iterable: Iterable)->tuple:
        data = tuple(iterable)
        return tuple(map(
            lambda idx: data[idx],
            self.fields.values()
        ))

    @property
    def cast_types(self)->tuple:
        if self._cast_types is None:
            all_cast_types = sum((
                reader.cast_types
                for reader in self._readers
            ), tuple())
            self._cast_types = self.extract_values(all_cast_types)
        return self._cast_types
        
    def __iter__(self)->tuple:
        rows = zip(*tuple(
            iter(reader) for reader in self._readers
        ))
        for reads in rows:
            row = self.extract_values(
                sum(reads, tuple())
            )
            yield self.Tupleclass(*tuple(
                cast(val) for val, cast
                in zip(row, self.cast_types)
            ))
            
    