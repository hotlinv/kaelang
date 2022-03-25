# 【引用】pyttsx3

# 【映射】
ka_pmap=KaeLevMap(lev0={
    #u"语音说：(.+)":"ka_speak(*)",
})

# 【实现】
import pyttsx3 as tts

ka_outputs["语音"] = "ka_speak(*)"

@catch2cn
def ka_speak(*a):
    """语音输出"""
    tts.speak(*a)
