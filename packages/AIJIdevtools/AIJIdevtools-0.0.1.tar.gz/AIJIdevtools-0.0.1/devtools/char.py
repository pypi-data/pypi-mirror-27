# coding: utf8
def tostr(sth):
    if isinstance(sth, str):
        return sth
    elif isinstance(sth, bytes):
        return sth.decode()
    else:
        return str(sth)

def tobytes(sth):
    if isinstance(sth, bytes):
        return sth
    elif isinstance(sth, str):
        return sth.encode()
    else:
        return bytes(sth)
