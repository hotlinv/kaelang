

def stdprint(*args):
    print(*args)

def fprint(filezname, *args):
    # print(globals().keys())
    from kae.libs.sys import fpath
    kb = open(fpath(filezname), "w", encoding='utf-8')
    print(*args, file=kb)
    kb.close()

def speakprint(*args):
    import pyttsx3 as tts
    tts.speak(*args)