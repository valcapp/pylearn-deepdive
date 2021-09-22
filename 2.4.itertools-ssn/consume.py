
import utilparse as prs
import fileread as fr
import joinread as jr
import datetime as dt

from collections.abc import Iterable, Iterator, Callable
from constants import DTYPES, FPATH
from filescfg import configs

from itertools import islice

def print_head(iterable:Iterable, n_lines:int=5)->None:
    for row in islice(iterable, n_lines):
        print(row)

def inspect_each_file(configs:tuple)->None:
    """Goal 1"""
    for cfg in configs:
        reader = fr.from_config(cfg)
        print_head(reader)

    #  Obejct Oriented
    # for cfg in configs:
    #     file_path = cfg.get(FPATH)
    #     cast_types = cfg.get(DTYPES)
    #     reader = fr.Filereader(file_path, cast_types)
    #     for row in islice(reader, 5):
    #         print(row)

def inspect_joined_files(configs:tuple)->None:
    """Goal 2"""
    reader = jr.from_configs('Employee', configs)
    print_head(reader)
    # Obj. Oriented
    # single_readers = (
    #     fr.Filereader(cfg.get(FPATH), cfg.get(DTYPES))
    #     for cfg in configs
    # )
    # employees = jr.Joinreader('Employee', single_readers)
    # for empl in islice(employees, 5):
    #     print(empl)

def inspect_nonstale(configs:tuple)->None:
    """Goal 3"""
    reader = jr.from_configs('Employee', configs)
    nonstale = prs.filter_nonstale(reader, dt.datetime(day=1, month=3, year=2017))
    print_head(nonstale, 10)
    
def inspect_carmake_by_gender(configs:tuple)->None:
    """Goal 4"""
    reader = jr.from_configs('Employee', configs)
    nonstale = prs.filter_nonstale(reader, dt.datetime(day=1, month=3, year=2017))
    print(prs.count_x_by_y(nonstale,'vehicle_make', 'gender'))

if __name__ == '__main__':
    inspect_each_file(configs)
    inspect_joined_files(configs)
    inspect_nonstale(configs)
    inspect_carmake_by_gender(configs)