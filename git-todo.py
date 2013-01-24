#!/usr/bin/env python
#coding: utf-8

import os
import sys
import miniparser

from util import core
from util import adjust
from util import objects
from util.git import *
from util.color import *
from util.objects import Todo

from subprocess import Popen, PIPE
from StringIO import StringIO
from datetime import datetime
from sys import exit as kill

parser = miniparser.parser(
            version="0.1.0b",
            description="You can manage to" \
                    "What you want to do on your git repository")

CACHE_FILE = os.path.join(git_directory(), "gitodo")
CACHE_FILE_PATH = os.path.join(os.getcwd(), CACHE_FILE)

@parser.default(description="Show all ToDos.")
def default():
    showall()

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
    #   3. author(str)            - the author name that create todo
    #   4. created_at(datetime)   - datetime when open todo
    #   5. status(str)            - open or close
    #   6. opened_commit(str)     - commit hash when created todo
    #   7. closed_at(datetime)    - datetime when close todo
    #   8. closed_commit(str)     - commit hash when closed todo
    # ------------------------------------------------

    # get todo container
    todo_container = core.load_state(open(CACHE_FILE_PATH,"r"))

    for n,todo in enumerate(todo_container):
        if todo.content == content:
            print "fatal: this ToDo is duplicate."
            print "Your appending ToDo: %s" % content
            print "duplicate ToDo: %(index)s %(content)s" % {
                    "index": yellow(n), "content":todo.content}
            kill(1)


    todo_info = {}
    todo_info["hashid"] = make_hash(content)
    todo_info["content"] = content
    todo_info["author"] = get_author()
    todo_info["created_at"] = datetime.now()
    todo_info["status"] = "OPEN"
    todo_info["opened_commit"] = adjust.get_latest_commit().commithash
    todo_info["closed_at"] = None
    todo_info["closed_commit"] = None

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
    if len(todo_container) == 0:
        print "There is not ToDo."
        kill(1)

    author_length = list(sorted([len(i.author) for i in todo_container]))[-1]
    index_length = len(str(len(todo_container)))+1
    timeformat = core.isoformat.replace("-"," ")
    
    header = "Date".ljust(21)+"Author".ljust(author_length)+" "+ \
                    "Stat".ljust(8)+"Commit".ljust(12)+"#".ljust(index_length)+"Content"
    title = "%(created_at)s  %(author)s  %(status)s  %(commit)s  %(index)s%(content)s"

    print header
    print "-"*core.terminal_width()
    for index, todo in enumerate(todo_container):
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

@parser.option("info", description="Show more information about todo",
                                            argument_types={"index": int})
def todo_information(index):
    if os.access(CACHE_FILE_PATH, os.F_OK) != True:
        print "The repository does not todo initialized yet."
        print "Please do 'git todo init'"
        kill(1)

    # get todo container
    todo_container = core.load_state(open(CACHE_FILE_PATH,"r"))
    if len(todo_container) == 0:
        print "There is not ToDo."
        kill(1)

    if index > len(todo_container)-1:
        print "The Index value is over the number of todo."
        kill(1)
        
    todo = todo_container[index]
    timeformat = core.isoformat.replace("-"," ")

    print "%s" % yellow("#%d"%index)
    print "[%s]" % (blue(todo.status) if todo.status == "OPEN"
                                        else red(todo.status)),
    print todo.content
    print "-"*core.terminal_width()
    
    print "Author".ljust(13),":",magenta(todo.author)
    print "Primary Id".ljust(13),":",todo.hashid
    print "Created at".ljust(13), ":", todo.created_at.strftime(
                                                     timeformat)
    if todo.status == "CLOSED":
        print "Closed at".ljust(13), ":", todo.closed_at.strftime(
                                                            timeformat)
    print "Opened commit", ":", blue(todo.opened_commit)

    if todo.status == "CLOSED":
        print "Closed commit", ":", red(todo.closed_commit)
        print "-"*core.terminal_width()
        #print get_commit_diff(todo.closed_commit)


@parser.option("close", description="Update todo status from OPEN to CLOSE.",
                                                    argument_types={"index": int})
