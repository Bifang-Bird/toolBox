from logs.CommonUtils import CommonUtils
global x
x=0
data = []
rdata = []
def speechncp(path):
    # 第二种方法
    for line in open(path, "r", encoding='utf-8'):  # 设置文件对象并读取每一行文件
        if '向国标平台发送' in line  or '发送登录报文' in line:
            strList = line.split('msg=')
            if len(strList)<2:
                strList = line.split('[发送登录报文]=')
            vinhex = strList[1][8:42]
            ct = strList[1][48:60]
            data.append(vinhex+ct)
            global x
            x=x+1
        if '接收国标平台应答报文' in line:
            rstrList = line.split('msg=')
            rvinhex = rstrList[1][8:42]
            rct = rstrList[1][48:60]
            if rvinhex+rct in data:
                data.remove(rvinhex+rct)
            else:
                rdata.append(rvinhex+rct)

if __name__ == '__main__':
    path = "G:/辛巴文档/日志/zflogs"
    comUtils = CommonUtils()
    comUtils.init(path)
    files = comUtils.walkFile()
    for file in files:
        speechncp(file)
    fail= len(data) / x
    print ('已发送未反馈报文数：%d' %(len(data)),'已反馈未匹配到发送报文数：%d' %(len(rdata)),'发送失败率：%f' %(fail))