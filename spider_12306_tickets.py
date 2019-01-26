from selenium import webdriver

from selenium.common.exceptions import TimeoutException

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains

from pyquery import PyQuery as pq

import requests

import json

from PIL import Image  

from PIL import ImageFilter  

import urllib  

import re 

import time

class traintickets():

    def __init__(self):
    
        self.username = "15000730358"
        
        self.password = "yanyu19960822"
        
        self.person = requests.Session()
        
        self.browser = webdriver.Chrome()

        self.wait = WebDriverWait(self.browser,5)
        
        self.url = "https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2019-01-09&leftTicketDTO.from_station=SHH&leftTicketDTO.to_station=QRS&purpose_codes=ADULT"
    
        self.pic_url = "https://kyfw.12306.cn/passport/captcha/captcha-image64?login_site=E&module=login&rand=sjrand&1546100463604"
        
        self.login_url = "https://kyfw.12306.cn/otn/resources/login.html"
    
    def get_page(self,url):

        headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'}

        response = requests.get(url,headers=headers)
    
        return response.json()
    
    def get_list(self,json):

        items = json.get('data').get('result')
    
        for item in items:
        
            item = item.split("|")
            
            item = item[3:]
            
            dic = {}
            
            dic['车次'] = item[0]
            
            dic['发车时间'] = item[5]
            
            dic['到达时间'] = item[6]
            
            dic['历时'] = item[7]
    
            yield dic
            
    def checkticket(self):

        self.json = self.get_page(self.url)
    
        self.list = self.get_list(self.json)
    
        for i in self.list:
    
            print (i)
            
    def login(self,login_url):
    
        self.browser.get(login_url)
        
        html = self.browser.page_source
        
        title = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.login-hd-account')))
        
        print("搜索标题。。。")
        
        title.click()
        
        input_username = self.wait.until(EC.presence_of_element_located((By.ID,"J-userName")))
        
        input_password = self.wait.until(EC.presence_of_element_located((By.ID,'J-password')))
        
        time.sleep(3)
        
        print("输入中。。。")
         
        input_username.send_keys(self.username)
        
        input_password.send_keys(self.password)
        
        print("验证中。。。")
        
        while self.browser.current_url == self.login_url:
        
            print("页面跳转中。。")
            
            time.sleep(3)
        
        index = self.wait.until(EC.presence_of_element_located((By.ID,"J-index")))
        
        print("跳转至首页。。")   
        
        while self.browser.current_url == "https://kyfw.12306.cn/otn/view/index.html":
        
            print("跳转中。。")
            
            time.sleep(2)
        
            index.click()
            
    def input_info(self):
    
        print("信息输入中。。。")
    
        input_start = self.wait.until(EC.presence_of_element_located((By.ID,"fromStationText")))
        
        input_end = self.wait.until(EC.presence_of_element_located((By.ID,"toStationText")))
        
        input_date = self.wait.until(EC.presence_of_element_located((By.ID,"train_date")))
        
        submit_info = self.wait.until(EC.presence_of_element_located((By.ID,"search_one")))
        
        input_start.click()
        
        input_start.send_keys("上海")
        
        input_start.send_keys(Keys.ENTER)
        
        time.sleep(1)
        
        input_end.click()
        
        input_end.send_keys("泉州")
        
        input_end.send_keys(Keys.DOWN)
        
        input_end.send_keys(Keys.ENTER)
        
        time.sleep(1)
        
        js = "document.getElementById('train_date').removeAttribute('readonly')"
        
        self.browser.execute_script(js)
        
        input_date.clear()
        
        input_date.send_keys("2019-02-04")
        
        submit_info.send_keys(Keys.ENTER)
        
        print("跳转至选票页面。。。")
        
    def train_num(self):
    
        try:

            return self.wait.until(EC.presence_of_element_located((By.ID,"trainum"))).text.strip()
            
        except:
        
            pass
        
    def choose_tickets(self):
    
        try:
    
            id = 1
        
            self.browser.switch_to_window(self.browser.window_handles[1])
        
            num = self.train_num() 
        
            #ck = self.browser.get_cookies()
        
            #for i in ck:
        
                #print(i)
    
            while id <= 2 * int(num):
        
                xpath = "//tbody[@id='queryLeftTable']/tr[%s]" % id
        
                seat = self.browser.find_element_by_xpath(xpath + "/td[4]").text.strip()
        
                times = self.browser.find_element_by_xpath(xpath + "//div[3]/strong[1]").text.strip()
            
                id += 2
            
                if seat == "有" and times == "09:05":
            
                    print (seat+"该车次",times)
                
                    book_button = self.browser.find_element_by_xpath(xpath+"//td[13]/a").click()
                
                    id = 100
                
                else:
            
                    print('没有符合要求的车次！')
        
            self.wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='normalPassenger_0']"))).click()
        
            self.wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='normalPassenger_1']"))).click()
        
            self.wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='normalPassenger_2']"))).click()
        
            self.wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='submitOrder_id']"))).click()

        #iframe = self.browser.find_element(By.XPATH,"//*[@id='body_id']/iframe[2]")
        
        #self.browser.switch_to_frame(iframe)
        
        
        
            confirm = self.wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='qr_submit_id']")))
        
            time.sleep(3)
        
        #jss = "document.getElementByXpath('//*[@id='qr_submit_id']').click()"
        
        #self.browser.execute_script(jss)
        
            confirm.send_keys(Keys.ENTER)
        
            print("已点击提交。。")
           
            print("请在30s内付款。。")
        
        except:
        
            print("还没开始出票。。")
            
            self.browser.close()
            
            self.browser.switch_to_window(self.browser.window_handles[0])
            
            submit_info = self.wait.until(EC.presence_of_element_located((By.ID,"search_one")))
            
            submit_info.send_keys(Keys.ENTER)
            
            self.choose_tickets()
            
            
    
tk = traintickets()  

tk.checkticket()

tk.login(tk.login_url)

time.sleep(2)

tk.input_info()

time.sleep(2)

tk.choose_tickets()


        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        