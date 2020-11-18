from collections import OrderedDict
from typing import Any


def recursively_assert_values(exp: Any, o: Any, s: int = 0, parent: str = ''):
    if type(exp) != type(o):
        raise AssertionError(
            f'{parent or "root"} Object type mismatch'
            f'\nExpected type of {type(exp)}, got type of {type(o)}'
            f'\n{"*" * 50}'
            f'\nGot data: \n'
            f'{o}'
            f'\n\n'
            f'Expected'
            f'\n\n'
            f'{exp}\n'
        )

    if isinstance(exp, dict) or isinstance(exp, OrderedDict):
        for k, v in exp.items():
            recursively_assert_values(exp.get(k), o.get(k), s + 4, f'{parent}["{k}"]')
    elif isinstance(exp, list):
        for i, item in enumerate(exp):
            recursively_assert_values(exp[i], o[i], s + 4, f'{parent}[{i}]')
    else:
        assert exp == o, f'{parent} failed, \nExpected {exp}, \nBut got {o}'
