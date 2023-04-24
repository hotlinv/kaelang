

def stdprint(*args):
    print(*args)

def fprint(filename, *args):
    kb = open(filename, encoding='utf-8')
    print(*args, file=kb)
    kb.close()