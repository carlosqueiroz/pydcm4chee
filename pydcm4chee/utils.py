# -*- coding: utf-8 -*-

def get_from_nested_dict(input_dict, key_list, silence_exceptions=True):
    """
    Utility funcion to quickly get to an element inside a nested dict.
    Based on: http://stackoverflow.com/a/14692747
    """
    try:
        return reduce(lambda d, k: d[k], key_list, input_dict)
    except (TypeError, IndexError, KeyError) as e:
        if silence_exceptions:
            return None
        else:
            raise e
