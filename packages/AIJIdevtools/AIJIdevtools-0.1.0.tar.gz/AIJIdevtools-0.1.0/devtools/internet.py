def toaddr(strs):
    host = 'localhost'
    port = 0
    if isinstance(strs, list):
        if len(strs) == 1:
            return toaddr(strs[0])
        elif len(strs) == 2:
            host = strs[0]
            port = int(strs[1])
        else:
            raise ValueError
        return (host, port)
    elif isinstance(strs, str):
        strs = strs.split(':')
        if len(strs) == 1:
            host = strs[0]
            return (host, port)
        elif len(strs) == 2:
            return toaddr(strs)
        else:
            raise ValueError
    else:
        raise ValueError

if __name__ == '__main__':
    print(toaddr('1.1.1:808'))
    print(toaddr('1.1.1'))
    print(toaddr(['1.1.1', 808]))
    print(toaddr(['1.1.1', '808']))
    print(toaddr(['1.1.1:808']))
    print(toaddr(['1.1.1']))