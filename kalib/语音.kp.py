# 【引用】pyttsx3

# 【映射】
ka_pmap=lambda:{
    u"语音说：(.+)":"ka_speak(*)",
}

# 【实现】
import pyttsx3 as tts

@catch2cn
def ka_speak(*a):
    """打印"""
    tts.speak(*a)
