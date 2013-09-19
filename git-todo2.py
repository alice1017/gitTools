#!/usr/bin/env python
#coding: utf-8

import os
import sys
import argparse

from util         import core
from util         import adjust
from util         import objects
from util.git     import *
from util.color   import *
from util.objects import Todo

from subprocess   import Popen, PIPE
from StringIO     import StringIO
from datetime     import datetime
from sys          import exit        as kill
from gettext      import gettext     as _

parser = argparse.ArgumentParser(description="You can manage to \
                        What you want to do on your git repository.")

subparsers = parser.add_subparsers(
        title="git-todo commands",
        dest="commands",
        help=_("You can use these commands."))

cmd_init = subparsers.add_parser(
        "init", 
        help=_("Program prepare for maneging your todo."))

cmd_add = subparsers.add_parser(
        "add",
        help=_("You can add new task. \
                Please write task content at argument."))
cmd_add.add_argument(
        "content", 
        action="store", 
        help=_("your task content string. If you want to write \
                long string what contains spaces, please put \
                double-quotation(\") to left and right side of long string."))

cmd_ls = subparsers.add_parser(
        "ls",
        help=_("You can show all todo with any filter."))
cmd_ls.add_argument(
        "--filter",
        action="store",
        dest="filter:content",
        help=_("This is todo filter.\
                You can make the filter by string concatenate \
                the filter name and filter contents by colon. \
                (ex. date:2012/12/31, status:open, etc.)"))
cmd_ls.add_argument(
        "--sortby",
        action="store",
        dest="element:order",
        help=_("This option sort todo by sort element.\
                You can make the sort element by string concatenate \
                the sorter element name and sort order by colon. \
                (ex. date:ascending, index:Descending, etc.)"))


class ArgumentNamespace(object):
    def __setattr__(self, key, value):

        if value != None:

            if key.find(":") != -1 and value.find(":") == -1:
                parser.error(_("'%s' does not follow the foramt." % value))

            if key == "filter:content":
                filter_name, filter_content = value.split(":")
                self.__dict__["filter-%s"%filter_name] = filter_content

            elif key == "element:order":
                sorter_name, sort_order = value.split(":")
                self.__dict__["sortby-%s"%sorter_name] = sort_order

            else:
                self.__dict__[key] = value


    def __repr__(self):
        return "ArgumentNamespace(%s)" % ", ".join([k+"='%s'"%v for k,v in vars(self).iteritems()])

if __name__ == "__main__":
    if len(sys.argv) == 1:
        parser.parse_args(["-h"])

    args = parser.parse_args(namespace=ArgumentNamespace())
    print args

