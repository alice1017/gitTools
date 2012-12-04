#!/usr/bin/env python
#coding: utf-8

import os
import cPickle as pickle

from objects  import *
from subprocess import Popen
from subprocess import PIPE


def shellrun(command):
    """コマンドをシェルで起動し、その出力を返す"""
    if isinstance(command, list) or isinstance(command, tuple):
        proc = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    elif isinstance(command, str):
        cmd = command.split(" ")
        proc = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    
    out, err = proc.communicate()
    if len(err) == 0:
        return out[:-1]
    else:
        raise SystemError(err)
        

def check_exist_repo():
    """現在のディレクトリにgitリポジトリがあるかどうか、Booleanで返す"""
    if ".git" in os.listdir("."):
        return True
    else:
        return False

def terminal_width():
    """ターミナルの横幅をintで返す"""
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

def save_state(todolist, fp):
    """ProjectToDoSetterオブジェクトのリストとファイルポインタを引数にわたして
    シリアライズしてファイルに上書きする"""
    pickle.dump(todolist, fp)
    return True


def load_state(fp):
    """ファイルポインタを引数に渡して
    ProjectToDoSetterオブジェクトリストを返す"""
    return pickle.load(fp)


def create_file(path):
    """ファイルパスを引数に渡してファイルを作る"""
    fp = open(path, "w")
    fp.write("")
    fp.close()
    return True


