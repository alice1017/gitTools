#!/usr/bin/env python
#coding: utf-8

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
    def __init__(self, commithash, author, date, comment):
        self.commithash = commithash
        self.author = self._get_user_obj(author)
        self.date = date
        self.comment = comment

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
    hashs = shellrun("git log --format=%h")
    commits = []
    for hash in hashs.split("\n"):
        commitdata = shellrun("git log %s" % hash)
        commithash, author, date, comment = parse_commit(commitdata)
        commits.append(
            Commit(commithash, author, date, comment))
    return commits

        
def parse_commit(commitdata):
    lines = commitdata.split("\n")
    commithash = lines[0].replace("commit ", "")
    author     = lines[1].replace("Author: ", "")
    date       = dateparser.parse(
                    lines[2].replace("Date:   ", "")
                 )
    comment    = lines[4].strip()
    return commithash, author, date, comment

def shellrun(command):
    return commands.getoutput(command)
        



