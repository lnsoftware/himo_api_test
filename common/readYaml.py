import yaml
import traceback
from yamlCase.YamlPath import ymlPath as path


class GettingDate(object):

    def __init__(self, filename=None):
        self.filename = filename
        self.f = open(path() + '\\' + self.filename, encoding='utf-8')
        self.y = yaml.load(self.f, Loader=yaml.FullLoader)

    def return_data(self):
        casename = list(self.y)  # 获取所有用例名称
        casedata = []
        for i in range(0, len(casename)):
            casedata.append(self.y[casename[i]])  # 获取当前用例名称下的用例参数数据
        return casename, casedata


if __name__ == '__main__':
    file = GettingDate('preferentialCode.yml')
    casename, casedata = file.return_data()
    for i in range(0, len(casename)):
        print(casename[i])
        print(casedata[0])
