import csv
from functools import wraps
from contextlib import closing as ctx_closing

# priming coroutines
def primed_coroutine(coro):
    @wraps(coro)
    def decored(*args, **kwargs):
        gen = coro(*args, **kwargs)
        next(gen)
        return gen
    return decored

def broadcast_data_to(data, coro):
    with ctx_closing(coro()) as pipe:
        for row in data:
            pipe.send(row)

@primed_coroutine
def save_sink(fpath, headers=None):
    with open(fpath, 'w', newline='') as file:
        writer = csv.writer(file)
        if headers is not None:
            writer.writerow(headers)
        while True:
            row = yield
            writer.writerow(row)

@primed_coroutine
def coro_filter(row_filter, target):
    while True:
        row = yield
        if row_filter(row):
            target.send(row)

@primed_coroutine
def coro_save(save_path, headers=None, row_filter=None):
    target = save_sink(save_path, headers)
    if row_filter is not None:
        target = coro_filter(row_filter, target)
    while True:
        row = yield
        target.send(row)

def make_sinksave(save_path, headers=None, row_filter=None):
    pipeline = lambda: coro_save(save_path, headers, row_filter )
    def broadcast(data):
        broadcast_data_to(data, pipeline)
    return broadcast