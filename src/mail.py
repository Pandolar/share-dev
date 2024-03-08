# python3
# -- coding: utf-8 --
# -------------------------------
# @Author : Terry
# @File : mail.py
# @Time : 2024/3/8 16:30
# -------------------------------
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
from email.utils import formataddr, parseaddr
import smtplib

class EmailTool:
    """
    邮件发送类
    """

    def __init__(self, smtp_server, smtp_port, user, password, from_):
        self.smtp_server = smtp_server  # 服务器地址  如smtp.163.com
        self.smtp_port = smtp_port  # 端口 如465
        self.user = user  # 系统账户 如xxxx@163.com
        self.password = password  # 系统密码 如xxxx
        self.from_ = from_  # 发送的邮箱(一般同user) 如xxxx@163.com

    def __format_addr(self, s):
        name, addr = parseaddr(f'{s.split("@")[0]}<{s}>')
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def send_email(self, sender, title='', content='', is_html=False, file_list=None):
        """
        :param sender: 发送目标 字符串类型, 如果多个目前请填写数组类型 ['xxx@x.com']
        :param title:  标题 字符串类型
        :param content: 内容 字符串类型
        :param is_html:  是否为html 布尔类型
        :param file_list: 附件列表 数组类型 ['1.txt']
        :return:
        """
        try:
            # 创建一个带附件的实例
            msg = MIMEMultipart()
            # 发件人格式
            msg['From'] = formataddr(["ops", self.user])
            # 收件人格式
            msg['To'] = ','.join(list(map(self.__format_addr, sender)))
            # 邮件主题
            msg['Subject'] = title
            # 邮件正文内容
            if is_html:
                part = MIMEText(content, 'html', 'utf-8')
            else:
                part = MIMEText(content, 'plain', 'utf-8')
            msg.attach(part)
            # 多个附件
            for file_name in file_list:
                print("file_name", file_name)
                # 构造附件
                xlsxpart = MIMEApplication(open(file_name, 'rb').read())
                # filename表示邮件中显示的附件名
                xlsxpart.add_header('Content-Disposition', 'attachment', filename='%s' % file_name)
                msg.attach(xlsxpart)

            # SMTP服务器
            server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, timeout=10)
            # 登录账户
            server.login(self.user, self.password)
            # 发送邮件
            server.sendmail(from_addr=self.user, to_addrs=sender, msg=msg.as_string())
            # 退出账户
            server.quit()
            print(f'<{title}>邮件发送成功')
            return True
        except smtplib.SMTPRecipientsRefused:
            raise Exception("邮件发送失败，收件人被拒绝")
        except smtplib.SMTPAuthenticationError:
            raise Exception('邮件发送失败，认证错误')
        except smtplib.SMTPSenderRefused:
            raise Exception('邮件发送失败，发件人被拒绝')
        except Exception as e:
            raise Exception("邮件发送失败，原因：" + str(e))