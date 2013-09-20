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

__prog__    = "git-todo"
__version__ = "0.2.0b"
__author__  = "Alice1017 <takemehighermore@gmail.com>"


class OriginalHelpFormatter(argparse.HelpFormatter):
    def _format_action(self, action):
        # determine the required width and the entry label
        help_position = min(self._action_max_length + 2,
                self._max_help_position)
        help_width = self._width - help_position
        action_width = help_position - self._current_indent - 2
        action_header = self._format_action_invocation(action)

        # ho nelp; start on same line and add a final newline
        if not action.help:
            tup = self._current_indent, '', action_header
            action_header = '%*s%s\n' % tup

        # short action name; start on the same line and pad two spaces
        elif len(action_header) <= action_width:
            tup = self._current_indent, '', action_width, action_header
            action_header = '%*s%-*s  ' % tup
            indent_first = 0

        # long action name; start on the next line
        else:
            tup = self._current_indent, '', action_header
            action_header = '%*s%s\n' % tup
            indent_first = help_position


        # collect the pieces of the action help
        parts = [action_header]

        # if there was help for the action, add lines of help text
        if action.help:
            help_text = self._expand_help(action)
            help_lines = self._split_lines(help_text, help_width)
            parts.append('%*s%s\n' % (indent_first, '', help_lines[0]))
            for line in help_lines[1:]:
                parts.append('%*s%s\n' % (help_position, '', line))

        # or add a newline if the description doesn't end with one
        elif not action_header.endswith('\n'):
            parts.append('\n')

        # if there are any sub-actions, add their help as well
        for subaction in self._iter_indented_subactions(action):
            parts.append(self._format_action(subaction))

            # Original Code
            parts.append("\n")

        # return a single string
        return self._join_parts(parts)

help_formatter = (lambda prog: 
        OriginalHelpFormatter(
            prog,
            indent_increment=4,
            max_help_position=27,
            width=int(core.terminal_width())
            )
        )

# Parser Define
parser = argparse.ArgumentParser(
        prog=__prog__,
        formatter_class=help_formatter,
        description="You can manage to What you want to do on your git repository.")
parser.add_argument(
        "-v", "--version",
        action="version",
        version="%s - %s" % (__prog__,__version__))

# Subparser Define
subparsers = parser.add_subparsers(
        title="git todo commands",
        dest="commands")

# subcommand : init
cmd_init = subparsers.add_parser(
        "init", 
        help=_("Program prepare for maneging your todo."))

# subcommand : add
cmd_add = subparsers.add_parser(
        "add",
        help=_("You can add new task. \
                Please write task content to argument."))
cmd_add.add_argument(
        "content", 
        action="store", 
        help=_("your task content string. If you want to write \
                long string what contains spaces, please put \
                double-quotation(\") to left and right side of long string."))

# Subcommand : ls
cmd_ls = subparsers.add_parser(
        "ls",
        help=_("You can show tasks with any filter. \
                If you all this option without any filter, \
                this option show only OPEN status tasks. \
                And If you want to show all tasks, \
                Please use --all option."))
cmd_ls.add_argument(
        "--all",
        action="store_true",
        dest="show-all",
        help=_("If you want to show all tsaks, Please use this option"))
cmd_ls.add_argument(
        "--filter",
        action="store",
        dest="filter:content",
        help=_("This is todo filter.\
                You can make the filter by string concatenate \
                the filter name and filter contents by colon. \
                (ex. date:2012/12/31, status:open, etc.) \
                These are filter names what you use : \
                *date"))
cmd_ls.add_argument(
        "--sortby",
        action="store",
        dest="element:order",
        help=_("This option sort todo by sort element.\
                You can make the sort element by string concatenate \
                the sorter element name and sort order by colon. \
                (ex. date:ascending, index:Descending, etc.)"))

# Subcommand : branch
cmd_branch = subparsers.add_parser(
        "branch",
        help=_("This option create branch to implement contents of a task, and \
                checkout it branch. Please write the task index \
                to argument.You can set branch name using argument. \
                But when you don't want to set branch name, \
                the branch name become 'Todo#(todo-index)_implement'. "))
cmd_branch.add_argument(
        "index",
        action="store",
        type=int,
        help=_("The task index. this is INT type only."))
cmd_branch.add_argument(
        "-n", "--name",
        action="store",
        dest="branch-name",
        help=_("The branch name string. \
                You can use this option if you want to set branch name."))

# Subcommand : close
cmd_close = subparsers.add_parser(
        "close",
        help=_("You can close a task.\
                Please write the task index to argument. \
                If you close a task, this program put a tag \
                what name is 'Todo#(todo-index)_close' on git. \
                (ex. Todo#3_close, etc.) \
                And this program changes status to CLOSED."))
cmd_close.add_argument(
        "index",
        action="store",
        type=int,
        help=_("The task index. this is INT type only."))

# Subcommand : reopen
cmd_reopen = subparsers.add_parser(
        "reopen",
        help=_("If you want to open a task again when you close a task by \
                mistake, You can use this option. \
                This option change task status to OPEN, and this option \
                don't change commit hash when a task opened. And, \
                This option delete git tag that put when you closed a task. \
                Please write the task index to argument."))
cmd_reopen.add_argument(
        "index",
        action="store",
        type=int,
        help=_("The task index. this is INT type only."))

# Subcomand : print
cmd_print = subparsers.add_parser(
        "print",
        help=_("This program create the TODO file to write \
                only OPEN status tasks."))



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

