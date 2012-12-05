#!/usr/bin/env python
#coding: utf-8

from git import git
from objects import *
from dateutil import parser as dateparser

def get_commits():
    """シェルからコミットログを取得してCommitオブジェクトにしてリストで返す"""
    commits = []
    commits_string = git("log")

    # analyzing
    commitlines = commits_string.split("\n\n")
    commits_string_list = []
    while 0 < len(commitlines):
        commits_string_list.append(
                    "\n".join(commitlines[0:2]))
        commitlines = commitlines[2:]

    # parse
    for commitline in commits_string_list:
        commitdata = parse_commit(commitline)
        commits.append(
            Commit(**commitdata))

    return commits

def get_latest_commit():
    """最新のコミットのCommitオブジェクトを返す"""
    commits = []
    commits_string = git("log", "-n", "1")

    # analyzing
    commitlines = commits_string.split("\n\n")
    commits_string_list = []
    while 0 < len(commitlines):
        commits_string_list.append(
                    "\n".join(commitlines[0:2]))
        commitlines = commitlines[2:]

    # parse
    for commitline in commits_string_list:
        commitdata = parse_commit(commitline)
        commits.append(
            Commit(**commitdata))

    return commits[0]

def parse_commit(commitstring):
    """シェルから取得したコミットログをパースして""" \
    """コミットのハッシュ値、コミットした者、日付・時間、コミットコメント及び""" \
    """マージした場合はsourceとdestinationを返す"""
    commitlines = commitstring.split("\n")

    # 1 row
    commithash = commitlines[0].replace("commit ","")

    # 2 row
    merge_source = merge_dest = None
    author = None
    if "Merge" in commitlines[1]:
        # parse merge data
        merge_source = commitlines[1].split(" ")[1]
        merge_dest = commitlines[1].split(" ")[2]
    else:
        # parse author
        author = commitlines[1].replace("Author: ","")

    # 3 row
    if "Author" in commitlines[2]:
        # parse author
        author = commitlines[2].replace("Author: ","")
    else:
        # parse date
        date = dateparser.parse(commitlines[2].replace("Date:   ",""))

    # 4 row
    if "Date" in commitlines[3]:
        # parse date
        date = dateparser.parse(commitlines[3].replace("Date:   ",""))
    else:
        # parse comment
        comment = " ".join([i.strip() for i in commitlines[3:]])

    # 5 row
    if "Merge" in commitlines[1]:
        # comment -> under 4 row
        comment = " ".join([i.strip() for i in commitlines[4:]])

    return {"commithash": commithash,
            "merge_data": (merge_source, merge_dest) if merge_source != None else None,
            "author"    : author,
            "date"      : date,
            "comment"   : comment}
        


