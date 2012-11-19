#!/usr/bin/env python
#coding: utf-8

import os
import commands
import dateutil.parser as dateparser


class User(object):
    def __init__(self, name, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return "UserObject(name='%s', email='%s')" % (
                                    self.name, self.email)
    def __str__(self):
        return self.__repr__()

class Commit(object):
    def __init__(self, commithash, author, date, comment, merge_data=None):
        self.commithash = commithash
        self.author = self._get_user_obj(author)
        self.date = date
        self.comment = comment
        self.merge_data = merge_data

    def _get_user_obj(self, author_string):
        if " " in author_string:
            lines = author_string.split(" ")
            name = lines[0]
            email = lines[1][0:1]
            return User(name, email)
        else:
            return User(author_string)


    def __repr__(self):
        return "CommitObject(%s)" % self.commithash

    def __str__(self):
        return self.commithash


def get_commits():
    commits = []
    commits_string = shellrun("git log")
    
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

            
def parse_commit(commitstring):
    commitdata = [i for i in commitstring.split("\n") if i != "    "]
    parse_result = {}
    
    if len(commitdata) == 5:
        # Contain merge data
        # -- sample -----------------------------------------
        # 0 commit 9bb0df77e3f6727c873f8fee1e3f73f74b5ad633
        # 1 Merge: b1f4e7e 943916f
        # 2 Author: alice <takemehighermore@gmail.com>
        # 3 Date:   Thu Nov 15 00:47:26 2012 +0900
        # 4     Merge branch 'master' into rewrite
        # ---------------------------------------------------
        commithash   = commitdata[0].split(" ")[1]
        merge_source = commitdata[1].split(" ")[1]
        merge_dest   = commitdata[1].split(" ")[2]
        author       = commitdata[2].split(" ")[1]
        date         = dateparser.parse(
                        commitdata[3].replace(
                                "Date:   ",""))
        comment      = commitdata[4].strip()

        return {"commithash": commithash,
                "merge_data": (merge_source, merge_dest),
                "author"    : author,
                "date"      : date,
                "comment"   : comment}

    elif len(commitdata) == 4:
        # nomal
        # -- sample -----------------------------------------
        # 0 commit 943916fe88a2c247231f2f5f138e7d572e9248d5
        # 1 Author: alice <takemehighermore@gmail.com>
        # 2 Date:   Thu Nov 15 00:46:23 2012 +0900
        # 3     added utilities
        # ---------------------------------------------------
        commithash   = commitdata[0].split(" ")[1]
        author       = commitdata[1].split(" ")[1]
        date         = dateparser.parse(
                        commitdata[2].replace(
                                "Date:   ",""))
        comment      = commitdata[3].strip()

        return {"commithash": commithash,
                "merge_data": None,
                "author"    : author,
                "date"      : date,
                "comment"   : comment}
    else:
        # abnomal
        # -- sample -----------------------------------------
        # 0 commit 311dda81133c69e9394a1c11c5eab7b1baf0477c
        # 1 Merge: 5740af5 3691dad
        # 2 Author: alice <genocidedragon@gmail.com>
        # 3 Date:   Mon Nov 5 16:58:31 2012 -0800
        # 4    Merge pull request #5 from yosida95/bugfix
        # 5    pull request merge.
        # ---------------------------------------------------
        commithash   = commitdata[0].split(" ")[1]
        merge_source = commitdata[1].split(" ")[1]
        merge_dest   = commitdata[1].split(" ")[2]
        author       = commitdata[2].split(" ")[1]
        date         = dateparser.parse(
                        commitdata[3].replace(
                                "Date:   ",""))
        comment      = ", ".join([i.strip() for i in commitdata[4:]])

        return {"commithash": commithash,
                "merge_data": (merge_source, merge_dest),
                "author"    : author,
                "date"      : date,
                "comment"   : comment}

def shellrun(command):
    return commands.getoutput(command)
        

def check_exist_repo():
    if ".git" in os.listdir("."):
        return True
    else:
        return False

def terminal_width():
    """Return terminal width."""
    width = 0
    try:
        import struct
        import fcntl
        import termios
        s = struct.pack('HHHH', 0, 0, 0, 0)
        x = fcntl.ioctl(1, termios.TIOCGWINSZ, s)
        width = struct.unpack('HHHH', x)[1]
    except:
        pass
    if width <= 0:
        if "COLUMNS" in os.environ:
            width = int(os.getenv("COLUMNS"))
        if width <= 0:
            width = 80
    return width

