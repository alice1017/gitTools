#!/usr/bin/env python
#coding: utf-8

import os
import sys
import commands
import dateutil.parser

class BaseError(Exception):pass
class NoGitRepositoryError(BaseError):pass

class ConsoleGitLibrary:
    def __init__(self):
        if os.path.isdir(".git") == False:
            raise NoGitRepositoryError("There is not exist git repository in now directory!")

        self.command = "git"

    def commitkies(self, commit_key_length=40, output=True):
        self.command = "git log"
        log = self.execute(self.command).replace("\t","")
        
        commit_kies  = [i for i in log.split("\n") if i.startswith("commit")]
        commit_dates = [i for i in log.split("\n") if i.startswith("Date")]
        commit_msgs  = [i for i in log.split("\n") if i.startswith(" ")]
        most_longest = sorted([len(i) for i in commit_msgs])[-1]

        commit_info_unfix  = zip(commit_dates, commit_msgs, commit_kies)
        commit_info_fixed = []
        for date, msg, key in commit_info_unfix:
            commit_info_fixed.append((
                dateutil.parser.parse(date.replace("Date:   ","")).strftime("%y/%m/%d %H:%M:%S"),
                "\"" + msg.replace("    ","") + "\""+" "*(most_longest-len(msg)),
                key.replace("commit ","")[:int(commit_key_length)]
            ))


        if output == True:
            for date, msg, key in commit_info_fixed:
                print date+" : "+msg+" : "+key

        elif output == False:
            return commit_info_fixed
            

    def commitkey(self):
        commitkies = self.commitkies(40, False)
        print commitkies[0][2]

    def execute(self, command_string):
        return commands.getoutput(command_string)



if __name__ == "__main__":
    cgl = ConsoleGitLibrary()
    cgl.commitkies(10)
    cgl.commitkey()

