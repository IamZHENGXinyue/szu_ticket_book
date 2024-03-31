from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os,json
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

# 定义常量
USERNAME_FILE_PATH = 'C:/Users/11398/code/szu_ticket_book/passwords.json'
LOGIN_URL = "https://ehall.szu.edu.cn/qljfwapp/sys/lwSzuCgyy/index.do#/sportVenue"

# 直接打开并读取JSON文件
try:
    with open(USERNAME_FILE_PATH) as file:
        # load JSON data
        data = json.load(file)
    # 数据已加载带变量data中，现在可以直接操作数据
    # 获取第一个用户和密码
    first_user = list(data.items())[0]  # 使用items()方法将字典转换为键值对列表，并取第一个元素
    username = first_user[0]  # 获取用户名
    password = first_user[1]  # 获取密码
except FileNotFoundError:
    print("文件不存在，请检查文件路径是否正确。")

# 打印第一个用户和密码
# print(f"First Username: {username}, Password: {password}")
#打印所用用户名和对应密码
# for username,password in data.items():
#     print(f"Username: {username}, Password: {password}")


# 定义 XPATH 列表或字典,利用xpaths.items()读取数组,或者利用键值对xpaths["login_button"]
xpaths = {
    'login_button': '//*[@id="casLoginForm"]/p[5]/button',
    'sportVenue': '//*[@id="sportVenue"]/div[1]/div/div[1]',
    'badminton':'//*[@id="sportVenue"]/div[2]/div[2]/div[2]/div[1]/div/div[1]/div',
    'basketball':'//*[@id="sportVenue"]/div[2]/div[2]/div[2]/div[5]/div/div[1]/div/img',
    'tomorrow':'//*[@id="apply"]/div[3]/div[4]/div[2]/label/div[2]',
    'today':'//*[@id="apply"]/div[3]/div[4]/div[1]/label/div[2]',
    'check_condition':'//div[@class="element" and contains(@style, "rgb(29, 33, 41)") and (text()="20:00-21:00(可预约)" or text()="21:00-22:00(可预约)")]',
    'courts_condition':'//*[@id="apply"]/div[3]/div[10]/div/label/div[2][contains(@style, "rgb(29, 33, 41)")]',
    'reservation':'//*[@id="apply"]/div[3]/div[11]/button[2]'
}

#读取异常、超时异常、定位异常


#定义点击函数,使用 except Exception as e 语句捕获了其他可能的异常，并打印出异常的具体信息。
#首先捕获的是 TimeoutException 异常，然后是通用的 Exception 异常。
def wait_and_click(driver, xpath):
    try:
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
    except TimeoutException:
        print("等待元素可点击超时，请检查元素是否正确，或者尝试增加等待时间。")
    except Exception as e:
        print("发生异常", e)

driver = webdriver.Chrome()
driver.get(LOGIN_URL)

#登录
driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(username)
driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(password)

# 等待元素可点击
#element_to_be_clickable 不推荐，正确来说应该是使用element_to_be_clickable函数来实施点击
#WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpaths['login_button']))).click()
wait_and_click(driver, xpaths['login_button'])

#选择粤海校区
#WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, xpaths['sportVenue']))).click()
wait_and_click(driver, xpaths['sportVenue'])

#进入羽毛球界面
#WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpaths[badminton"]))).click()
#wait_and_click(driver, xpaths['badminton'])

#进入篮球界面
#WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpaths['basketball']))).click()
wait_and_click(driver, xpaths['basketball'])

#优先检查次日空余时间段和场地
#首先点击次日时间（每天12:30之后都会出现）
#WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpaths['tomorrow'] ))).click()
wait_and_click(driver, xpaths['tomorrow'])

#检查20:00是否还有场地
available_time_slots = driver.find_elements(By.XPATH,xpaths['check_condition'] )
#如果函数值非空，则点击预约时段
if available_time_slots:
    available_time_slots[0].click()
    #不能和场地使用同样的xpath，因为在场地里使用该xpath时不止包括场地信息在列表里，可能会涉及时间版块的其他元素
    available_court_slots = driver.find_elements(By.XPATH,xpaths['courts_condition'] )
    print("次日有可预约时间段")
    if available_court_slots:
        available_court_slots[0].click()
        print("次日有可预约场地")
        #提交预约
        #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,xpaths['reservation'] ))).click()
        wait_and_click(driver, xpaths['reservation'])
        print(f'已预约次日 {available_time_slots[0].text} 的 {available_court_slots[0].text},请及时支付 ')
    else:
        print("已无可预约场地")
        
else:
    print("次日20:00及以后已无可预约时间段")
    #因次日已无可预约场地，故返回当天时间，检查空余时间段和场地
    #选择当天日期
    driver.find_element(By.XPATH,xpaths['today']).click()
    available_today_time_slots = driver.find_elements(By.XPATH, xpaths['check_condition'])
    
    if available_today_time_slots:
        available_today_time_slots[0].click()
        available_today_court_slots = driver.find_elements(By.XPATH,xpaths['courts_condition'])
        print("今日有可预约时间段")
        if available_today_court_slots:
            available_today_court_slots[0].click()
        #提交预约
        #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpaths['reservation']))).click()
        wait_and_click(driver, xpaths['reservation'])
        print(f'已预约次日{available_today_time_slots[0].text}的{available_today_court_slots[0].text},请及时支付')
        
    else:
        print("今明两天已无可预约场地")
