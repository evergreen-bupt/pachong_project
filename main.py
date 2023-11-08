# <<<<<<< Updated upstream
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time


EVAL_NUM = 1

class pa_chong():
    def __init__(self):
        self.last_name = ['11h2min18s', '19h14min24s']
        self.num_train = 0
        self.model_list = []
        self.eval_model_list = ['Update-vjw_10h', 'Update-v6-17h']
        self.last_name_counts = {'test_pr1':0, 'Update-v6-1':0}
        self.emeny = 'baseline-3'
        self.eval_task_list = ['udv617_t3', 'udv617_t22']
        self.time = 3
        self.eval_result_dict = {}
    
    def go(self):
        # 初始化浏览器
        self.browser = webdriver.Chrome()
        #PART1:自动化登陆 打开登录页面
        login_url = 'https://aiarena.tencent.com/p/user/login?redirect=https%3A%2F%2Faiarena.tencent.com%2Flogin'
        self.browser.get(login_url)
        # 输入用户名和密码
        username = self.browser.find_element(By.ID,'basic_email')  # 替换为实际的用户名输入框定位方法
        password = self.browser.find_element(By.ID, 'basic_password') # 替换为实际的密码输入框定位方法
        submit = self.browser.find_element(By.XPATH,'//*[@id="basic"]/div[4]/div/div/div/span/button')
        username.send_keys('609531932@qq.com')
        password.send_keys('bupt151540809')
        submit.click()
        time.sleep(5)
        while True:
            '''self.download_modle()
            time.sleep(3)'''
            self.eval_model()
            time.sleep(3)
            self.eval_result()
            time.sleep(self.time)

    def download_modle(self):
        task_num = 0
        for i in range(1, 11):
            self.browser.get('https://aiarena.tencent.com/p/competition-exp/21/cluster-training') # 替换为目标网站的URL
            time.sleep(3)
            table = self.browser.find_element(By.XPATH, '//*[@id="root"]/div/div/section/section/main/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/table/tbody')
            tr_list = table.find_elements(By.TAG_NAME, 'tr')
            td_list = tr_list[i].find_elements(By.TAG_NAME, 'td')
            if td_list[2].text == '进行中':
                task_num += 1
                task_name = td_list[1].text
                if task_name not in self.last_name_counts:
                    self.last_name_counts[task_name] = 0
                    self.last_name[task_num - 1] = None
                j, name = 0, None
                while(True):
                    self.browser.find_element(By.XPATH, 
                    f'//*[@id="root"]/div/div/section/section/main/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/table/tbody/tr[{i+1}]/td[12]/div/div/div[2]/button').click()
                    time.sleep(3)
                    t1 = self.browser.find_element(By.XPATH, 
                                                    '/html/body/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/table/tbody')
                    tr1_list = t1.find_elements(By.TAG_NAME, 'tr')
                    td1_list = tr1_list[j+1].find_elements(By.TAG_NAME, 'td')
                    if td1_list[0].text == self.last_name[task_num - 1]:break
                    self.last_name_counts[task_name] += 1
                    name = tr1_list[1].find_elements(By.TAG_NAME, 'td')[0].text
                    self.browser.find_element(By.XPATH, 
                        f'/html/body/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[{j+2}]/td[3]/div/div/div[2]/span/button').click()
                    time.sleep(3)
                    input1_s2 = self.browser.find_element(By.XPATH, 
                                                            '/html/body/div[3]/div/div[2]/div/div/div[2]/form/div/div[1]/div[1]/div[2]/div[1]/div/span/input')
                    model_name = task_name +'_'+ str(self.last_name_counts[task_name])
                    input1_s2.send_keys(model_name)
                    input2_s2 = self.browser.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div/div[2]/form/div/div[1]/div[4]/div[2]/div/div/div/textarea')
                    input2_s2.send_keys(task_name +'_'+ td1_list[0].text)
                    time.sleep(2)
                    self.browser.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div/div[2]/form/div/div[2]/div/div[1]/span/button').click()
                    time.sleep(3)
                    self.model_list.append(model_name)
                    self.browser.get('https://aiarena.tencent.com/p/competition-exp/21/cluster-training')
                    time.sleep(3)
                    j += 1
                    if j == len(tr1_list):break
                self.last_name[task_num - 1] = name
            if task_num == 2:break
    
    def eval_model(self):
        if len(self.model_list) == 0:return
        self.browser.get('https://aiarena.tencent.com/p/competition-exp/21/model-manage')
        time.sleep(3)
        model_to_eval = list(self.model_list)
        table = self.browser.find_element(By.XPATH,
                                    '/html/body/div/div/div/section/section/main/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/table')
        tr_list = table.find_elements(By.TAG_NAME, 'tr')
        for i in range(1, len(tr_list)):
            time.sleep(3)
            td_list = tr_list[i].find_elements(By.TAG_NAME, 'td')
            if td_list[1].text in model_to_eval:
                model_name = td_list[1].text
                
                if td_list[3].text == '检测失败':continue

                self.browser.find_element(By.XPATH,f'//*[@id="root"]/div/div/section/section/main/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[{i}]/td[12]/div/div/div[1]/span/button/span').click()
                time.sleep(3)
                eval_input1_s2 = self.browser.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/div/div/div[2]/form/div/div[1]/div[5]/div[2]/div[1]/div/span/input')
                eval_input1_s2.send_keys(model_name + 'vs' + self.emeny)
                eval_select1_element = self.browser.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/div/div/div[2]/form/div/div[1]/div[7]/div[2]/div/div/div/div[2]/div[2]/div[1]/div/span/div/div/div[1]')
                # eval_select1_element.click()
                # 使用键盘上下箭头键浏览选项
                eval_select1_option = self.browser.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/div/div/div[2]/form/div/div[1]/div[7]/div[2]/div/div/div/div[2]/div[2]/div[1]/div/span/div/div/div[1]/div/div/input')
                eval_select1_option.click()
                #选择评估阵容
                for i in range(3):
                    eval_select1_option.send_keys(Keys.ARROW_DOWN)
                    # 使用回车键选择选项
                    eval_select1_option.send_keys(Keys.ENTER)
                #选择模型
                eval_select2_element = self.browser.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/div/div/div[2]/form/div/div[1]/div[8]/div[2]/div/div/div/div[1]/div[2]/div/div/span/div/div/span[1]/input')
                eval_select2_element.click()
                time.sleep(3)
                eval_select2_element.send_keys(Keys.TAB)
                time.sleep(3)
                activate_element = self.browser.switch_to.active_element
                activate_element.send_keys(self.emeny)
                time.sleep(3)
                # activate_element.send_keys(Keys.ENTER)
                # eval_select2_element.send_keys(baseline_name)
                eval_select2_element.send_keys(Keys.ARROW_DOWN)
                    # 使用回车键选择选项
                
                eval_select2_element.send_keys(Keys.ENTER)
                eval_select3_element=self.browser.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/div/div/div[2]/form/div/div[1]/div[8]/div[2]/div/div/div/div[2]/div[2]/div/div/span/div/div/div[1]/div/div/input')
                eval_select3_element.click()
                for i in range(3):
                    eval_select3_element.send_keys(Keys.ARROW_DOWN)
                    # 使用回车键选择选项
                    eval_select3_element.send_keys(Keys.ENTER)
                s3=self.browser.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/div/div/div[2]/form/div/div[1]/div[9]/div[2]/div/div/div/div[1]/div[2]/div/div/div/div/div[2]/input')
                #删除现有轮数
                s3.send_keys(Keys.CONTROL+'a')
                s3.send_keys(Keys.DELETE)
                s3.send_keys(EVAL_NUM)
                time.sleep(1)
                self.browser.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/div/div/div[2]/form/div/div[2]/div/div[1]/span/button').click()
                time.sleep(1)
                self.model_list.remove(model_name)
                self.eval_model_list.append(model_name)
                self.browser.get('https://aiarena.tencent.com/p/competition-exp/21/model-manage')
                time.sleep(3)
                table = self.browser.find_element(By.XPATH,
                                    '/html/body/div/div/div/section/section/main/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/table')
                tr_list = table.find_elements(By.TAG_NAME, 'tr')

    def eval_result(self):
        if len(self.eval_task_list) == 0:return
        task_list = list(self.eval_task_list)
        for task in task_list:
            self.browser.get('https://aiarena.tencent.com/p/competition-exp/21/model-access')
            time.sleep(3)
            s = self.browser.find_element(By.XPATH, '//*[@id="name"]')
            s.send_keys(task)
            self.browser.find_element(By.XPATH, '//*[@id="root"]/div/div/section/section/main/div/div/div[2]/div/div/div/form/div/div[1]/div[2]/div/div/div/span/span/span[2]/button').click()
        
            table = self.browser.find_element(By.XPATH,
                                            '//*[@id="root"]/div/div/section/section/main/div/div/div[2]/div/div/div/div/div/div/div/div/div/table/tbody')
            tr_list = table.find_elements(By.TAG_NAME, 'tr')
            td_list = tr_list[1].find_elements(By.TAG_NAME, 'td')
            if td_list[1].text == '已完成':
                self.eval_result_dict[td_list[3].text] = {td_list[5].text:td_list[2].text}
                time.sleep(1)
                self.eval_task_list.remove(task)
        

if __name__ == "__main__":
    m = pa_chong()
    m.go()