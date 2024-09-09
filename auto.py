import json
import threading
import time
import requests
from refresh_Cookie import RefreshCookie


lock = threading.Lock()
# condition = threading.Condition(lock)
#
# is_refreshing = False

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': '',
    'Referer': 'https://yjsxk.buaa.edu.cn/yjsxkapp/sys/xsxkappbuaa/course.html',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

courses = [
    {"name": "深度学习", "bjdm": "20241-010600-D061251002-1720060759837"},
    # {"name": "图形学", "bjdm": "20241-010600-D061251003-1720172763411"},
    # {"name": "并行处理", "bjdm": "20241-010600-D061241001-1720060590844"},
    # {"name": "科学计算", "bjdm": "20241-010600-D061042006-1720060472448", "fromKzwid": "4c7fc670f95b4fd28fe57795da212568"},
    # {"name": "视频编码", "bjdm": "20241-010600-D061042007-1720172762493"},
    # {"name": "信息检索", "bjdm": "20241-010600-D061042008-1720172762723", "fromKzwid": "4c7fc670f95b4fd28fe57795da212568"},
]

wait = 0.5

def get_token():
    response = requests.get(
        'https://yjsxk.buaa.edu.cn/yjsxkapp/sys/xsxkappbuaa/xsxkHome/loadPublicInfo_course.do',
        headers=headers,
    )
    token = response.json()["csrfToken"]
    print("token: " + token)
    return token


def run(course):
    global token
    token = get_token()
    while True:
        data = {
            'bjdm': course["bjdm"],
            'lx': '2',
            'csrfToken': token
        }
        if "fromKzwid" in course:
            data["fromKzwid"] = course["fromKzwid"]
        response = requests.post(
            'https://yjsxk.buaa.edu.cn/yjsxkapp/sys/xsxkappbuaa/xsxkCourse/choiceCourse.do',
            headers=headers,
            data=data,
        )
        print(f"{course['name']}: \t{response.text}\t{time.ctime()}")
        if response.json()["msg"] == "页面已过期，请刷新页面后重试":
            token = get_token()
        if response.json()["code"] == 1:
            courses.remove(course)
            break
        time.sleep(wait)


class MyThread(threading.Thread):
    def __init__(self, course):
        threading.Thread.__init__(self)
        self.course = course

    def run(self):
        while True:
            try:
                run(self.course)
            except Exception as e:
                # print(f"Error: {e}")
                # 只有第一个线程能够刷新Cookie
                # 其他线程上锁至刷新成功
                with lock:
                    if self.course["name"] == courses[0]["name"]:
                        print("\n")
                        print("Refreshing Cookie...")
                        RefreshCookie.run()
                        print("\n")
                        headers["Cookie"] = open("Cookie.txt", "r").read()
                continue


if __name__ == "__main__":
    headers["Cookie"] = open("Cookie.txt", "r").read()
    for course in courses:
        MyThread(course).start()
        time.sleep(0.1)