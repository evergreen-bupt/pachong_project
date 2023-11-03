from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time
import random

def download_modle(td_list, browser):
    num = 0
    for i in range(1, len(tr_lsit)):
        td_list = tr_lsit[i].find_elements(By.TAG_NAME, 'td')
        if td_list[2].text == '进行中':
            num = 1
            s1 = browser.find_element(By.XPATH, f'//*[@id="root"]/div/div/section/section/main/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/table/tbody/tr[{i+1}]/td[12]/div/div/div[2]/button')
            s1.click()
            time.sleep(3)
            t1 = browser.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/table/tbody')
            tr1_list = t1.find_elements(By.TAG_NAME, 'tr')
            for j in range(1, len(tr1_list), 2):
                random_number = random.random()
                k = j if random_number < 0.5 and j+1 <= len(tr1_list) else j+1##需要测试测试
                s2 = browser.find_element(By.XPATH, f'/html/body/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[{k+1}]/td[3]/div/div/div[2]/span/button')
                s2.click()                            
                time.sleep(3)
                input1_s2 = browser.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div/div[2]/form/div/div[1]/div[1]/div[2]/div[1]/div/span/input')
                input1_s2.send_keys('cb_test1')
                input2_s2 = browser.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div/div[2]/form/div/div[1]/div[4]/div[2]/div/div/div/textarea')
                input2_s2.send_keys('cb_test1')
                time.sleep(2)
                s3 = browser.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div/div[2]/form/div/div[2]/div/div[1]/span/button')
                s3.click()
                time.sleep(1)
                s4 = browser.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div/div[1]/div/button/span/svg')       
                s4.click()
                time.sleep(1)    
                s4.click()
    return num
# 初始化浏览器
browser = webdriver.Edge()
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
#PART2: 进入训练监控，获取模型指标信息，选择周围时间点模型。
# 查找上传文件输入框并上传文件
time.sleep(10)
num_train = 0
while(num_train!=2):
    table = browser.find_element(By.XPATH, '//*[@id="root"]/div/div/section/section/main/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/table/tbody')
    tr_lsit = table.find_elements(By.TAG_NAME, 'tr')
    num_train += download_modle(tr_lsit, browser)
    if num_train == 2 : break
    s = browser.find_element(By.XPATH,'//*[@id="root"]/div/div/section/section/main/div/div/div[2]/div/div/div/div/div[2]/div/div/ul/li[9]/button')

browser.quit()
