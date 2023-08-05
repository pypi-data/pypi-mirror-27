#!/usr/bin/env
# coding=utf-8

from __future__ import print_function

import os
import atexit
import logging
from time import time
from traceback import print_exc

from texttable import Texttable

logging.basicConfig(format='[%(levelname)s] %(message)s')

class _bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

_, _width = os.popen('stty size', 'r').read().split()
_table = Texttable(int(_width))
_table.header(["func", "time(s)", "result", "expect", "status"])
_table.set_cols_dtype(['t','f','t','t','t'])

def _print():
    # draw table
    result = _table.draw()
    result = result.replace(u'√', _bcolors.OKGREEN + u'√' + _bcolors.ENDC).replace(u'×', _bcolors.FAIL + u'×' + _bcolors.ENDC)
    print(result)
    # statistic
    if _total == 0:
        print(_bcolors.WARNING + u'0 test' + _bcolors.ENDC)
    elif _fail + _error == 0 :
        print('all %d test(s) passed' % _total)
    else:
        print('total:%d, passed:%d, fail:%d, error:%d' % (_total, _total - _fail - _error, _fail, _error))


atexit.register(_print)

_total = 0
_fail = 0
_error = 0


def dump_args(*args, **kw):
    return ', '.join(map(repr, args) + ["%s=%s"%(str(k), repr(v)) for k,v in kw.items()])

def test(func, in_and_out, summary=None, unpack=True):
    """call a function and assert its return value 

    func can take arbitrary arguments

    Arguments:
        func {callable} -- the function to be tested
        in_and_out {list} -- every element is a 2-tuple (args, expected) or a triple: (args, kw, expected)
            args {a single value or a tuple} -- more than one argument should be provided in form of tuple
                if args is a tuple and unpack is True, then func will be invoked as func(*args) otherwise as func(args)
                so if func takes only a tuple, then set unpack to False
            kw {dict, optional} -- keywords arguments passed to func
            expected {a single value or a tuple} -- expected valued returned from func

    Keyword Arguments:
            summary {str} -- summary to display (default: None)
            unpack {boolean} -- whether to unpack tuple arguments (default: True)
    """

    global _total, _fail, _error
    for case in in_and_out:
        row = []
        kw = {}
        _total += 1
        if len(case)==2:
            arg, exp = case
        elif len(case)==3:
            arg, kw, exp = case
        else:
            # todo
            logging.error('test data could not be recognized: %s' % case)
            _error += 1
            continue
        if not (type(arg) is tuple and unpack):
            arg = (arg,)
        arg_str = dump_args(*arg, **kw)
        call = "%s(%s)" % (func.__name__, arg_str)
        row.append(call)
        start = time()
        try:
            result = func(*arg, **kw)
        except Exception:
            logging.error('call function failed: %s' % call)
            print_exc()
            _error += 1
            continue
        t = time() - start
        row.append(t)
        row.append(result)
        if result == exp:
            row.append('')
            row.append("√")
        else:
            _fail += 1
            row.append(exp)
            row.append("×")
        _table.add_row(row)


if __name__ == '__main__':
    """some code examples
    """

    # one argument and one return value
    test(abs,
        [
            (1,1),
            (-2,2)
        ],
    )

    # failed test
    test(abs,
        [
            (-1,-1)
        ]
    )

    # two arguments and two return values
    test(divmod,
        [
            ((10,3), (3,1)),
            ((10,5), (2,0))
        ]
    )
    
    # return a list
    test(str.split,
        [
            (
                'hello world',
                ['hello', 'world']
            ,)
        ]
    )

    # two arguments and return a list
    test(str.split,
        [
            (
                ('1,,2,',','),
                ['1','','2','']
            )
            # can not use like this, you will see error: split() takes no keyword arguments
            # because optional arguments of built-in functions implemented in c can not be supplied by keyword
            # see http://stackoverflow.com/questions/11716687/why-does-str-split-not-take-keyword-arguments
            # ,
            # (
            #     ',1,,2,',
            #     {'sep':','},
            #     ['1','','2']
            # )
        ]
    )


    # arbitray arguments
    def foo(a, b='b', *args, **kw):
        return 'a = %s b = %s args = %s kw = %s' % (a, b, args, kw)

    test(foo,
        [
            (
                1,
                'a = 1 b = b args = () kw = {}'
            ),
            (
                (1, 2),
                'a = 1 b = 2 args = () kw = {}'
            ),
            (
                1,
                {'b':2},
                'a = 1 b = 2 args = () kw = {}'
            ),
            (
                (1, 2, 'a', 'b'),
                "a = 1 b = 2 args = ('a', 'b') kw = {}"
            ),
            (
                (1, 2, 'a', 'b'),
                {'x': 99},
                "a = 1 b = 2 args = ('a', 'b') kw = {'x': 99}"
            ),
        ]
    )
    
    # pass a tuple as argument
    test(foo,
        [
            [
                (1, 2),
                {'x': 99},
                "a = (1, 2) b = b args = () kw = {'x': 99}"
            ]
        ],
        unpack=False
    )

    # wrong test data
    test(abs,
        [
            [],
            [
                'a', 'b', 'c', 'd'
            ]
        ]
    )


    def bar(**kw):
        return 'kw = %s' % (args, kw)

    # empty args
    test(bar,
        [
            (
                (),
                {'x':99},
                "args = () kw = {'x': 99}"
            )
        ]
    )
