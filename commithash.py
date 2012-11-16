#!/usr/bin/env python
#coding: utf-8

import commands
import miniparser
import util.core as core
from util.color import *

parser = miniparser.parser()

@parser.command(description="You can show latest commit hash.")
def latest():
    commits = core.get_commits()
    print commits[-1].commithash

@parser.option("ls", description="You can show all commit hash with date, comment")
def show_all():
    commits = core.get_commits()
    for index, commit_obj in enumerate(commits):
        print "[%(index)s] %(date)s : %(hash)s - '%(comment)s'" % {
            "index": yellow("0%d"%index) if index < 10 else yellow(index),
            "date" : commit_obj.date.strftime("%y/%m/%d %H:%M:%S"),
            "hash" : magenta(commit_obj.commithash),
            "comment": commit_obj.comment,
        }

@parser.option("get", description="You can get commit hash. Please set index.", argument_types={"index":int})
def copy_hash(index):
    commits = core.get_commits()
    if index > len(commits):
        print "this index is over length limit."
        return

    print commits[index].commithash


if __name__ == "__main__":

    parser.parse()
