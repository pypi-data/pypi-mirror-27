# coding: utf8
from subprocess import Popen, PIPE
from .char import tostr

def lxrun(cmd, err=False):
    res = None
    p =  Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = p.communicate()
    stdout = tostr(stdout)
    stderr = tostr(stderr)
    if err:
        return stdout, stderr
    else:
        return stdout

