#!/usr/bin/env python
#coding: utf-8

import os
import commands
import miniparser
import util.core as core
from util.color import *

parser = miniparser.parser(version="1.0.0", description="This tools make you more usefull git")

@parser.command(description="You can show latest commit hash.")
def latest():
    commits = core.get_commits()
    print commits[0].commithash

@parser.option(
    "ls", 
    description="You can show all commit hash with date, comment")
def show_all():
    commits = core.get_commits()
    width = core.terminal_width()
    header = "No  "+"Date".ljust(17)+"   "+"Hash".ljust(10)+"   Comment" 
    print header
    print "-"*width
    for index, commit_obj in enumerate(commits):
        print "%(index)s  %(date)s   %(hash)s   %(comment)s" % {
            "index": yellow("0%d"%index) if index < 10 else yellow(index),
            "date" : commit_obj.date.strftime("%y/%m/%d %H:%M:%S"),
            "hash" : commit_obj.commithash[:10],
            "comment": commit_obj.comment,
        }

@parser.option(
    "get", 
    description="You can get commit hash. Please set index.", 
    argument_types={"index":int})
def copy_hash(index):
    commits = core.get_commits()
    if index > len(commits)-1:
        print yellow("this index is over length limit.")
        return

    print commits[index].commithash

@parser.option(
    "show",
    description="You can show commit difarence",
    argument_types={"index":int})
def show_diff(index):
    commits = core.get_commits()
    if index > len(commits)-1:
        print yellow("this index is over length limit.")
        return

    lines = core.shellrun("git show %s" % commits[index]).split("\n")
    for line in lines:
        if line.startswith("+"):
            print red(line)
        elif line.startswith("-"):
            print green(line)
        elif line.startswith("diff") or line.startswith("index"):
            print yellow(line)
        else:
            print line

if __name__ == "__main__":
    if core.check_exist_repo() == False:
        print yellow("There is not git repository!")
        miniparser.kill(1)

    parser.parse()
