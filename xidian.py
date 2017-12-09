from tkinter import *
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

class win():
    def __init__(self):
        self.root=Tk()
        self.root.geometry('400x400')
        self.root.title('西电生活查询')#标题
        self.createWidgets()#创建窗口

    def  createWidgets(self):
        #主界面美化
        Label1=Label(text=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        Label1.pack()
       #使时间动起来
        def trickit():
            currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            Label1.config(text=currentTime)
            self.root.update()
            Label1.after(1000, trickit)
        Label1.after(1000,trickit)
        #创建菜单
        menu = Menu(self.root)
        self.root.config(menu=menu)
        functionMenu = Menu(menu)
        aboutMenu = Menu(menu)
        menu.add_cascade(label="查询", menu=functionMenu)
        functionMenu.add_command(label="物理实验查询", command=self.f1)
        functionMenu.add_command(label="图书馆借书查询", command=self.f2)
        functionMenu.add_command(label="成绩查询", command=self.f3)
        functionMenu.add_command(label="流量查询", command=self.f4)
        functionMenu.add_separator()
        functionMenu.add_command(label="退出", command=self.root.quit)
        menu.add_cascade(label="关于", menu=aboutMenu)
        aboutMenu.add_command(label="制作", command=self.info)


    def f1(self):
        #物理实验查询函数
        def searth():
            id = name.get()
            pass_word = password.get()
            if len(id) != 0 and len(pass_word) != 0:
                url = 'http://wlsy.xidian.edu.cn/PhyEws/default.aspx'
                r = requests.get(url)
                soup = BeautifulSoup(r.content, 'html.parser')
                value1 = soup.find(attrs={"name": "__VIEWSTATE"})['value']
                value2 = soup.find(attrs={"name": "__VIEWSTATEGENERATOR"})['value']
                value3 = soup.find(attrs={"name": "__EVENTVALIDATION"})['value']
                header = {
                    'Host': 'wlsy.xidian.edu.cn',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                    'Accept-Encoding': 'gzip, deflate',
                    'Referer': 'http://wlsy.xidian.edu.cn/PhyEws/default.aspx',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Content-Length': '150',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'DNT': '1'
                }
                data = {
                    '__EVENTTARGET': '',
                    '__EVENTARGUMENT': '',
                    '__VIEWSTATE': value1,
                    '__VIEWSTATEGENERATOR': value2,
                    '__EVENTVALIDATION': value3,
                    'login1$StuLoginID': id,
                    'login1$StuPassword': pass_word,
                    'login1$UserRole': 'Student',
                    'login1$btnLogin.x': '14',
                    'login1$btnLogin.y': '11'
                }
                #输出界面
                labelsFrame = LabelFrame(root2, text='物理实验情况:')
                labelsFrame.pack(fill="both", expand="yes")
                s = requests.session()
                response=s.post(url, data=data, headers=header)
                #判断获取状态
                if response.url=='http://wlsy.xidian.edu.cn/PhyEws/student/student.aspx':
                    r = s.get(url='http://wlsy.xidian.edu.cn/PhyEws/student/select.aspx')
                    soup2 = BeautifulSoup(r.content, 'html.parser')
                    for i in soup2.find_all('a', class_="linkSmallBold", target="_new"):
                        if '基础物理实验' not in i.string and '综合设计性物理实验' not in i.string and '下载' not in i.string:
                            Label(labelsFrame,text=i.string).grid(column=0)
                else:
                    messagebox.showinfo('warning!', '获取失败！！')
            else:
                messagebox.showinfo('warning!','请输入账号和密码')

        #次界面创建（下面同理）
        root2=Toplevel(self.root)
        label1=Label(root2,text='账号：')
        label1.pack()
        name=StringVar()
        anmeEntry=Entry(root2,textvariable=name)
        anmeEntry.pack()
        label2=Label(root2,text='密码：')
        label2.pack()
        password=StringVar()
        passwordEntry=Entry(root2,textvariable=password,show='*')
        passwordEntry.pack()
        button=Button(root2,text='确定',command=searth)
        button.pack()

#图书馆借书查询
    def f2(self):
        def searth():
            if len(name.get())!=0 and len(password.get())!=0:
                labelsFrame = LabelFrame(root2, text='借书情况:')
                labelsFrame.pack(fill="both", expand="yes")

                data = {
                    'func': 'login-session',
                    'login_source': 'bor_info',
                    'bor_id': name.get(),
                    'bor_verification': password.get(),
                    'bor_library': 'XDU50'
                }
                header = {
                    'Host': 'al.lib.xidian.edu.cn',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'
                }

                baseurl = 'http://al.lib.xidian.edu.cn/F/'
                try:
                    r = requests.get(baseurl)
                    soup = BeautifulSoup(r.content, 'html.parser')
                    for i in soup.find_all('a', title="输入用户名和密码"):
                        pattern = re.compile('href="(.*?)"')
                        for j in re.findall(pattern, str(i)):
                            url = j
                except:
                    url=''
                    messagebox.showinfo('Waring!','获取失败')
                # info储存书与时间
                info = {}
                book_list = []
                time_list = []
                s = requests.session()
                response=s.post(url, data=data, headers=header)
                info_url = url.replace('?func=file&amp;file_name=login-session',
                                       '?func=bor-loan&adm_library=XDU50')  # info_url为借书信息页面
                if response.url==url:
                    r = s.get(info_url)
                    soup = BeautifulSoup(r.content, 'html.parser')
                    for i in soup.find_all('a', target='_blank'):
                        if '热门信息' not in i.string:
                            book_list.append(i.string)
                    for j in soup.find_all('td', class_='td1', valign='top', width='10%'):
                        if j.string is not None:
                            if len(j.string) == 8:
                                time_list.append(j.string)
                    # 分别储存
                    if len(book_list) == len(time_list):
                        for i in range(0, len(book_list)):
                            Label(labelsFrame, text=book_list[i]).grid(column=0, row=i)
                            Label(labelsFrame, text=time_list[i]).grid(column=1, row=i)
                else:
                        messagebox.showinfo('Warning!','获取失败')
            else:
                messagebox.showinfo('warning!', '请输入账号和密码')

        root2=Toplevel(self.root)
        label1=Label(root2,text='账号：')
        label1.pack()
        name=StringVar()
        anmeEntry=Entry(root2,textvariable=name)
        anmeEntry.pack()
        label2=Label(root2,text='密码：')
        label2.pack()
        password=StringVar()
        passwordEntry=Entry(root2,textvariable=password,show='*')
        passwordEntry.pack()
        button=Button(root2,text='确定',command=searth)
        button.pack()
#成绩查询
    def f3(self):
        def searth():
            if len(name.get())!=0 and len(password.get())!=0:
                labelsFrame = LabelFrame(root2, text='成绩情况:')
                labelsFrame.pack(fill="both", expand="yes")
                web = webdriver.PhantomJS()
                web.set_page_load_timeout(5)
                try:
                    web.get('http://ids.xidian.edu.cn/authserver/login?service=http%3A%2F%2Fjwxt.xidian.edu.cn%2Fcaslogin.jsp')
                    element1 = web.find_element_by_name('username')
                    element2 = web.find_element_by_name('password')
                    element1.send_keys(name.get())
                    element2.send_keys(password.get())
                    element = web.find_element_by_name('submit')
                    element.submit()
                    time.sleep(1)
                    web.refresh()
                    if web.current_url == 'http://jwxt.xidian.edu.cn/caslogin.jsp':
                        web.get('http://jwxt.xidian.edu.cn/gradeLnAllAction.do?type=ln&oper=qbinfo')
                        html = web.execute_script("return document.documentElement.outerHTML")
                        soup = BeautifulSoup(html, 'html.parser')
                        web.quit()
                        grade = []
                        myclass = []
                        for i in soup.find_all('p', align='center'):
                            grade.append(i.string)
                        for i in soup.find_all('td', align='center'):
                            myclass.append(
                                str(i.string).replace('\n', '').replace('\t', '').replace('\xa0', '').replace(' ', ''))
                        for i in range(0, int(len(myclass) / 7)):
                            Label(labelsFrame, text=myclass[2 + i * 7]).grid(column=0, row=i)
                            Label(labelsFrame, text=myclass[4 + i * 7]).grid(column=1, row=i)
                            Label(labelsFrame, text=myclass[5 + i * 7]).grid(column=2, row=i)
                            Label(labelsFrame, text=grade[i]).grid(column=3, row=i)
                    else:
                        messagebox.showinfo('Warning', '获取失败')
                except:
                    messagebox.showinfo('Warning','连接超时')
            else:
                messagebox.showinfo('warning!', '请输入账号和密码')


        root2=Toplevel(self.root)
        label1=Label(root2,text='账号：')
        label1.pack()
        name=StringVar()
        anmeEntry=Entry(root2,textvariable=name)
        anmeEntry.pack()
        label2=Label(root2,text='密码：')
        label2.pack()
        password=StringVar()
        passwordEntry=Entry(root2,textvariable=password,show='*')
        passwordEntry.pack()
        button=Button(root2,text='确定',command=searth)
        button.pack()
#流量查询
    def f4(self):
        def searth():
            if len(name.get()) != 0 and len(password.get()) != 0:
                web.maximize_window()
                web.get('http://zfw.xidian.edu.cn/')
                element1 = web.find_element_by_name('LoginForm[username]')
                element2 = web.find_element_by_name('LoginForm[password]')
                element3 = web.find_element_by_name('LoginForm[verifyCode]')
                element1.send_keys(name.get())
                element2.send_keys(password.get())
                element3.send_keys(verify.get())
                submit = web.find_element_by_name('login-button')
                submit.submit()
                time.sleep(0.4)
                web.refresh()
                if web.current_url=='http://zfw.xidian.edu.cn/home':
                    web.get('http://zfw.xidian.edu.cn/home')
                    labelsFrame = LabelFrame(root2, text='流量情况:')
                    labelsFrame.pack(fill="both", expand="yes")
                    html = web.execute_script("return document.documentElement.outerHTML")
                    soup = BeautifulSoup(html, 'html.parser')
                    web.quit()
                    for i in soup.find_all('td', attrs={'data-col-seq': '1'}):
                        Label(labelsFrame, text=i.string).grid(column=0, row=0)
                    for i in soup.find_all('td', attrs={'data-col-seq': '7'}):
                        Label(labelsFrame, text=i.string).grid(column=0, row=1)
                else:
                    messagebox.showinfo('Warning','获取失败')
            else:
                messagebox.showinfo('warning!', '请输入账号和密码')


        imgine_url = 'http://zfw.xidian.edu.cn/site/captcha?v=59d5cfddb0cef'
        web = webdriver.PhantomJS()
        web.set_page_load_timeout(5)
        web.get(imgine_url)
        web.set_window_size(100, 50)
        web.get_screenshot_as_file('verify.png')
        root2 = Toplevel(self.root)
        im = PhotoImage(file='verify.png')
        lable = Label(root2, image=im)
        lable.pack()
        verify = StringVar()
        entry = Entry(root2, textvariable=verify)
        entry.pack()
        label1=Label(root2,text='账号：')
        label1.pack()
        name=StringVar()
        anmeEntry=Entry(root2,textvariable=name)
        anmeEntry.pack()
        label2=Label(root2,text='密码：')
        label2.pack()
        password=StringVar()
        passwordEntry=Entry(root2,textvariable=password,show='*')
        passwordEntry.pack()
        button=Button(root2,text='确定',command=searth)
        button.pack()

#制作信息
    def info(self):
            messagebox.showinfo("Info", "Made by Chun")
#运行
if __name__=='__main__':
    win=win()
    win.root.mainloop()
