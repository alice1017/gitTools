#!/usr/bin/env python
#coding: utf-8

import os
import miniparser

from util import core
from util import adjust
from util import objects

from util.git import *
from util.color import *
from util.objects import Todo
from datetime import datetime
from sys import exit as kill

parser = miniparser.parser(
            version="0.1.0b",
            description="You can manage to" \
                    "What you want to do on your git repository")

CACHE_FILE = os.path.join(git_directory(), "gitodo")
CACHE_FILE_PATH = os.path.join(os.getcwd(), CACHE_FILE)

@parser.option(
    "init",
    description="prepare for managing todo")
def initialize():
    # check exist file
    if os.access(CACHE_FILE_PATH, os.F_OK):
        print "In this repository, you already initialized."
        return 
    # create cache file
    core.save_state([], open(CACHE_FILE_PATH,"w"))


@parser.option("new",
    description="Create new todo, Please write TODO content at argument.")
def create(content):
    if os.access(CACHE_FILE_PATH, os.F_OK) != True:
        print "The repository does not todo initialized yet."
        print "Please do 'git todo init'"
        kill(1)

    # ------------------------------------------------
    # ToDo object
    #   1. id (str)               - git hash-object
    #   2. content(str)           - todo content string
    #   3. created_at(datetime)   - datetime when open todo
    #   4. status(str)            - open or close
    #   4. correlate_commit(str)  - commit hash when created todo
    #   5. closed_at(datetime)    - datetime when close todo
    #   6. closing_commit(str)    - commit hash when closed todo
    # ------------------------------------------------

    # get todo container
    todo_container = core.load_state(open(CACHE_FILE_PATH,"r"))

    todo_info = {}
    todo_info["hashid"] = make_hash(content)
    todo_info["content"] = content
    todo_info["author"] = get_author()
    todo_info["created_at"] = datetime.now()
    todo_info["status"] = "OPEN"
    todo_info["correlate_commit"] = adjust.get_latest_commit().commithash
    todo_info["closed_at"] = None
    todo_info["closing_commit"] = None

    todo_obj = Todo(**todo_info)
    todo_container.append(todo_obj)
    core.save_state(todo_container, open(CACHE_FILE_PATH,"w"))


@parser.option("ls","list", description="Show all todos.")
def showall():
    if os.access(CACHE_FILE_PATH, os.F_OK) != True:
        print "The repository does not todo initialized yet."
        print "Please do 'git todo init'"
        kill(1)

    # get todo container
    todo_container = core.load_state(open(CACHE_FILE_PATH,"r"))
    author_length = list(sorted([len(i.author) for i in todo_container]))[-1]
    
    header = "#  "+"Date".ljust(21)+"Author".ljust(author_length)+"Stat".ljust(8)+"Hash".ljust(12)+"Content"
    title = "%(index)s  %(created_at)s %(author)s  %(status)s  %(hashid)s  %(content)s"

    print header
    print "-"*core.terminal_width()
    for index, todo in enumerate(todo_container):
        print title % {
              "index"      : yellow(index),
              "created_at" : todo.created_at.strftime(core.isoformat),
              "author"     : todo.author,
              "status"     : (blue(todo.status)+"  " if todo.status == "OPEN"
                                              else red(todo.status)),
              "hashid"     : todo.hashid[:10],
              "content"    : todo.content,
        }

@parser.option("info", description="Show more information about todo",
                                            argument_types={"index": int})
def todo_information(index):
    if os.access(CACHE_FILE_PATH, os.F_OK) != True:
        print "The repository does not todo initialized yet."
        print "Please do 'git todo init'"
        kill(1)

    # get todo container
    todo_container = core.load_state(open(CACHE_FILE_PATH,"r"))

    if index > len(todo_container):
        print "The Index value is over the number of todo."
        kill(1)
        
    todo = todo_container[index]
    header = "[%(status)s] %(index)s %(content)s" % {
                "status": (blue(todo.status) if todo.status == "OPEN" 
                                                        else red(todo.status)),
                "index": yellow("#%d"%index),
                "content": todo.content }
    timeformat = core.isoformat.replace("-"," ")

    # header
    print 
    print header
    print "-"*core.terminal_width()

    # data
    print "ToDo was "+blue("opened")+" at", ":", \
                    todo.created_at.strftime(timeformat)
    print "Commit when "+blue("opened"), ":", todo.correlate_commit[:10]
    if todo.status == "CLOSED":
        print "ToDo was "+red("closed")+" at", ":", \
                    todo.created_at.strftime(timeformat)
        print "Commit when "+red("closed"), ":", todo.closing_commit[:10]

    # print "Status:".rjust(26), (blue(todo.status) if todo.status == "OPEN"
    #                                                     else red(todo.status))
    # print 
    # print "Created at:".rjust(26), todo.created_at
    # print "Todo Hash Id:".rjust(26), magenta(todo.hashid)
    # print "Git Commit When OPEN:".rjust(26), green(todo.correlate_commit)

    # if todo.status == "CLOSED":
    #     print ""
    #     print "Closed at:".rjust(26), todo.closed_at
    #     print "Git Commit When CLOSE:".rjust(26), green(todo.closing_commit)
    

@parser.option("close", description="Update todo status from OPEN to CLOSE.",
                                                    argument_types={"index": int})
def close_todo(index):
    if os.access(CACHE_FILE_PATH, os.F_OK) != True:
        print "The repository does not todo initialized yet."
        print "Please do 'git todo init'"
        kill(1)

    # get todo container
    todo_container = core.load_state(open(CACHE_FILE_PATH,"r"))

    if index > len(todo_container):
        print "The Index value is over the number of todo."
        kill(1)

    # check already closed
    if todo_container[index].status == "CLOSED":
        print "This ToDo is already closed."
        kill(1)

    # confirm
    print "Now you wanna closing '%s' Todo." % todo_container[index].hashid[:10]
    confirm = raw_input("Are you really OK? (y/n) >> ")
    
    if confirm == "y":
        todo_container[index].status = "CLOSED"
        todo_container[index].closing_commit = adjust.get_latest_commit().commithash
        todo_container[index].closed_at = datetime.now()
        core.save_state(todo_container, open(CACHE_FILE_PATH,"w"))

    else:
        print "discontinued."


@parser.option("alldelete",
    description="This is Only Development option. You can delete all ToDo data")
def alldeelete():
    if os.access(CACHE_FILE_PATH, os.F_OK) != True:
        print "The repository does not todo initialized yet."
        print "Please do 'git todo init'"
        kill(1)

    # delete cache file
    if os.access(CACHE_FILE_PATH, os.F_OK):
        core.shellrun("rm", "%s" % CACHE_FILE_PATH)

    print "Complete"

if __name__ == "__main__":
    if check_exist_repo() == False:
        print yellow("There is not git repository!")
        kill(1)

    parser.parse()
