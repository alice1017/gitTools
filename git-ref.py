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

parser.add_argument("-l", "--ls", action="store_true", default=SUPPRESS,
            help="Show all files with hash in commit.")

parser.add_argument("-t", "--type", action="store_true", default=SUPPRESS,
            help="Show type of hash.")

parser.add_argument("-f", "--file", action="store", default=SUPPRESS,
            help="Show file object hash in commit.")

parser.add_argument("-c", "--cat-file", action="store",
            dest="file", default=SUPPRESS,
            help="Show file contents.")

class ArgumentNamespace:

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __repr__(self):
        return "ArgumentNamespace(%s)" % ", ".join(
                                [k+"='%s'"%v for k,v in vars(self).iteritems()])

    def is_only_ref(self):
        """Return True  if there is only reference argument"""

        if len(vars(self).keys()) == 1 and self.reference:
            return True

def check_ref(reference):
    """This function check reference whether it's valid ref, \
                              If it's valid ref, return reference"""

    try:
        # Run git rev-parse --verify [ref]
        verified = git("rev-parse", "--verify", reference)

    except:
        # If it is invalid, Call error
        parser.error("invalid reference.")

    return reference

def main(args):

    # User set reference only
    if args.is_only_ref():

        print git("rev-parse", check_ref(args.reference))
        return 0

    if args.ls:

        print git("ls-tree", "-r", check_ref(args.reference))
        return 0



            

if __name__ == "__main__":

    if len(sys.argv) == 1:
        parser.parse_args(["-h"])

    #args = parser.parse_args()
    args = parser.parse_args(namespace=ArgumentNamespace())
    print args

    sys.exit(main(args))

