import os

class CommonUtils:
    def init(self,path):
        self.path = path
    # 遍历文件夹
    def walkFile(self):
        data = []
        for root, dirs, files in os.walk(self.path):
            # root 表示当前正在访问的文件夹路径
            # dirs 表示该文件夹下的子目录名list
            # files 表示该文件夹下的文件list
            # 遍历文件
            for f in files:
                path = os.path.join(root, f)
                if '.log' in path and 'toGov' in path:
                    data.append(path)
                    print(path)
        return data