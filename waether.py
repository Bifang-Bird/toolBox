#encoding:utf8
from aip import AipSpeech

class SpeechText(object):
    # 有点类似其它高级语言的构造函数
    def __init__(self,text,vol,per,num):
        self.text = text
        self.per = per
        self.vol = vol
        self.num = num

    def speech(self):
        """ 你的 APPID AK SK """
        APP_ID = '11093849'
        API_KEY = 'LFyDmN0p5MwbtlGv9Lqb0Nyj'
        SECRET_KEY = 'Z47Ht5lqEiibMGp5KTtI3WpTPcsjdepF'

        client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
        # result = client.synthesis(text = self.text, options={'vol':self.vol,'per':self.per})
        result = client.synthesis(self.text, 'zh', 1, {'vol': self.vol,'per':self.per})

        if not isinstance(result,dict):
            with open('./data/'+str(self.num)+'audio.mp3','wb') as f:
                f.write(result)
        else:print(result)
