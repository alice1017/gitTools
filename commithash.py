#!/usr/bin/env python
#coding: utf-8

import os
import sys
import commands
import miniparser

from util import core
from util import adjust
from util.git import *
from util.color import *
from StringIO import StringIO

parser = miniparser.parser(
        version="1.0.1", 
        description="The commithash support operating git commit hash")

@parser.default(description="You can show latest commit hash.")
def latest():
    commits = adjust.get_commits()
    print commits[0].commithash

@parser.option(
    "ls", 
    description="You can show all commit hash with date, comment")
def show_all():
    commits = adjust.get_commits()
    pager = get_pager()
    io = StringIO()

    width = core.terminal_width()
    author_length = list(sorted([len(i.author.name) for i in commits]))[-1]
    number_length = len(str(len(commits)))+1 # コミットの長さの桁数

    header = "#".ljust(number_length)+" "+"Date".ljust(19)+"  "+\
               "Author".ljust(author_length)+"  "+"Hash".ljust(10)+"  Comment" 
    timeformat = core.isoformat.replace("-"," ")

    sys.stdout = io
    print header
    print "-"*(width-1)
    for index, commit_obj in enumerate(commits):
        print "%(index)s %(date)s  %(author)s  %(hash)s  %(comment)s" % {
            "index"  : yellow(index)+" "*(number_length-len(str(index))),
            "date"   : commit_obj.date.strftime(timeformat),
            "author" : commit_obj.author.name.ljust(author_length),
            "hash"   : commit_obj.commithash[:10],
            "comment": commit_obj.comment,
        }

    sys.stdout = sys.__stdout__
    if pager == None:
        print io.getvalue()[:-1]
    else:
        proc = Popen(pager.split(" "), stdin=PIPE, stderr=PIPE)
        proc.communicate(io.getvalue()[:-1])

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
