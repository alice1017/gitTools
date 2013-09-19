#!/usr/bin/env python
#coding: utf-8

from git import git
from objects import *
from color   import *
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
        

def output_todolist(todo_container, sortby=None, nocolor=False):
    """ToDoが入っているcontainerを指定してToDoをリスト表示する。"""
    """第二引数にsortするattributeを指定すればsortedの状態で表示される。"""

    author_length = list(sorted([len(i.author) for i in todo_container]))[-1]
    index_length = len(str(len(todo_container)))+1
    timeformat = core.isoformat.replace("-"," ")

    header = "Date"  .ljust(21)+ \
             "Author".ljust(author_length+2)+ \
             "Stat"  .ljust(8)+ \
             "Commit".ljust(12)+ \
             "#"     .ljust(index_length)+ \
             "Content"
    title = "%(created_at)s  %(author)s  %(status)s  " \
                                  "%(commit)s  %(index)s%(content)s"

    print header
    print "-"*core.terminal_width()

    sort_attributes = ["index","created_at",\
                        "status-open","status-closed","commit"]
    todo_container = zip(range(len(todo_container)),todo_container)

    if (sortby is not None) and (sortby not in sort_attributes):
        raise AttributeError("this attribute not defined to sort attribute.")

    if sortby == "index":
        pass

    elif sortby == "created_at":
        todo_container = map(
                (lambda created_at: [(j,d)
                   for j,d in todo_container if d.created_at == created_at][0]),
                sorted([t.created_at for i,t in todo_container],reverse=True)
        )

    elif sortby == "status-open":
        todo_container = [(i,t) for i,t in todo_container if t.status == "OPEN"]

    for index, todo in todo_container:
        if nocolor == True:
            print title % {
                  "index"      : str(index).ljust(index_length),
                  "created_at" : todo.created_at.strftime(timeformat),
                  "author"     : todo.author.ljust(author_length),
                  "status"     : (todo.status+"  " if todo.status == "OPEN"
                                                             else todo.status),
                  "commit"     : todo.opened_commit[:10],
                  "content"    : todo.content
            }
        else:
            print title % {
                  "index"      : yellow(str(index).ljust(index_length)),
                  "created_at" : todo.created_at.strftime(timeformat),
                  "author"     : todo.author.ljust(author_length),
                  "status"     : (blue(todo.status)+"  " if todo.status == "OPEN"
                                                             else red(todo.status)),
                  "commit"     : (blue(todo.opened_commit[:10])
                        if todo.status == "OPEN" else red(todo.closed_commit[:10])),
                  "content"    : (red(todo.content) if todo.status == "CLOSED"
                                                                 else todo.content),
            }


