#!/usr/bin/env python
#coding: utf-8

import os
from distutils.core import setup


class Information(object):
    version = "1.0.3.0b"
    author = "alice1017"
    author_github = "http://github.com/alice1017"
    author_twitter = "http://twitter.com/alice1017"
    author_email = "takemehighermore@gmail.com"
    author_blog = "http://intention.hateblo.jp"
    license = "MIT"
    description = "This tools make you more usefull git"
    long_description = open(os.path.join(os.path.dirname(__file__), 'README.rst'),"r").read().replace(".. sourcecode:: shellscript","::")

info  =  Information()

# build tools
if os.path.isdir("bin") == False:
    os.system("mkdir bin/")

os.system("cp ./commithash.py bin/commithash; chmod +x ./bin/commithash")
os.system("cp ./git-ref.py bin/git-ref; chmod +x ./bin/git-ref")

setup(
    name = "gitTools",
    author = info.author,
    author_email = info.author_email,
    version = info.version,
    license = info.license,
    url = info.author_github,
    download_url = info.author_github+"/gitTools",
    description = info.description,
    long_description = info.long_description,
    py_modules = ['commithash', 'util.core', 'util.color', 'util.objects', 'util.git', 'util.adjust'],
    scripts = ['bin/commithash', 'bin/git-ref'],
    requires = ['dateutil', 'termcolor', 'miniparser'],
)
