import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import json
import os


# 设置 ChromeDriver 路径(替换成你自己的路径)
chrome_driver_path = "E:\Chrome driver\chromedriver-win64\chromedriver.exe"

# 配置 Chrome 选项
options = Options()
# options.add_argument("--headless")      #无头模式（获取cookie需注释）
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(service=Service(executable_path=chrome_driver_path), options=options)

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