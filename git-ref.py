#!/usr/bin/env python
#coding: utf-8

import sys

from argparse import ArgumentParser, SUPPRESS

# usage
#  git ref b81fe395c0bf28c4be8                         -> ハッシュ[b81fe395c0bf28c4be8]の[hash値]を出力
#  git ref tag                                         -> タグ[tag]の[hash値]を出力
#  git ref -t b81fe395c0bf28c4be8                      -> ハッシュ[b81fe395c0bf28c4be8]の[type値]を出力
#  git ref b81fe395c0bf28c4be8 --file git-todo.py      -> ハッシュ[b81fe395c0bf28c4be8]の[git-todo.py]の[hash値]を出力
#  git ref b81fe395c0bf28c4be8 --cat-file git-todo.py  -> ハッシュ[b81fe395c0bf28c4be8]の[git-todo.py]の[中身]を出力
#  git ref --ls HEAD                                   -> ハッシュ[HEAD]の[ls-tree -r]を表示
#  git ref 

parser = ArgumentParser(prog="git ref",
            description="This script can show refs hash or files easyly.")

parser.add_argument("refarence", action="store",
            help="Please set hash or refarence.\
                  If you not set other options, \
                                    script show full hash value.")

parser.add_argument("-l", "--ls", action="store_true", default=SUPPRESS,
            help="Show all files with hash in commit if you set.")

parser.add_argument("-t", "--type", action="store_true", default=SUPPRESS,
            help="Show type of hash.")

parser.add_argument("-f", "--file", action="store", default=SUPPRESS,
            help="Show file object hash in commit if you set.")

parser.add_argument("-c", "--cat-file", action="store",
            dest="file", default=SUPPRESS,
            help="Show file contents if you set.")
            

if __name__ == "__main__":

    if len(sys.argv) == 1:
        parser.parse_args(["-h"])

    args = parser.parse_args()
    print args

