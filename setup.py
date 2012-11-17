#!/usr/bin/env python
#coding: utf-8

import os
from distutils.core import setup

class Information(object):
    version = "1.0.0"
    author = "alice1017"
    author_github = "http://github.com/alice1017"
    author_twitter = "http://twitter.com/alice1017"
    author_email = "takemehighermore@gmail.com"
    author_blog = "http://intention.hateblo.jp"
    license = "MIT"
    description = "The command line tools about github."
    long_description = open(os.path.join(os.path.dirname(__file__), 'README.rst'),"r").read().replace(".. sourcecode:: shellscript","::")

info  =  Information()

# build tools
os.system("cp ./commithash.py bin/commithash;chmod +x ./bin/commithash")

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
    py_modules = ['util.core', 'util.color'],
    scripts = ['bin/commithash'],
    required = ['termcolor', 'miniparser']
)
