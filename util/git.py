#!/usr/bin/env python
#coding: utf-8

from subprocess import Popen
from subprocess import PIPE

class GitError(BaseException):
    """git関数の取得結果でエラーがでた場合に発生する"""
    pass


def git(cmd, *args, **kwargs):
    """gitの実行結果を取得して返す"""
    input=None
    if "input" in kwargs:
        input = kwargs["input"]
    else:
        input = ""
    
    proc = Popen(
        ("git", cmd) + args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate(input)
    if len(err) == 0:
        return out[:-1]
    else:
        raise GitError(err)

def git_directory():
    """gitリポジトリのディレクトリを返す"""
    return git("rev-parse","--git-dir")

def make_hash(data):
    """ハッシュを作って返す"""
    hash = git("hash-object", "--stdin", input=data)
    return hash

def check_exist_repo():
    """現在のディレクトリにgitリポジトリがあるかどうか、Booleanで返す"""
    boolean = git("rev-parse", "--is-inside-work-tree")
    if boolean == "true":
        return True
    else:
        return False

def get_pager():
    """gitが使用しているpagerを取得して返す。""" \
    """pagerの設定をしていない場合はlessを返す"""
    out = git("config", "core.pager")
    if len(out) == 0:
        # parger設定をしていない
        return "less"
    else:
        return out[:-1]
