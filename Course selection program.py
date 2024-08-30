import threading

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
import random

class MyThread(threading.Thread):
    def __init__(self, username, password, classname1, classname2, classname3, selectname, pagenumber, coursecount, collage=''):
        threading.Thread.__init__(self)
        self.username = username
        self.password = password
        self.classname1 = classname1
        self.classname2 = classname2
        self.classname3 = classname3
        self.selectname = selectname
        self.pagenumber = pagenumber
        self.coursecount = coursecount
        self.collage = collage

    def run(self) -> None:
        while True:
            try:
                path = "chromedriver/chromedriver"

                opt = webdriver.ChromeOptions()
                # opt.add_argument('headless')
                opt.add_experimental_option("excludeSwitches",
                                            ['enable-automation', 'enable-logging'])
                driver = webdriver.Chrome(executable_path=path, options=opt)
                driver.get(r'http://jwxt.buaa.edu.cn:8080/ieas2.1/welcome?falg=1')
                time.sleep(3)
                frame = driver.find_element('id', 'loginIframe')
                driver.switch_to.frame(frame)
                driver.find_element(By.ID, 'unPassword').send_keys(self.username)
                driver.find_element(By.ID, 'pwPassword').send_keys(self.password)
                driver.find_element(By.CLASS_NAME, 'default-bgcolor').click()
                time.sleep(3)
                driver.find_elements(By.ID, 'menu_6')[0].click()  # 属于哪一个下拉菜单
                time.sleep(1)
                a = driver.find_elements(By.CLASS_NAME, 'text')
                for i in a:
                    if i.text == self.classname1:
                        i.click()
                time.sleep(1)
                frame = driver.find_element(By.ID, 'iframename')
                driver.switch_to.frame(frame)
                urls = driver.find_elements(By.XPATH, "//a")
                for url in urls:
                    if url.text == self.classname2:
                        url.click()
                        break
                time.sleep(1)
                opt1 = driver.find_element(By.NAME, 'pageXnxq')
                Select(opt1).select_by_value(self.selectname)  # 哪一季度
                opt2 = driver.find_element(By.NAME, 'pageKkyx')
                Select(opt2).select_by_value(self.collage)  # 哪一学院
                driver.find_element(
                    By.XPATH, '//*[@id="queryform"]/ul/li[7]/div/a').click()
                time.sleep(1)
                pages = driver.find_elements(By.XPATH, "//a")
                for page in pages:
                    if page.text == str(self.pagenumber):
                        page.click()
                        break
                time.sleep(1)
                driver.switch_to.parent_frame()
                while True:
                    frame = driver.find_element(By.ID, 'iframename')
                    driver.switch_to.frame(frame)
                    b = driver.find_elements(By.XPATH, "//tbody/tr")
                    for class_name in self.classname3:
                        new_classname3 = self.classname3
                        flag = 0
                        for i in b:
                            need_tr = i
                            c = i.find_elements(By.XPATH, ".//a")
                            for j in c:
                                # print(j.text)
                                if j.text == class_name:
                                    flag += 1
                                    # j.click()
                                    break
                            if flag == self.coursecount:
                                print("已定位\"{}\"课程！".format(class_name))
                                break
                        if flag == 0:
                            print("未找到该课程！")
                            break
                        divs = need_tr.find_elements(By.XPATH, './/td')
                        # print("该课程信息为：")
                        for div in divs:
                            if div.text:
                                # print(div.text)
                                pass
                        print(str(divs[-1].text))
                        # if int(divs[-1].text.split('/')[0]) > 0:
                        if int(divs[-1].text.split(':')[1].split('/')[0]) > 0:
                        # if int(divs[-1].text.split('/')[0]) > int(divs[-1].text.split(':')[1].split('/')[0]):
                            span = need_tr.find_element(By.XPATH, './/span')
                            span.click()
                            try:
                                alert = driver.switch_to.alert
                                print(alert.text)
                                if alert.text == '选课成功':
                                    print("选课成功！！！")
                                    print("此刻时间：" + time.ctime())
                                    alert = driver.switch_to.alert  # 获取弹窗
                                    # print("弹窗文本:", alert.text)  # 获取弹窗文本
                                    alert.accept()  # 点击弹窗的确定按钮
                                    new_classname3 = [x for x in self.classname3 if x != class_name]
                            except:
                                pass
                    if len(self.classname3) != len(new_classname3):
                        break
                    # html = driver.page_source
                    # soup = BeautifulSoup(html, 'html.parser')
                    # f = open('1.txt', 'w', encoding='utf-8')
                    # f.write(str(soup))
                    driver.switch_to.parent_frame()
                    refresh = driver.find_element(By.ID, 'person_info2')
                    print(refresh.text)
                    # print(self.pagenumber)
                    refresh.click()
                    time.sleep(random.uniform(0, 1))
                # if flag == 0:
                #     break
                if len(self.classname3) != len(new_classname3):
                    self.classname3 = new_classname3
                    driver.close()
            except Exception as e:
                print(e)
                # driver.close()
            time.sleep(1)


####################################
### author:Tan


