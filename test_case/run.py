import os
from common.SendEmail import sendEmail


def pytest_allure():
    os.system('pytest --alluredir=../report/xml')
    # 生成allurehtml文件
    os.system('allure generate ../report/xml --clean -o ../html')


if __name__ == '__main__':
    pytest_allure()

    # 多线程执行pytestCase,生成pytest-html报告
    # os.system('pytest -s --html=../html_report/html_report.html --self-contained-html --workers=1 --tests-per-worker=4')

    # 发送邮件
    # sendEmail()
