import requests,time,smtplib,mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
#将课表发出
def sender():
    msg=MIMEMultipart()
    msg['From']='xiechunhui98@163.com'
    msg['to']='1194620498@qq.com'
    msg['Subject']='class_schedule'

    image=MIMEImage(open('class_schedule.gif','rb').read())
    image.add_header('Content-ID','<image1>')
    msg.attach(image)

    msg.attach(MIMEText('<html><body><h1>Class schedule</h1><p><img src=cid:image1></body></p></html>','html','utf-8'))

    server=smtplib.SMTP()
    server.connect('smtp.163.com')
    server.login('xiechunhui98@163.com','123abc')
    server.sendmail(msg['From'],msg['to'],msg.as_string())
    server.quit()

if __name__=="__main__":
    year=time.strftime("%Y",time.localtime())
    month=time.strftime("%m",time.localtime())
    if int(month)>7:
        mode='b'
    else:
        mode='a'
    Class=input("输入班级：")
    url=u'http://kb.xidian.cc/upload/picold/'+year+mode+'/'+Class+'.gif'
    try:
        r=requests.get(url)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        with open('class_schedule.gif','wb') as f:
            f.write(r.content)
    except:
        print("错误班级号，或服务器上已经没有相关文件")
    sender()