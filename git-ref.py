#!/usr/bin/env python
#coding: utf-8

import sys

from util         import core
from util         import adjust
from util.git     import *
from argparse     import ArgumentParser, SUPPRESS

# usage
#  git ref b81fe395c0bf28c4be8                         -> ハッシュ[b81fe395c0bf28c4be8]の[hash値]を出力
#  git ref tag                                         -> タグ[tag]の[hash値]を出力
#  git ref -t b81fe395c0bf28c4be8                      -> ハッシュ[b81fe395c0bf28c4be8]の[type値]を出力
#  git ref b81fe395c0bf28c4be8 --file git-todo.py      -> ハッシュ[b81fe395c0bf28c4be8]の[git-todo.py]の[hash値]を出力
#  git ref b81fe395c0bf28c4be8 --cat-file git-todo.py  -> ハッシュ[b81fe395c0bf28c4be8]の[git-todo.py]の[中身]を出力
#  git ref --ls HEAD                                   -> コミット[HEAD]の[ls-tree -r]を表示
#  git ref --detail HEAD                               -> コミット[HEAD]の[git show]を表示

parser = ArgumentParser(prog="git ref",
            description="This script can show reference hash or files easyly.")

parser.add_argument("reference", action="store",
            help="Please set hash of reference.\
                  If you not set other options, \
                                    script show full hash value.")

parser.add_argument("-l", "--ls", action="store_true",
            help="Show all files with hash in commit.")

parser.add_argument("-t", "--type", action="store_true",
            help="Show type of hash.")

parser.add_argument("-f", "--file", action="store",
            help="Show file object hash in commit.")

parser.add_argument("-p", "--pretty-print", action="store", dest="pretty_print",
            metavar="FILE", help="Show file contents.")

class ArgumentNamespace:

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __repr__(self):
        return "ArgumentNamespace(%s)" % ", ".join(
                                [k+"='%s'"%v for k,v in vars(self).iteritems()])

    def is_only_ref(self):
        """Return True if there is only reference argument"""

        if args.file == None and args.type == False and args.ls == False and args.pretty_print == None:
            return True

    def is_only_ls(self):
        """Return True if there is only --ls option"""

        if args.ls == False:
            return False

        if args.ls == True:

            if args.file == None and args.type == False and args.pretty_print == None:
                return True

            else:
                parser.error("this option can't use concomitantly.")

    def is_only_type(self):
        """Return True if there is only --type option"""

        if args.type == False:
            return False

        if args.type == True:

            if args.file == None and args.ls == False and args.pretty_print == None:
                return True

            else:
                parser.error("this option can't use concomitantly.")

    def is_only_file(self):
        """Return True is there is only --file option"""

        if args.file == None:
            return False

        if args.file:

            if args.type == False and args.ls == False and args.pretty_print == None:
                return True

            else:
                parser.error("this option can't use concomitantly.")

    def is_only_pretty_print(self):
        """Return True is there is only --pretty-print option"""

        if args.pretty_print == None:
            return False

        if args.pretty_print:

            if args.type == False and args.ls == False and args.file == None:
                return True

            else:
                parser.error("this option can't use concomitantly.")

def check_ref(reference):
    """This function check reference whether it's valid ref, Return True"""
    try:
        # Run git rev-parse --verify [ref]
        verified = git("rev-parse", "--verify", reference)

    except:
        # If it is invalid, Call error
        parser.error("invalid reference.")
        sys.exit(1)

    return True

def main(args):

    ref = args.reference
    check_ref(ref)

    # User set reference only
    if args.is_only_ref():

        print git("rev-parse", ref)
        return 0

    # User set --ls 
    elif args.is_only_ls():

        print git("ls-tree", "-r", ref)
        return 0

    # User set --type
    elif args.is_only_type():

        print git("cat-file", "-t", ref)
        return 0

    # User set --file
    elif args.is_only_file():

        body = git("ls-tree", ref, args.file)

        if len(body) == 0:
            parser.error("%s file does not found." % args.file)

        print body.split(" ")[-1].split("\t")[0]
        return 0

    # User set --pretty-print
    elif args.is_only_pretty_print():

        body = git("ls-tree", ref, args.pretty_print)

        if len(body) == 0:
            parser.error("%s file does not found." % args.file)

        hash_var = body.split(" ")[-1].split("\t")[0]

        print git("cat-file", "-p", hash_var)
        return 0


if __name__ == "__main__":

    if len(sys.argv) == 1:
        parser.parse_args(["-h"])

    #args = parser.parse_args()
    args = parser.parse_args(namespace=ArgumentNamespace())
    #print args

    sys.exit(main(args))

