#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import typing
from .common import Option, ExceptionOption, Picker, Stop, Help

def pick_method(obj: object, *, allow_none: bool=True, raise_on_help: bool=True) -> callable:
    '''
    pick a method from a obj (`cls` or `self`).
    can use filter to filter

    return `None` if user pick `None`.
    '''
    if obj is None:
        raise ValueError('obj cannot be None')

    methods = []
    for name in dir(obj):
        if not name.startswith('_'):
            attr = getattr(obj, name)
            if callable(attr):
                methods.append((name, attr))

    options = Picker(sep='\n')
    for idx, (name, method) in enumerate(methods):
        doc = getattr(method, '__doc__', '')
        desc = name
        if doc:
            desc += '  (' + doc + ')'
        options.add(Option(desc, [str(idx), name], method))

    if allow_none:
        options.add(Option('None', ['X', 'none'], None))
    options.add(ExceptionOption('Stop', ['S', 'stop'], Stop))
    if raise_on_help:
        options.add(ExceptionOption('Help', ['?', 'H'], Help))
    else:
        options.add(Option('Help', ['?', 'H'], Help))
    return options.pick(None)
