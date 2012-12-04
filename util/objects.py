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


class ProjectToDoSetter(object):
    def __init__(self, hash, author, content, status, created_at):
        self.id = hash
        self.author = author
        self.content = content
        self.status = status
        self.created_at = created_at
