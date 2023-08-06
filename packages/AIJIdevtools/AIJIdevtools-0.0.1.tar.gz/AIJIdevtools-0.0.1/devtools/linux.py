# coding: utf8
from subprocess import Popen, PIPE
from .char import tostr

def lxrun(cmd):
    res = None
    with Popen(cmd, stdout=PIPE, shell=True) as p:
        res = tostr(p.stdout.read())
    return res

