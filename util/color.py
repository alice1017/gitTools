#!/usr/bin/env python
#coding: utf-8

import termcolor

#blue, grey, yellow, green, cyan, magenta, white, red


def blue(string):
    return termcolor.colored(string, "blue")


def grey(string):
    return termcolor.colored(string, "grey")


def yellow(string):
    return termcolor.colored(string, "yellow")


def green(string):
    return termcolor.colored(string, "green")


def cyan(string):
    return termcolor.colored(string, "cyan")


def magenta(string):
    return termcolor.colored(string, "magenta")


def red(string):
    return termcolor.colored(string, "red")
