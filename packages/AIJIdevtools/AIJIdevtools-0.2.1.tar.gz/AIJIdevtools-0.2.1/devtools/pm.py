'''
    A simple process manager
'''

import re
from devtools.linux import lxrun

__all__ = ['get_pid', 'get_command', 'kill', 'reboot']

# Internal
def _get_pid_by_port(port):
    pattern = ':{} | PID\/P'.format(port)
    res = lxrun('netstat -apn | grep -E "{0}"'.format(pattern)).strip()
    lines = res.split('\n')
    if len(lines) == 1:
        return None
    else:
        site = re.search('PID\/P', lines[0]).start()
        pid = lines[1][site:].split('/')[0]
        if pid.isdigit():
            return pid
        else:
            return None


def get_pid(pattern=None, port=None, regex=False):
    if port is not None:
        return _get_pid_by_port(port)

    if pattern is not None:
        res = lxrun('ps -ef | grep {0} "{1}"'.format(('-E' if regex else ''),pattern))
        res = res.strip()
        if not res:
            return None
        else:
            res = res.split('\n')
            pid = re.split(' +', res[0])[1]
            return pid

def get_proc(pid):
    res = lxrun('ps p {0}| grep {0}'.format(pid)).strip()
    if not res:
        return None
    return res

def get_command(pid):
    res = get_proc(pid)
    if not res:
        return None
    res = re.split(' +', res, 4) 
    res = res[-1]
    return res

def kill(pid):
    return lxrun('kill -9 {0}'.format(pid))

def reboot(pid):
    cmd = get_command(pid)
    kill(pid)
    lxrun(cmd, daemon=True)
    pid = get_pid(pattern=cmd)
    return pid

if __name__ == '__main__':
    print('Start testing.')

    for pid in [0,1,2,100]:
        print(get_proc(pid))
    print('-' * 20)
    
    port = [12346, 0, 1, 80]
    for p in port:
        print('port at {0} is '.format(p) + str( _get_pid_by_port(p)))
    
    print('Pid of this is ' + get_pid(pattern='python.*pm\.py'))
    print('-'*20)
    pid = get_pid(port=12346)
    print('origin pid =', pid)
    cmd = get_command(pid)
    print('cmd =', repr(cmd))
    kill(pid)
    cmd2 = get_command(pid)
    print('killed cmd =', cmd2)
    lxrun(cmd, daemon=True)
    pid = get_pid(pattern=cmd)
    print('New pid:', pid)
    pid = reboot(pid)
    print('Another new pid', pid)
