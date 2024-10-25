import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import posixpath
from lxml import etree
from to_csv import to_csv


def get_cookies(driver):
    # 打开小红书主页并手动登录,抓取cookie
    driver.get("https://www.xiaohongshu.com/explore")
    time.sleep(5)

    time.sleep(40)  # 给用户足够的时间手动登录
    # 获取登录后的 cookie
    cookies = driver.get_cookies()

    # 打印当前工作目录
    print("Current working directory: ", os.getcwd())

    # 将 cookie 保存到文件
    with open("cookies.json", "w") as file:
        json.dump(cookies, file)
    print("Cookies saved successfully.")

    driver.quit()


def get_html(driver,home_url,key_url):
    # 打开小红书主页
    driver.get(home_url)
    time.sleep(5)

    # 从文件加载 cookie
    with open("cookies.json", "r") as file:
        cookies = json.load(file)

    # 注入 cookie
    for cookie in cookies:
        driver.add_cookie(cookie)
    time.sleep(5)
    driver.refresh()  # 刷新页面以加载注入的 cookie
    time.sleep(5)  # 等待页面加载

    driver.get(key_url)
    time.sleep(5)  # 等待页面加载

    html_data = Page_Scrolling(driver)  #滚动到页面底部，并获取页面数据

    # # 获取整个页面的HTML源代码
    # page_source = driver.page_source
    # # 打开或创建一个txt文件并写入
    # with open("html.txt", "w", encoding="utf-8") as file:
    #     file.write(page_source)
    # # 打印页面的HTML
    # # print(page_source)
    # # time.sleep(30)  # 等待页面加载
    # driver.quit()

    return html_data


def Page_Scrolling(driver):
    # 获取初始页面高度
    last_height = driver.execute_script("return document.body.scrollHeight")
    data = []
    while True:
        # 滚动到页面底部
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # 等待页面加载
        time.sleep(2)
        # 获取整个页面的HTML源代码
        html = driver.page_source
        # 解析首页HTML
        tree = etree.HTML(html)
        x = 1
        while True:
            # 使用XPath提取数据
            title = tree.xpath(f'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[5]/section[{x}]/div/div/a/span/text()')
            links = tree.xpath(f'//*[@id="global"]/div[2]/div[2]/div/div[5]/section[{x}]/div/a[2]/@href')
            footer_text = tree.xpath(f'//*[@id="global"]/div[2]/div[2]/div/div[5]/section[{x}]/div/div/div/a/@href')
            print(title)
            #判断是否为空数据
            if links != [] and footer_text != [] and title != []:
                links = ['https://www.xiaohongshu.com'+ links[0]]
                footer_text = ['https://www.xiaohongshu.com'+ footer_text[0]]
            else:
                break

            Temporary_data = title + links + footer_text
            if Temporary_data not in data:
                data.append(Temporary_data)
                x += 1
                print(title)
            else:
                break

        # data = data+html_Analysis(html)
        # 获取新的页面高度
        new_height = driver.execute_script("return document.body.scrollHeight")
        # 判断是否到达页面底部
        if new_height == last_height:
            break

        last_height = new_height
    return data

def html_Analysis(html):
    # 解析首页HTML
    tree = etree.HTML(html)
    data = []
    x = 1
    while True:
        try:
            # 使用XPath提取数据
            title = tree.xpath(f'/html/body/div[1]/div[1]/div[2]/div[2]/div/div[5]/section[{x}]/div/div/a/span/text()')
            links = tree.xpath(f'//*[@id="global"]/div[2]/div[2]/div/div[5]/section[{x}]/div/a[2]/@href')
            footer_text = tree.xpath(f'//*[@id="global"]/div[2]/div[2]/div/div[5]/section[{x}]/div/div/div/a/@href')
            if title != []:
                data.append(title + links + footer_text)
                # data.append(title)
                # print(title)
                x += 1
            else:
                break
        except:
            break
    return data


# 设置 ChromeDriver 路径(替换成你自己的路径)
chrome_driver_path = "E:\Chrome driver\chromedriver-win64\chromedriver.exe"
home_url = "https://www.xiaohongshu.com/explore"
key_url = "https://www.xiaohongshu.com/search_result/?keyword=重庆租房"
header = ['主页标题','笔记连接','作者首页']

# 配置 Chrome 选项
options = Options()
# options.add_argument("--headless")      #无头模式（获取cookie需注释）
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(service=Service(executable_path=chrome_driver_path), options=options)

# get_cookies(driver)     #获取cookie文件

html_data = get_html(driver,home_url,key_url)

print(html_data)
print(len(html_data))

to_csv(header,html_data)