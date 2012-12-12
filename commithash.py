#!/usr/bin/env python
#coding: utf-8

import os
import commands
import miniparser

from util import core
from util import adjust
from util.git import *
from util.color import *

parser = miniparser.parser(
        version="1.0.1", description="This tools make you more usefull git")

@parser.default(description="You can show latest commit hash.")
def latest():
    commits = adjust.get_commits()
    print commits[0].commithash

@parser.option(
    "ls", 
    description="You can show all commit hash with date, comment")
def show_all():
    commits = adjust.get_commits()
    width = core.terminal_width()
    author_length = list(sorted([len(i.author.name) for i in commits]))[-1]
    header = "No  "+"Date".ljust(17)+"  "+\
               "Author".ljust(author_length)+"  "+"Hash".ljust(10)+"  Comment" 
    print header
    print "-"*width
    for index, commit_obj in enumerate(commits):
        print "%(index)s  %(date)s  %(author)s  %(hash)s  %(comment)s" % {
            "index" : yellow(index) if index >= 100 else yellow("0%d"%index) if index > 10 else yellow("00%d"%index),
            "date"  : commit_obj.date.strftime("%y/%m/%d %H:%M:%S"),
            "author": commit_obj.author.name.ljust(6) if len(
                       commit_obj.author.name) <= 6 else commit_obj.author.name,
            "hash"  : commit_obj.commithash[:10],
            "comment": commit_obj.comment,
        }

@parser.option(
    "get", 
    description="You can get commit hash. Please set index.", 
    argument_types={"index":int})
def copy_hash(index):
    commits = adjust.get_commits()
    if index > len(commits)-1:
        print yellow("this index is over length limit.")
        return

    print commits[index].commithash

@parser.option(
    "show",
    description="You can show commit difarence",
    argument_types={"index":int})
def show_diff(index):
    commits = adjust.get_commits()
    if index > len(commits)-1:
        print yellow("this index is over length limit.")
        return

    lines = git("show","%s" % commits[index]).split("\n")
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
    if check_exist_repo() == False:
        print yellow("There is not git repository!")
        miniparser.kill(1)

    parser.parse()
