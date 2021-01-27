import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 第三方 SMTP 服务
mail_host = "smtp.qq.com"  # 设置服务器
mail_user = "897707849@qq.com"  # 用户名(你的邮箱)
mail_pass = "lholgkvemabgbfed"  # 口令,即开启smtp服务得到的授权码，不是QQ密码

sender = "897707849@qq.com"  # 发送者的邮箱(也是你的邮箱,同用户名)
receivers = ["897707849@qq.com"]  # 接收邮件，其他人邮箱

# 三个参数：第一个为文本内容，第二个为格式 plain 代表文本格式，第三个 utf-8 设置编码
report_path = '点击查看自动化测试报告\n自动化报告链接:http://10.20.222.255:8888/#'
message = MIMEText(report_path, "plain", "utf-8")

# 标准邮件需要三个头部信息： From, To, 和 Subject
message["From"] = Header("隐形", "utf-8")  # 发送人(名称)
message["To"] = Header("自动化测试报告", "utf-8")  # 接收人(名称)

subject = '自动化测试报告'
message['Subject'] = Header(subject, 'utf-8')  # 邮件主题

def sendEmail():
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
        smtpObj.quit()
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")


if __name__ == '__main__':
    sendEmail()


    '''
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        """
        但是这样我们用25号端口都是以明文发送的，很容易被监视，
        所以我们可以发送加密邮件，只需要利用SSL:
        smtpObj = smtplib.SMTP_SSL()
        smtpObj.connect(mail_host, 465)  # QQ邮箱的端口465或587
    
        SMTP和SMTP_SSL选择一个使用即可
        """
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
        smtpObj.quit()
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")
'''