if __name__ == '__main__':
    # username = '20373861'       # 学生账号
    # password = 'Wanwan921'  # 密码
    # # username = 'gy20001218'       # 学生账号
    # # password = '123456qwe'  # 密码
    # # username = '20373864'       # 学生账号
    # # password = 'tanlide753951'  # 密码
    # classname1 = u'通识课程选课'  # 哪一大类
    # classname2 = '核心通识类'     # 哪一小类
    # classname3 = 'Android平台开发技术'  # 课程名字
    # selectname = '2022-20231'  # 哪一季度
    # pagenumber = 5  # 哪一页码
    # coursecount = 1  # 哪一位次
    # t1 = MyThread(username, password, classname1, classname2, classname3, selectname, pagenumber, coursecount)
    # t1.start()
    # # print("1111")
    # username = '20373862'       # 学生账号
    # password = 'dwk20020322'  # 密码
    # classname1 = u'专业课程选课'  # 哪一大类
    # classname2 = '一般专业类'     # 哪一小类
    # classname3 = 'Android平台开发技术'  # 课程名字
    # selectname = '2022-20231'  # 哪一季度
    # pagenumber = 5  # 哪一页码
    # coursecount = 1  # 哪一位次
    # t2 = MyThread(username, password, classname1, classname2, classname3, selectname, pagenumber, coursecount)
    # t2.start()

    username = '20373719'  # 学生账号
    password = '1887415157qwerty'  # 密码
    classname1 = u'专业课程选课'  # 哪一大类
    classname2 = '一般专业类'     # 哪一小类
    classname3 = ['救生与防护技术']  # 课程名字
    selectname = '2023-20241'  # 哪一季度
    pagenumber = 2  # 哪一页码
    coursecount = 1  # 哪一位次
    collage = '05'  # 哪一学院
    t2 = MyThread(username, password, classname1, classname2, classname3, selectname, pagenumber, coursecount, collage)
    t2.start()

    # username = '20373864'  # 学生账号
    # password = 'tanlide753951'  # 密码
    # classname1 = u'通识课程选课'  # 哪一大类
    # classname2 = '核心通识类'  # 哪一小类
    # classname3 = ['西方音乐史与名曲鉴赏', '中国现代文学三十年', '美学基础', '中国语文经典文本选读']  # 课程名字
    # selectname = '2023-20241'  # 哪一季度
    # pagenumber = 1  # 哪一页码
    # coursecount = 1  # 哪一位次
    # collage = '11'  # 哪一学院
    # t3 = MyThread(username, password, classname1, classname2, classname3, selectname, pagenumber, coursecount, collage)
    # t3.start()
    #
    # username = '20373864'  # 学生账号
    # password = 'tanlide753951'  # 密码
    # classname1 = u'专业课程选课'  # 哪一大类
    # classname2 = '一般专业类'  # 哪一小类
    # classname3 = ['信息系统与安全对抗技术', '信息安全工程', '信息系统与安全对抗技术', '图像处理与信息隐藏']  # 课程名字
    # selectname = '2023-20241'  # 哪一季度
    # pagenumber = 1  # 哪一页码
    # coursecount = 1  # 哪一位次
    # collage = '39'  # 哪一学院
    # t6 = MyThread(username, password, classname1, classname2, classname3, selectname, pagenumber, coursecount, collage)
    # t6.start()



    # username = '20373864'       # 学生账号
    # password = 'tanlide753951'  # 密码
    # classname1 = u'专业课程选课'  # 哪一大类
    # classname2 = '一般专业类'     # 哪一小类
    # classname3 = 'X86汇编程序设计'  # 课程名字
    # selectname = '2022-20232'  # 哪一季度
    # pagenumber = 8  # 哪一页码
    # coursecount = 1  # 哪一位次
    # t3 = MyThread(username, password, classname1, classname2, classname3, selectname, pagenumber, coursecount)
    # t3.start()
    # username = '20373864'       # 学生账号
    # password = 'tanlide753951'  # 密码
    # classname1 = u'专业课程选课'  # 哪一大类
    # classname2 = '核心专业类'  # 哪一小类
    # classname3 = '计算机网络'  # 课程名字
    # selectname = '2022-20232'  # 哪一季度
    # pagenumber = 7  # 哪一页码
    # coursecount = 2  # 哪一位次
    # t4 = MyThread(username, password, classname1, classname2, classname3, selectname, pagenumber, coursecount)
    # t4.start()
    # username = '20373719'  # 学生账号
    # password = '1887415157qwerty'  # 密码
    # classname1 = u'专业课程选课'  # 哪一大类
    # classname2 = '一般专业类'  # 哪一小类
    # classname3 = '软件项目管理'  # 课程名字
    # selectname = '2022-20232'  # 哪一季度
    # pagenumber = 9  # 哪一页码
    # coursecount = 1  # 哪一位次
    # t5 = MyThread(username, password, classname1, classname2, classname3, selectname, pagenumber, coursecount)
    # t5.start()
    # main(username, password, classname1, classname2, classname3, selectname, pagenumber)    # username = '20373934'       # 学生账号
    # password = 'heziyuan1888'  # 密码
    # classname1 = u'专业课程选课'  # 哪一大类
    # classname2 = '一般专业类'     # 哪一小类
    # classname3 = 'Android平台开发技术'  # 课程名字
    # selectname = '2022-20231'  # 哪一季度
    # pagenumber = 5  # 哪一页码
    # coursecount = 1  # 哪一位次
    # t3 = MyThread(username, password, classname1, classname2, classname3, selectname, pagenumber, coursecount)
    # t3.start()
    # main(username, password, classname1, classname2, classname3, selectname, pagenumber)

# html = driver.page_source
# soup = BeautifulSoup(html, 'html.parser')
# f = open('1.txt', 'w', encoding='utf-8')
# f.write(str(soup))
