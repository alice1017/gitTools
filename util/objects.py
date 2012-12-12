#!/usr/bin/env python
#coding: utf-8


class User(object):
    """コミットした者の名前とメールアドレスを保持"""
    def __init__(self, name, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return "UserObject(name='%s', email='%s')" % (
                                    self.name, self.email)
    def __str__(self):
        return self.__repr__()


class Commit(object):
    """コミットのハッシュ値、製作者、日付時間、コミットコメント"""\
    """マージしたのであればマージしたデータを保持"""
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


class Todo(object):
    def __init__(self, hashid, content, created_at, status, correlate_commit, closed_at, closing_commit):
        self.hashid           = hashid
        self.content          = content
        self.created_at       = created_at
        self.status           = status
        self.correlate_commit = correlate_commit
        self.closed_at        = closed_at
        self.closing_commit   = closing_commit
    
    def __repr__(self):
        context = "id='%s', " % self.hashid
        context += "content='%s', " % self.content
        context += "created_at='%s', " % self.created_at.strftime("20%y/%m/%d-%H:%M:%S")
        context += "status='%s', " % self.status
        context += "correlate_commit='%s'" % self.correlate_commit
        return 'Todo(%s)' % context
                    