def close_todo(index):
    if os.access(CACHE_FILE_PATH, os.F_OK) != True:
        print "The repository does not todo initialized yet."
        print "Please do 'git todo init'"
        kill(1)

    # get todo container
    todo_container = core.load_state(open(CACHE_FILE_PATH,"r"))
    if len(todo_container) == 0:
        print "There is not ToDo."
        kill(1)

    if index > len(todo_container):
        print "The Index value is over the number of todo."
        kill(1)

    # check already closed
    if todo_container[index].status == "CLOSED":
        print "This ToDo is already closed."
        kill(1)

    # create tag
    put_tag("ToDo#%d_close" % index, "Closed '%s' ToDo."%todo_container[index].content)

    # change status
    todo_container[index].status = "CLOSED"
    todo_container[index].closed_commit = adjust.get_latest_commit().commithash
    todo_container[index].closed_at = datetime.now()
    core.save_state(todo_container, open(CACHE_FILE_PATH,"w"))


@parser.option("del", description="delete ToDo", argument_types={"index": int})
def delete(index):
    if os.access(CACHE_FILE_PATH, os.F_OK) != True:
        print "The repository does not todo initialized yet."
        print "Please do 'git todo init'"
        kill(1)

    # get todo container
    todo_container = core.load_state(open(CACHE_FILE_PATH,"r"))
    if len(todo_container) == 0:
        print "There is not ToDo."
        kill(1)

    if index > len(todo_container):
        print "The Index value is over the number of todo."
        kill(1)

    todo_container.pop(index)
    core.save_state(todo_container, open(CACHE_FILE_PATH,"w"))


@parser.option("log",
    description="You can show commit log with when your ToDo opened or closed")
def show_log():
    if os.access(CACHE_FILE_PATH, os.F_OK) != True:
        print "The repository does not todo initialized yet."
        print "Please do 'git todo init'"
        kill(1)

    todo_container = core.load_state(open(CACHE_FILE_PATH,"r"))
    commits = adjust.get_commits()
    pager = get_pager()
    isoformat = "%a %b %d %H:%M:%S %Y %z"
    

    io = StringIO()
    sys.stdout = io

    for commit in commits:
        print yellow("commit: %s" % commit.commithash)

        opened_commits = ([blue(t.hashid[:10]) for t in todo_container \
                                if t.opened_commit == commit.commithash])
        closed_commits = ([red(t.hashid[:10]) for t in todo_container \
                                if t.closed_commit == commit.commithash])

        if len(opened_commits) != 0:
            print "Opened ToDo: %s" % ", ".join(opened_commits)
        if len(closed_commits) != 0:
            print "Closed ToDo: %s" % ", ".join(closed_commits)

        if commit.merge_data != None:
            print "Merge: %s" % " ".join(commit.merge_data)
            print "Author: %s <%s>" % (
                    commit.author.name,
                    commit.author.email)
        else:
            print "Author: %s <%s>" %  (
                    commit.author.name,
                    commit.author.email)
        print "Date: %s" % commit.date.strftime(isoformat)
        print 
        print commit.comment
        print 
    
    sys.stdout = sys.__stdout__
    if pager == None:
        print io.getvalue()[:-1]
    else:
        proc = Popen(pager.split(" "), stdin=PIPE, stderr=PIPE)
        proc.communicate(io.getvalue()[:-1])

@parser.option("alldelete",
    description=yellow("This is Only Development option.")+" You can delete all ToDo data")
def alldeelete():
    if os.access(CACHE_FILE_PATH, os.F_OK) != True:
        print "The repository does not todo initialized yet."
        print "Please do 'git todo init'"
        kill(1)

    # save todo container data to backup file
    fp = open("todo_backup","w")
    todo_container = core.load_state(open(CACHE_FILE_PATH,"r"))
    core.save_state(todo_container, fp)

    # delete cache file
    if os.access(CACHE_FILE_PATH, os.F_OK):
        core.shellrun("rm", "%s" % CACHE_FILE_PATH)

    print "Complete"

@parser.option("import",
    description=yellow("This is Only Development option")+ \
                    " You can import ToDo data from backup file.")
def import_todo(backup_file):
    if os.access(backup_file, os.F_OK) == False:
        print "'%s' file is not found." % backup_file
        kill(1)

    fp = open(backup_file,"r")
    todo_container = core.load_state(fp)
    
    core.save_state(todo_container, open(CACHE_FILE_PATH,"w"))
    
if __name__ == "__main__":
    if check_exist_repo() == False:
        print yellow("There is not git repository!")
        kill(1)

    parser.parse()
