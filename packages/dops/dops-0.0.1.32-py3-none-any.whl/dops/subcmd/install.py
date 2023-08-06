#!/usr/bin/env python3
# coding=utf-8

"""
@version:0.1
@author: ysicing
@file: dops/install.py 
@time: 2018/1/3 23:43
"""

from . import BaseFlag, SubCommand
from  dops.plugins.instance import GeneralInstall


def _create_instance(args):
    m = GeneralInstall()
    return m.install_instance(args.name, args.reinstall)

InstallCommand = SubCommand(
    name="install", help="install instance", metavar="<resource>",
    flags=[],
    subcmds=[
        SubCommand(
            name="instance",
            usage="install an instance",
            flags=[
                BaseFlag('name', metavar='instance_id'),
                BaseFlag('-r', '--reinstall', action='store_true')
            ],
            func=_create_instance
        ),
    ]
)