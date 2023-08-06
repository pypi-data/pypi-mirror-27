#!/usr/bin/env python3
# coding=utf-8

"""
@version:0.1
@author: ysicing
@file: dops/get.py 
@time: 2017/12/27 23:18
"""

from . import  BaseFlag, SubCommand


def _get_test(args):
    return 'test {}/{}'.format(args.name, args.full)


GetCommand = SubCommand(
    name="get", help="get the resource", metavar="<resource>",
    flags=[],
    subcmds=[
        SubCommand(
            name="system", usage="get system info",
            flags=[
                BaseFlag('name', metavar="services_name", nargs='?'),
                BaseFlag('--full', action='store_true'),
            ],
            func=_get_test
        ),
    ]
)

