# /bin/env python
# -*-coding:utf8-*-
import socket
import fcntl
import time
import struct
import smtplib
import urllib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from json import load
from urllib2 import urlopen

# 发送邮件的基本函数，参数依次如下
# smtp服务器地址、邮箱用户名，邮箱秘密，发件人地址，收件地址（列表的方式），邮件主题，邮件html内容


def sendEmail(smtpserver, username, password, sender, receiver, subject,
              msghtml):
    msgRoot = MIMEMultipart('related')
    msgRoot["To"] = ','.join(receiver)
    msgRoot["From"] = sender
    msgRoot['Subject'] = subject
    msgText = MIMEText(msghtml, 'html', 'utf-8')
    msgRoot.attach(msgText)
    # sendEmail
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msgRoot.as_string())
    smtp.quit()

# 检查网络连同性


def check_network():
    while True:
        try:
            result = urllib.urlopen('http://baidu.com').read()
            print result
            print "Network is Ready!"
            break
        except Exception, e:
            print e
            print "Network is not ready,Sleep 5s...."
            time.sleep(5)
    return True

# 获取最新的外网IP


def get_ip_address():
    ipaddr = load(urlopen('http://httpbin.org/ip'))['origin']
    return ipaddr

# 将最新的外网IP写入到ip.txt中


def write_to_file():
    ipaddr = get_ip_address()
    with open("ip.txt", "w") as text_file:
        text_file.write(ipaddr)

# 比较ip是否一致


def compare_ip_diff(storedIp, currentIp):
    if storedIp != currentIp:
        return True
    else:
        return False

# 读取老ip


def read_stored_ip():
    with open("ip.txt", "r") as ipfile:
        data = ipfile.read()
        return data

if __name__ == '__main__':
    # 延迟15秒执行，以防重启后网络没有立即连通
    time.sleep(15)
    check_network()
    currentIP = get_ip_address()
    storedIP = read_stored_ip()
    if compare_ip_diff(storedIP, currentIP):
        message = u'Hi My Ip has changed from %s to %s' % (storedIP,currentIP)
        sendEmail('smtp.exmail.qq.com', 'shenlin@shenlin.im', 'MAZgg89dSuRzwcuv',
                  'shenlin@shenlin.im',
                  ['shenlinchou@outlook.com'],
                  'Home Public IP Address Notification', message)
        write_to_file()
        print 'File updated'
    else:
        print 'nothing changed'
