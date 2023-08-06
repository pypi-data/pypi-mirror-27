# coding: utf8
from subprocess import Popen, PIPE, DEVNULL
from devtools.format import tostr
import os

__all__ = ['lxrun']

def lxrun(cmd, err=False, daemon=False):
    if isinstance(cmd, list):
        cmd = ' '.join(cmd)

    if daemon is True:
        p = Popen(cmd, shell=True, stdout=DEVNULL)
        return p 
        
    res = None
    p =  Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = p.communicate()
    stdout = tostr(stdout).rstrip()
    stderr = tostr(stderr).rstrip()
    if err:
        return stdout, stderr
    else:
        return stdout

