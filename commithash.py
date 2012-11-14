#!/usr/bin/env python
#coding: utf-8

import commands
import miniparser
import utils.core as core
from utils.color import *

parser = miniparser.parser()

@parser.command(description="You can show latest commit hash.")
def latest():
    commits = core.get_commits()
    print commits[-1].commithash

@parser.option("ls", description="You can show all commit hash with date, comment")
def show_all():
    commits = core.get_commits()
    for commit_obj in commits:
        print "%(date)s : %(hash)s - '%(comment)s'" % {
            "date" : commit_obj.date.strftime("%y/%m/%d %H:%S:%S"),
            "hash" : magenta(commit_obj.commithash),
            "comment": commit_obj.comment,
        }



if __name__ == "__main__":

    parser.parse()
