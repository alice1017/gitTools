#!/usr/bin/env python
#coding: utf-8

import os
from distutils.core import setup
from commithash import Information

info  =  Information()

# build tools
if os.path.isdir("bin") == False:
    os.system("mkdir bin/")

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
    py_modules = ['commithash', 'util.core', 'util.color'],
    #scripts = ['bin/commithash'],
    required = ['termcolor', 'miniparser']
)
