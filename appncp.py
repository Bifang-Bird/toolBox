import cx_Oracle #导入包
import datetime
from pyecharts import Bar,Line,EffectScatter,Overlap,Map, Geo


def getYesterday(i):
    today=datetime.date.today()
    oneday=datetime.timedelta(days=i)
    yesterday=today-oneday
    return yesterday
def action():
    keys = []
    val = []
    for i in range(1,7):
        # 连接数据库
        db = cx_Oracle.connect("cherymon/1q@W3e$R@tlmsrac.mychery.com:1521/cheryddc_taf")
        print(db.version) #打印版本看看 显示 11.2.0.1.0
        cur = db.cursor() # 游标操作
        sql="select a.userid ,sum(a.access_count) from ( select b.userid, b.code, b.access_date, count(1) as access_count from t_app_access_list b "+"where b.access_date = to_char(sysdate - "+str(i)+", 'yyyy-mm-dd') group by b.userid, b.access_date, b.code ) a where a.code='login' group by a.userid"
        print(sql)
        cur.execute(sql) # 执行sql语句
        rows = cur.fetchall() # 获取数据
        # 打印数据
        count=0
        for row in rows:
            count+=row[1]
            # print("用户ID:"+str(row[0])+"访问总数:"+str(row[1]))
        yesterday = getYesterday(i)
        print(str(yesterday)+"访问总数："+str(count))
        keys.append(str(yesterday))
        val.append(count)
    bar(keys,val)
    line(keys,val)
    lineeffect(keys,val)

def bar(keys,values):
    bar = Bar("我的第一个图表", "这里是副标题")
    #bar.add("app日活", keys,values,mark_point = ['average'])
    bar.add("app日活", keys,values,mark_line = ['min','max'])
    bar.show_config()
    bar.render('./bar01.html')
def line(attr,v1):
    line = Line('折线示例图')
    line.add('商家A', attr, v1,
             mark_point=['average', 'max', 'min'],  # 标注点：平均值，最大值，最小值
             mark_point_symbol='diamond',  # 标注点：钻石形状
             mark_point_textcolor='#40ff27')  # 标注点：标注文本颜色
    # line.add('商家B', attr, v2, mark_point=['average', 'max', 'min'],
    #          mark_point_symbol='arrow',
    #          mark_point_symbolsize=40)
    line.render('./line01.html')
def lineeffect(attr,val,val2):
    line = Line('芜湖新冠肺炎病例')
    line.add('确诊病例', attr, val, is_label_show=True)
    line.add("治愈病例", attr, val2, is_label_show=True)
    es = EffectScatter()
    es.add('', attr, val, effect_scale=8)  # 闪烁
    es.add('', attr, val2, effect_scale=8)  # 闪烁

    overlop = Overlap()
    overlop.add(line)  # 必须先添加line,在添加es
    overlop.add(es)
    overlop.render('./data/line-es01.html')

def citMap():
    # 河南地图  数据必须是省内放入城市名
    # 城市 -- 指定省的城市 xx市
    # city = ['合肥市', '蚌埠市', '阜阳市', '亳州市', '安庆市', '六安市', '宿州市', '马鞍山市', '芜湖市', '铜陵市', '淮南市', '淮北市', '池州市', '滁州市', '黄山市',
    #         '宣城市']
    # values2 = [150, 134, 132, 92, 80, 59, 33, 32, 31, 27, 24, 24, 15, 12, 9, 6]
    provinces = []
    values2 = []
    for line in open("E:\ownworkspace\python-spider-master\python-spider\data\provinceNcpnumData.txt", "r", encoding='utf-8'):  # 设置文件对象并读取每一行文件
        if line != '':
            datas = line.split(",")
            province = datas[0].replace("省",'').replace('市','').strip().replace(' ','').replace('自治区','').replace('维吾尔','').replace('壮族','').replace('回族','')
            provinces.append(province)
            numbers = datas[1].replace(' ','')
            values2.append(numbers)

    map2 = Map("中国新冠肺炎地图", '中国新冠肺炎地图', width='100%', height=750)
    map2.add('中国新冠肺炎', provinces, values2, visual_range=[1, 5000], maptype='china', is_visualmap=True, visual_text_color='#000')
    map2.show_config()
    map2.render(path="./data/04-02地图.html")

def cityMap():
    indexs = ['上海', '北京', '合肥', '哈尔滨', '广州', '成都', '无锡', '杭州', '武汉', '深圳', '西安', '郑州', '重庆', '长沙']
    values = [4.07, 1.85, 4.38, 2.21, 3.53, 4.37, 1.38, 4.29, 4.1, 1.31, 3.92, 4.47, 2.40, 3.60]
    geo = Geo("全国主要城市空气质量评分", "data from pm2.5", title_color="#fff", title_pos="center", width='100%', height=750,
              background_color='#404a59')
    # type="effectScatter", is_random=True, effect_scale=5  使点具有发散性
    geo.add("空气质量评分", indexs, values, type="effectScatter", is_random=True, effect_scale=5, visual_range=[0, 5],
            visual_text_color="#fff", symbol_size=15, is_visualmap=True, is_roam=False)
    geo.show_config()
    geo.render(path="./data/04-05空气质量评分.html")

if __name__ == '__main__':
        #action();
        citMap();
        cityMap();
        attr = ['2月1号', '2月2号', '2月3号', '2月4号', '2月5号', '2月6号','2月7号','2月8号','2月9号','2月10号', '2月11号','2月12号','2月13号']
        val = [16, 16, 21, 23, 26, 27, 29, 29, 30, 31, 31, 31, 31]
        val2 = [0, 0, 1, 1, 2, 2, 3, 3, 3, 3, 4, 4, 5]
        lineeffect(attr,val,val2)