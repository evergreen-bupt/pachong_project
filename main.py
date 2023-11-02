from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time
TX_URL=''
# 初始化浏览器
browser = webdriver.Chrome()
#PART1:自动化登陆 打开登录页面
login_url = 'https://aiarena.tencent.com/p/user/login?redirect=https%3A%2F%2Faiarena.tencent.com%2Flogin'
browser.get(login_url)

# 输入用户名和密码
username = browser.find_element(By.ID,'basic_email')  # 替换为实际的用户名输入框定位方法
password = browser.find_element(By.ID, 'basic_password') # 替换为实际的密码输入框定位方法
submit = browser.find_element(By.XPATH,'//*[@id="basic"]/div[4]/div/div/div/span/button')
username.send_keys('609531932@qq.com')
password.send_keys('bupt151540809')
submit.click()
time.sleep(5)
browser.get('https://aiarena.tencent.com/p/competition-exp/21/cluster-training') # 替换为目标网站的URL
time.sleep(10)
#PART2: 进入训练监控，获取模型指标信息，选择周围时间点模型。
# 查找上传文件输入框并上传文件
table=browser.find_elements(By.XPATH,"//*[@class='ant-table-tbody']")
# 解析表格元素的HTML文档
soup = BeautifulSoup(table[0].get_attribute('innerHTML'), 'html.parser')
print(soup)
# 提取表格元素中的每一行数据
rows = soup.find_all('tr')
elements = browser.find_elements(By.XPATH,"//span[@class='ant-tag ant-tag-primary kuic-tag-point-primary']")
print(elements)
file_input = browser.find_element(By.ID, 'fileInput')  # 替换为实际的输入框ID或其他定位方法
file_path = 'path_to_your_file/model_script.py'  # 替换为实际文件路径
file_input.send_keys(file_path)

#PART3: 选择模型,自动提交评估任务
model_select = Select(browser.find_element(By.ID, 'modelSelect'))  # 替换为实际的下拉选择框ID或其他定位方法
model_select.select_by_value('model_option_value')  # 替换为实际模型选项值

# 点击提交按钮
submit_button = browser.find_element(By.ID, 'submitBtn')  # 替换为实际的提交按钮ID或其他定位方法
submit_button.click()

# 等待一段时间，以确保上传和选择操作完成
time.sleep(5)
#PART4： 提取评估结果，生成ELO分数，并返回下阶段预备训练模型
# 关闭浏览器
browser.quit()
