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
            email = lines[1]
            return User(name, email)
        else:
            return User(author_string)


    def __repr__(self):
        return "CommitObject(%s)" % self.commithash

    def __str__(self):
        return self.commithash


class Todo(object):
    def __init__(self, hashid, content, author, created_at, status, opened_commit, closed_at, closed_commit):
        self.hashid           = hashid
        self.content          = content
        self.author           = author
        self.created_at       = created_at
        self.status           = status
        self.opened_commit    = opened_commit
        self.closed_at        = closed_at
        self.closed_commit    = closed_commit
    
    def __repr__(self):
        context =  "id='%s', "             % self.hashid
        context += "content='%s', "        % self.content
        context += "author='%s', "         % self.author
        context += "created_at='%s', "     % self.created_at.strftime(core.isoformat)
        context += "status='%s', "         % self.status
        context += "opened_commit='%s'"    % self.opened_commit
        return 'Todo(%s)' % context
                    
