class WrongKey(Exception):
    pass

class WrongType(Exception):
    pass

def validate(data:dict, templ:dict, root:str=''):
    # where_at = root and f' at {root}' or ''
    try:
        # check keys
        data_keys = set(data.keys())
        templ_keys = set(templ.keys())
        compare_keys(data_keys, templ_keys, root, f"Unexpected keys: ")
        compare_keys(templ_keys, data_keys, root, f"Missing keys: ")
        # check values
        for key, dtype in templ.items():
            val = data[key]
            # if dtype is dictionary
            if isinstance(dtype, dict):
                if not isinstance(val, dict):
                    raise WrongType(f'Wrong type for key {root}.{key}')
                else:
                    is_child_valid, whats_wrong = validate(val, dtype, root+'.'+key)
                    if not is_child_valid:
                        return False, whats_wrong
            # if dtype is actual type
            else:
                if not isinstance(val, dtype):
                    raise WrongType(f'Wrong type for key {root}.{key}')
        return True, ''
    except (WrongType, WrongKey) as exc:
        return False, exc


def compare_keys(set1:set, set2:set, root:str='', msg:str=''):
    diff = set1 - set2
    if diff:
        raise WrongKey(msg+\
            ','.join(
                root+'.'+key
                for key in diff
            )
        )

from example import template, samples

if __name__ == '__main__':
    for name, sample in samples.items():
        is_ok, err = validate(sample, template)
        print(f'\nIs {name} ok?', is_ok)
        err and print(err)