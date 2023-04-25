

def stdprint(*args):
    print(*args)

def fprint(filezname, *args):
    # print(globals().keys())
    from kae.libs.sys import fpath
    kb = open(fpath(filezname), "w", encoding='utf-8')
    print(*args, file=kb)
    kb.close()