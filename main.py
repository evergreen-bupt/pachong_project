# <<<<<<< Updated upstream
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time
import random


def download_modle(tr_list, browser):
    num = 0
    for i in range(1, len(tr_lsit)):
        td_list = tr_lsit[i].find_elements(By.TAG_NAME, 'td')
        if td_list[2].text == '进行中':
            task_name=td_list[1].text
            num = 1

            s1 = browser.find_element(By.XPATH, f'//*[@id="root"]/div/div/section/section/main/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/table/tbody/tr[{i+1}]/td[12]/div/div/div[2]/button')
            s1.click()
            time.sleep(3)
            t1 = browser.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/table/tbody')
            tr1_list = t1.find_elements(By.TAG_NAME, 'tr')
            task_time=browser.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[2]/td[1]').text
            s2 = browser.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[2]/td[3]/div/div/div[2]/span/button')
            s2.click()
            time.sleep(3)
            input1_s2 = browser.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div/div[2]/form/div/div[1]/div[1]/div[2]/div[1]/div/span/input')
            model_name=task_name+'_'+str(cnt)
            input1_s2.send_keys(model_name)
            input2_s2 = browser.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div/div[2]/form/div/div[1]/div[4]/div[2]/div/div/div/textarea')
            input2_s2.send_keys(task_name+'_'+task_time)
            time.sleep(2)
            s3 = browser.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div/div[2]/form/div/div[2]/div/div[1]/span/button')
            s3.click()
            time.sleep(3)
            break #找到一个就break
            #TODO：修改为两个的版本
    return model_name
def eval_model(model_to_eval,browser):
    baseline_name='baseline_3'
    eval_num=5
    table = browser.find_element(By.XPATH,
                                 '/html/body/div/div/div/section/section/main/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/table')
    time.sleep(1)
    tr_lsit = table.find_elements(By.TAG_NAME, 'tr')
    for i in range(1, len(tr_lsit)):
        td_list = tr_lsit[i].find_elements(By.TAG_NAME, 'td')
        for model_name in model_to_eval:
            if td_list[1].text == model_name:
                if td_list[3].text=='检测成功':
                    s1=browser.find_element(By.XPATH,f'//*[@id="root"]/div/div/section/section/main/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[{i}]/td[12]/div/div/div[1]/span/button/span')
                    s1.click()
                    time.sleep(1)
                    eval_input1_s2=browser.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/div/div/div[2]/form/div/div[1]/div[5]/div[2]/div[1]/div/span/input')
                    eval_input1_s2.send_keys(model_name)
                    eval_select1_element=browser.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/div/div/div[2]/form/div/div[1]/div[7]/div[2]/div/div/div/div[2]/div[2]/div[1]/div/span/div/div/div[1]')
                    # eval_select1_element.click()
                    # 使用键盘上下箭头键浏览选项
                    eval_select1_option=browser.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/div/div/div[2]/form/div/div[1]/div[7]/div[2]/div/div/div/div[2]/div[2]/div[1]/div/span/div/div/div[1]/div/div/input')
                    eval_select1_option.click()
                    #选择评估阵容
                    for i in range(3):
                        eval_select1_option.send_keys(Keys.ARROW_DOWN)
                        # 使用回车键选择选项
                        eval_select1_option.send_keys(Keys.ENTER)
                    #选择模型
                    eval_select2_element=browser.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/div/div/div[2]/form/div/div[1]/div[8]/div[2]/div/div/div/div[1]/div[2]/div/div/span/div/div/span[1]/input')
                    eval_select2_element.click()
                    time.sleep(1)
                    eval_select2_element.send_keys(Keys.TAB)
                    time.sleep(1)
                    activate_element=browser.switch_to.active_element
                    activate_element.send_keys(baseline_name)
                    # activate_element.send_keys(Keys.ENTER)
                    # eval_select2_element.send_keys(baseline_name)
                    eval_select2_element.send_keys(Keys.ARROW_DOWN)
                        # 使用回车键选择选项
                    eval_select2_element.send_keys(Keys.ENTER)


                    eval_select3_element=browser.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/div/div/div[2]/form/div/div[1]/div[8]/div[2]/div/div/div/div[2]/div[2]/div/div/span/div/div/div[1]/div/div/input')
                    eval_select3_element.click()
                    for i in range(3):
                        eval_select3_element.send_keys(Keys.ARROW_DOWN)
                        # 使用回车键选择选项
                        eval_select3_element.send_keys(Keys.ENTER)
                    s3=browser.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/div/div/div[2]/form/div/div[1]/div[9]/div[2]/div/div/div/div[1]/div[2]/div/div/div/div/div[2]/input')
                    #删除现有轮数
                    s3.send_keys(Keys.CONTROL+'a')
                    s3.send_keys(Keys.DELETE)
                    s3.send_keys(eval_num)
                    s4=browser.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/div/div/div[2]/form/div/div[2]/div/div[1]/span/button')
                    s4.click()
                    eval_model_list.append(model_name)
                else:
                    continue




    return eval_model_list








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

num_train = 0
cnt=0
model_list=[]
eval_model_list=[]
while True:
    browser.get('https://aiarena.tencent.com/p/competition-exp/21/cluster-training') # 替换为目标网站的URL
    time.sleep(1)
    table = browser.find_element(By.XPATH, '//*[@id="root"]/div/div/section/section/main/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/table/tbody')
    tr_lsit = table.find_elements(By.TAG_NAME, 'tr')
    time.sleep(3)
    model_name=download_modle(tr_lsit, browser)
    model_list.append(model_name)
    cnt+=1
    browser.get('https://aiarena.tencent.com/p/competition-exp/21/model-manage')
    time.sleep(1)
    model_to_eval=[x for x in model_list if x not in eval_model_list]
    eval_model_list=eval_model(model_to_eval,browser)
    time.sleep(600)
    if cnt>5:
        break  #just for test
print(eval_model_list)
browser.quit()
