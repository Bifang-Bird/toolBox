import datetime
import os
from playsound import playsound
from waether import SpeechText

# 遍历文件夹
def walkFile(file):
    data = []
    for root, dirs, files in os.walk(file):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        for f in files:
            path = os.path.join(root, f)
            if '.mp3' in path:
                data.append(path)
                print(path)
    return data
        # 遍历所有的文件夹
        # for d in dirs:
        #     print(os.path.join(root, d))

def speechtext():
    # 第二种方法
    data = []
    k = ''
    for line in open("E:\ownworkspace\python-spider-master\python-spider\data\demo.txt", "r", encoding='utf-8'):  # 设置文件对象并读取每一行文件
        if line != '\n':
            k = k + line
        else:
            data.append(k)  # 将每一行文件加入到list中
            k = ''
    count = 0
    for text in data:
        count = count + 1
        speechtext = SpeechText(text, 5, 3, count)
        speechtext.speech()
    files = []
    files = walkFile('./data/')
    for file in files:
        playsound(file)

def speechncp():
    # 第二种方法
    data = []
    k = ''
    for line in open("E:\ownworkspace\python-spider-master\python-spider\data\provinceNcpData.txt", "r", encoding='utf-8'):  # 设置文件对象并读取每一行文件
        if line != '':
            k = k + line
    count = 0
    speechtext = SpeechText(k, 5, 3, count)
    speechtext.speech()
    files = []
    files = walkFile('./data/')
    for file in files:
        playsound(file)

if __name__ == '__main__':
    # speechtext()
    speechncp()