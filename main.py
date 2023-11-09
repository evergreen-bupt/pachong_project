# <<<<<<< Updated upstream
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time
import re
import json
import os

EVAL_NUM = 1

class pa_chong():
    def __init__(self):
        #如果last_name和 last_NAME_counts顺序与平台里的先后顺序不一致，可能存在问题。
        self.model_list = []
        self.eval_model_dict = {}
        # self.train_task = {'test_pr2':'13h5min50s', 'Update-v6-2':'19h59min15s'}
        # self.enemy_pool = ['baseline-1', 'baseline-2', 'baseline-3']
        self.eval_task_list = []
        self.time = 60
        self.eval_result_dict = {}
        if os.path.exists('elo.json'):
            f2 = open('elo.json', 'r')
            self.elo_dic= json.load(f2)
            print("load elo file")
        else:
            self.elo_dic={}
        if os.path.exists('task.json'):
            with open('task.json','r') as f3:
                data = json.load(f3)
                self.train_task=data[0]
                self.enemy_pool=data[1]
                print("load task file")
        else:
            self.train_task={}
    
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
            self.download_modle()
            self.eval_model()
            self.eval_result()
            self.get_elo_score()
            self.save_result()
            time.sleep(self.time)

    def build_modle_name(self, task_name, train_total_time, train_time):
        task = task_name.split("-")
        name1 = str(task[0]) if len(task) == 1 else str(task[0] +"-"+ task[1])
        total_time = train_total_time.split("(")
        time1 = total_time[1].split(")")[0]
        time1_hour = int(time1.split("h")[0])
        time2 = train_time.split("m")[0]
        time2_hour = int(time2.split("h")[0])
        time2_min = time2.split("h")[1]
        name2 = str(str(time1_hour + time2_hour) +'h'+ time2_min)
        return name1 +'-'+ name2

    def download_modle(self):
        task_num = 0
        last_train_time = str()
        for i in range(1, 11):
            self.browser.get('https://aiarena.tencent.com/p/competition-exp/21/cluster-training') # 替换为目标网站的URL
            time.sleep(3)
            table = self.browser.find_element(By.XPATH, '//*[@id="root"]/div/div/section/section/main/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/table/tbody')
            tr_list = table.find_elements(By.TAG_NAME, 'tr')
            td_list = tr_list[i].find_elements(By.TAG_NAME, 'td')
            if td_list[2].text != '进行中':continue
            task_num += 1
            task_name = str(td_list[1].text)
            train_total_time = str(td_list[3].text)
            j = 0
            while(True):
                time.sleep(1)
                self.browser.find_element(By.XPATH, 
                f'//*[@id="root"]/div/div/section/section/main/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/table/tbody/tr[{i+1}]/td[12]/div/div/div[2]/button').click()
                time.sleep(3)
                tr1_list = self.browser.find_element(By.XPATH, 
                                                '/html/body/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/table/tbody').find_elements(By.TAG_NAME, 'tr')
                train_time  = tr1_list[j+1].find_elements(By.TAG_NAME, 'td')[0].text
                last_train_time = tr1_list[1].find_elements(By.TAG_NAME, 'td')[0].text
                if train_time == self.train_task[task_name]:break
                self.browser.find_element(By.XPATH, 
                    f'/html/body/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[{j+2}]/td[3]/div/div/div[2]/span/button').click()
                time.sleep(3)
                input1_s2 = self.browser.find_element(By.XPATH, 
                                                        '/html/body/div[3]/div/div[2]/div/div/div[2]/form/div/div[1]/div[1]/div[2]/div[1]/div/span/input')
                model_name = self.build_modle_name(task_name, train_total_time, train_time)
                input1_s2.send_keys(model_name)
                input2_s2 = self.browser.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div/div[2]/form/div/div[1]/div[4]/div[2]/div/div/div/textarea')
                input2_s2.send_keys(task_name +'_'+ train_time)
                time.sleep(2)
                self.browser.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div/div[2]/form/div/div[2]/div/div[1]/span/button').click()
                time.sleep(3)
                self.model_list.append(model_name)
                self.eval_model_dict[model_name] = 0
                self.browser.get('https://aiarena.tencent.com/p/competition-exp/21/cluster-training')
                time.sleep(3)
                j += 1
                if j == len(tr1_list):break
            self.train_task[task_name] = last_train_time
            if task_num == 2:break
    
    def eval_model(self):
        if len(self.model_list) == 0 and len(self.eval_task_list) == 20:return 
        model_to_eval = list(self.model_list)
        for model_name in model_to_eval:
            for enemy in self.enemy_pool:
                if len(self.eval_task_list) == 20: return 
                self.browser.get('https://aiarena.tencent.com/p/competition-exp/21/model-manage')
                time.sleep(3)
                self.browser.find_element(By.XPATH, '//*[@id="name"]').send_keys(model_name)
                time.sleep(1)
                self.browser.find_element(By.XPATH, 
                                        '//*[@id="root"]/div/div/section/section/main/div/div/div[2]/div/div/div/div/form/div/div[1]/div[2]/div/div/div/span/span/span[2]/button').click()
                time.sleep(1)
                td_list = self.browser.find_element(By.XPATH,
                                        '/html/body/div/div/div/section/section/main/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/table').find_elements(By.TAG_NAME, 'tr')[2].find_elements(By.TAG_NAME, 'td')
                print(td_list[3].text)
                if td_list[3].text == '检测中' or td_list[3].text == '待检测':break
                elif td_list[3].text == '检测失败':
                    self.model_list.remove(model_name)
                    break
                self.browser.find_element(By.XPATH, 
                                        '//*[@id="root"]/div/div/section/section/main/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[2]/td[12]/div/div/div[1]/span/button').click()
                time.sleep(2)
                self.browser.find_element(By.XPATH,
                                        '/html/body/div[2]/div/div[2]/div/div/div[2]/form/div/div[1]/div[5]/div[2]/div[1]/div/span/input').send_keys(model_name + '_' +  str(self.eval_model_dict[model_name]))
                eval_select1_option = self.browser.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/div/div/div[2]/form/div/div[1]/div[7]/div[2]/div/div/div/div[2]/div[2]/div[1]/div/span/div/div/div[1]/div/div/input')
                eval_select1_option.click()
                for _ in range(3):
                    eval_select1_option.send_keys(Keys.ARROW_DOWN)
                        # 使用回车键选择选项
                    eval_select1_option.send_keys(Keys.ENTER)
                eval_select2_element = self.browser.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/div/div/div[2]/form/div/div[1]/div[8]/div[2]/div/div/div/div[1]/div[2]/div/div/span/div/div/span[1]/input')
                eval_select2_element.click()
                time.sleep(3)
                eval_select2_element.send_keys(Keys.TAB)
                time.sleep(3)
                activate_element = self.browser.switch_to.active_element
                activate_element.send_keys(enemy)
                time.sleep(3)
                eval_select2_element.send_keys(Keys.ARROW_DOWN)
                    # 使用回车键选择选项
                eval_select2_element.send_keys(Keys.ENTER)
                eval_select3_element=self.browser.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/div/div/div[2]/form/div/div[1]/div[8]/div[2]/div/div/div/div[2]/div[2]/div/div/span/div/div/div[1]/div/div/input')
                eval_select3_element.click()
                for _ in range(3):
                    eval_select3_element.send_keys(Keys.ARROW_DOWN)
                    # 使用回车键选择选项
                    eval_select3_element.send_keys(Keys.ENTER)
                s3=self.browser.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/div/div/div[2]/form/div/div[1]/div[9]/div[2]/div/div/div/div[1]/div[2]/div/div/div/div/div[2]/input')
                #删除现有轮数
                s3.send_keys(Keys.CONTROL+'a')
                s3.send_keys(Keys.DELETE)
                s3.send_keys(EVAL_NUM)
                time.sleep(1)
                self.browser.find_element(By.XPATH,
                                        '//*[@id="desc"]').send_keys(model_name + 'vs' + enemy)
                time.sleep(1)
                self.browser.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/div/div/div[2]/form/div/div[2]/div/div[1]/span/button').click()
                time.sleep(1)
                self.eval_model_dict[model_name] += 1 
                self.eval_task_list.append(model_name + '_' +  str(self.eval_model_dict[model_name]))
                if enemy == self.enemy_pool[len(self.enemy_pool)-1] :self.model_list.remove(model_name)

    def eval_result(self):
        if len(self.eval_task_list) == 0:return
        task_list = list(self.eval_task_list)
        for task in task_list:
            self.browser.get('https://aiarena.tencent.com/p/competition-exp/21/model-access')
            time.sleep(3)
            s = self.browser.find_element(By.XPATH, '//*[@id="name"]')
            s.send_keys(task)
            self.browser.find_element(By.XPATH, '//*[@id="root"]/div/div/section/section/main/div/div/div[2]/div/div/div/form/div/div[1]/div[2]/div/div/div/span/span/span[2]/button').click()
            time.sleep(3)
            table = self.browser.find_element(By.XPATH,
                                            '//*[@id="root"]/div/div/section/section/main/div/div/div[2]/div/div/div/div/div/div/div/div/div/table/tbody')
            tr_list = table.find_elements(By.TAG_NAME, 'tr')
            td_list = tr_list[1].find_elements(By.TAG_NAME, 'td')
            if td_list[1].text == '已完成':
                self.eval_result_dict[td_list[3].text+'_vs_'+td_list[5].text]=td_list[2].text
                time.sleep(1)
                self.eval_task_list.remove(task)

    def get_elo_score(self):
        K = 32
        def expected_result(player1_elo, player2_elo):
            return 1 / (1 + 10**((player2_elo - player1_elo) / 400))
        for key,value in list(self.eval_result_dict.items()):
            model=key.split("_vs_")
            model_a=model[0]
            model_b=model[1]
            if model_a not in self.elo_dic:
                self.elo_dic[model_a]=1000
            if model_b not in self.elo_dic:
                self.elo_dic[model_b]=1000 
            numbers=re.findall(r'\d+',value)
            numbers=[int(number) for number in numbers]
            W_a = numbers[0] / numbers[2]
            W_b = numbers[1] / numbers[2]
            if W_b<0.5 and model_b==self.enemy_pool[-1]:
                print(self.enemy_pool)
                self.updata_enemy_pool()
                print(self.enemy_pool)
            # print(model_a,model_b,numbers)
            E_a = expected_result(self.elo_dic[model_a],self.elo_dic[model_b])
            E_b = expected_result(self.elo_dic[model_b],self.elo_dic[model_a])
            self.elo_dic[model_a] = self.elo_dic[model_a] + K * (W_a - E_a)
            #暂时不更新baseline的分数
            # self.elo_dic[model_b] = self.elo_dic[model_b] + K * (W_b - E_b)
            self.eval_result_dict.pop(key)
        # print(self.elo_dic)

    def save_result(self):
        elo_json = json.dumps(self.elo_dic,sort_keys=False, indent=4, separators=(',', ': '))
        f = open('elo.json', 'w')
        f.write(elo_json)
        task_to_write=[self.train_task,self.enemy_pool]
        with open('task.json','w') as json_file:
            json.dump(task_to_write, json_file)

    def updata_enemy_pool(self):
        #取出最新的对手
        last_enemy_name=self.enemy_pool[-1]
        cnt=last_enemy_name.split("-")
        new_cnt=int(cnt[1])+1
        self.enemy_pool.pop(0)
        self.enemy_pool.append("baseline-"+str(new_cnt))
        




        

if __name__ == "__main__":
    m = pa_chong()
    m.go()