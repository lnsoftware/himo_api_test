import pytest
from selenium import webdriver
from py._xmlgen import html

driver = None


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """当测试失败的时候，自动截图，展示到html报告中"""
    outcome = yield
    pytest_html = item.config.pluginmanager.getplugin('html')

    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    # 如果你生成的是web ui自动化测试，请把下面的代码注释打开，否则无法生成错误截图
    # if report.when == 'call' or report.when == "setup":
    #     xfail = hasattr(report, 'wasxfail')
    #     if (report.skipped and xfail) or (report.failed and not xfail):  # 失败截图
    #         file_name = report.nodeid.replace("::", "_") + ".png"
    #         screen_img = capture_screenshot()
    #         if file_name:
    #             html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:600px;height:300px;" ' \
    #                    'onclick="window.open(this.src)" align="right"/></div>' % screen_img
    #             extra.append(pytest_html.extras.html(html))
    #     report.extra = extra
    extra.append(pytest_html.extras.text('some string', name='Different title'))
    report.description = str(item.function.__doc__)
    report.nodeid = report.nodeid.encode("utf-8").decode("utf-8")  # 解决乱码


def capture_screenshot():
    '''截图保存为base64'''
    return driver.get_screenshot_as_base64()


def pytest_configure(config):
    # 添加接口地址与项目名称
    config._metadata["项目名称"] = "缦图摄影APP接口自动化"
    # config._metadata['接口地址'] = ''
    # 删除Java_Home
    config._metadata.pop("JAVA_HOME")
    config._metadata.pop("Packages")
    config._metadata.pop("Plugins")


@pytest.mark.optionalhook
def pytest_html_results_summary(prefix):
    prefix.extend([html.p("所属部门: 缦图互联网小组")])
    prefix.extend([html.p("测试人员: 隐形")])


@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('Description'))
    cells.pop(-1)  # 删除link列


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(report.description))
    cells.pop(-1)  # 删除link列


@pytest.fixture(scope='session')
def driver():
    global driver
    print('------------open browser------------')
    driver = webdriver.Chrome()

    yield driver
    print('------------close browser------------')
    driver.quit()
