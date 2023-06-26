
import selenium
# selenium의 webdriver를 사용하기 위한 import
from selenium import webdriver
# selenium으로 키를 조작하기 위한 import
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import pyperclip as c
import pyautogui as p
import schedule
import pywinauto
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import UnexpectedAlertPresentException,ElementClickInterceptedException, InvalidSelectorException,JavascriptException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import json


weather_arr = []
luck_arr = []

# 템플릿 만들기
def create_template(arr):
    str = ''
    for i in arr:
        str += i + '\n'
    return str

def set_weather(driver,tabs):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")  # 알림 차단
        chrome_options.headless = False # 완성 후 True로 set

        # global weather_arr
        #드라이버 경로는 Service객체를 넘겨줘야함
        driver.switch_to.window(tabs[0])

        # open window
        driver.get('https://weather.naver.com/')

        #명시적대기(10초)
        driver.implicitly_wait(10)

        ### crolling start !!

        # crolling val set
        current_temp = None
        location = None
        compare_to = None
        up_down = None
        tomorrow_am_precipitation = None
        tomorrow_pm_precipitation = None
        today_am_precipitation = None
        today_pm_precipitation = None
        try:
            current_temp = driver.execute_script("return document.querySelector('#now > div > div.weather_area > div.weather_now > div > strong').innerText.slice(6,11)")
            location = driver.execute_script("return document.getElementsByClassName('location_name')[0].innerText")
            compare_to = driver.find_element(By.XPATH,'//*[@id="now"]/div/div[3]/div[1]/p/span[2]').text[0:4]
            up_down = driver.find_element(By.XPATH,'//*[@id="now"]/div/div[3]/div[1]/p/span[2]').text[5:]
            today_am_precipitation = driver.execute_script("return document.getElementsByClassName('rainfall')[0].innerText")
            today_pm_precipitation = driver.execute_script("return document.getElementsByClassName('rainfall')[1].innerText")
            tomorrow_am_precipitation = driver.execute_script("return document.getElementsByClassName('rainfall')[2].innerText")
            tomorrow_pm_precipitation = driver.execute_script("return document.getElementsByClassName('rainfall')[3].innerText")

            today_am_precipitation = today_am_precipitation.replace('강수확률\n','')
            today_pm_precipitation = today_pm_precipitation.replace('강수확률\n','')
            tomorrow_am_precipitation = tomorrow_am_precipitation.replace('강수확률\n','')
            tomorrow_pm_precipitation = tomorrow_pm_precipitation.replace('강수확률\n','')            
        except NoSuchElementException or InvalidSelectorException:
            print('예외 발생 where : current_temp or location or compare_to or up_down')
            
        ### weather_arr - SET !!
        # 현재 시각 구하기
        time1 = time.localtime()
        get_now = "[" + str(time1.tm_mon) + "월" + str(time1.tm_mday) + "일" + str(time1.tm_hour) + "시" + str(time1.tm_min) + "분]"

        weather_arr.append(get_now)
        weather_arr.append(location+'의')
        weather_arr.append('현재온도는 '+current_temp+'이고,')
        weather_arr.append('어제보다 '+compare_to+up_down)
        weather_arr.append('오늘의 강수량은')
        weather_arr.append('오전('+today_am_precipitation+')')
        weather_arr.append('오후('+today_pm_precipitation+')'+'이에요')
        weather_arr.append('그리고')
        weather_arr.append('내일 오전 강수량은 '+tomorrow_am_precipitation+' 이고')
        weather_arr.append('내일 오후 강수량은 '+tomorrow_pm_precipitation+' 이에요')
        weather_arr.append('>_<❤️')

        # 템플릿 만들기
        input_text = create_template(weather_arr)

        ### kakaotalk channel SET !!
        driver.get('https://center-pf.kakao.com/_mSsyxj/custom_menus/auto_replies/keyword/1961454')
        weather_text = driver.find_element(By.XPATH,'//*[@id="mArticle"]/div/form/fieldset/div[1]/div[1]/div/div[2]/div/div/textarea')

        # textarea 활성화
        actions = ActionChains(driver)
        actions.move_to_element(weather_text).click().perform()
        # text delete
        weather_text.clear()
        # template paste
        weather_text.send_keys(input_text)
        # arr clear
        weather_arr.clear()
        # 저장 버튼 누르기
        try:
            driver.find_element(By.XPATH,'//*[@id="mArticle"]/div/form/fieldset/div[2]/button[2]').click()
            driver.find_element(By.XPATH,'/html/body/div[4]/div/div/div/div/div/button').click()
        except ElementClickInterceptedException:
            print('ElementClickInterceptedException 예외 발생')
    except NoSuchElementException:
        print('NoSuchElement by crolling')

def notification_rain_tommorow(driver,tabs):
    try:
        # global weather_arr
        #드라이버 경로는 Service객체를 넘겨줘야함
        driver.switch_to.window(tabs[1])

        # open window
        driver.get('\nhttps://weather.naver.com/\n')

        tomorrow_am_precipitation = ''
        tomorrow_pm_precipitation = ''
        try:
            tomorrow_am_precipitation = driver.execute_script("return document.getElementsByClassName('rainfall')[2].innerText")
            tomorrow_pm_precipitation = driver.execute_script("return document.getElementsByClassName('rainfall')[3].innerText")
            print(tomorrow_am_precipitation)
            print(tomorrow_pm_precipitation)

            tomorrow_am_precipitation = tomorrow_am_precipitation.replace('강수확률\n','')
            tomorrow_pm_precipitation = tomorrow_pm_precipitation.replace('강수확률\n','')            
            am_percentage = tomorrow_am_precipitation >= '60'
            pm_percentage = tomorrow_pm_precipitation >= '60'
            time1 = time.localtime()
            get_now = "[" + str(time1.tm_mon) + "월" + str(time1.tm_mday) + "일" + str(time1.tm_hour) + "시" + str(time1.tm_min) + "분]"
            if am_percentage is True or pm_percentage is True:
                weather_arr.append('[강수량 알림톡]')
                weather_arr.append('내일 오전은 비 올 확률이'+tomorrow_am_precipitation+'이고,')
                weather_arr.append('내일 오후는 비 올 확률이'+tomorrow_pm_precipitation+'입니다!')
                weather_arr.append('오늘의 강수량을 확인하세요!')                
                weather_arr.append('https://weather.naver.com/')
                input_text = create_template(weather_arr)
                driver.get('https://center-pf.kakao.com/_mSsyxj/chats/4876896613890149')
                send_message = driver.find_element(By.XPATH,'//*[@id="chatWrite"]')
                send_message.send_keys(input_text,Keys.ENTER)
                weather_arr.clear()
        except NoSuchElementException:
            print('예외 발생 where : current_temp or location or compare_to or up_down')
        except InvalidSelectorException:
            print('InvalidSelectorException')
        except JavascriptException:
            print('오류나니까 한번더')
            notification_rain_tommorow(driver,tabs)            
    except NoSuchElementException:
        print('NoSuchElement by crolling')    

def notification_rain_today(driver,tabs):
    try:
        # global weather_arr
        #드라이버 경로는 Service객체를 넘겨줘야함
        driver.switch_to.window(tabs[1])

        # open window
        driver.get('https://weather.naver.com/')

        today_am_precipitation = ''
        today_pm_precipitation = ''
        try:
            today_am_precipitation = driver.execute_script("return document.getElementsByClassName('rainfall')[0].innerText")
            today_pm_precipitation = driver.execute_script("return document.getElementsByClassName('rainfall')[1].innerText")

            today_am_precipitation = today_am_precipitation.replace('강수확률\n','')
            today_pm_precipitation = today_pm_precipitation.replace('강수확률\n','')
            am_percentage = today_am_precipitation >= '60'
            pm_percentage = today_pm_precipitation >= '60'
            time1 = time.localtime()
            get_now = "[" + str(time1.tm_mon) + "월" + str(time1.tm_mday) + "일" + str(time1.tm_hour) + "시" + str(time1.tm_min) + "분]"
            if am_percentage is True or pm_percentage is True:
                weather_arr.append('[강수량 알림톡]')
                weather_arr.append('오늘 오전은 비 올 확률이'+today_am_precipitation+'이고,')
                weather_arr.append('오늘 오후는 비 올 확률이'+today_pm_precipitation+'입니다!')
                weather_arr.append('오늘의 강수량을 확인하세요!')
                weather_arr.append('https://weather.naver.com/')
                input_text = create_template(weather_arr)
                driver.get('https://center-pf.kakao.com/_mSsyxj/chats/4876896613890149')
                send_message = driver.find_element(By.XPATH,'//*[@id="chatWrite"]')
                send_message.send_keys(input_text,Keys.ENTER)
                weather_arr.clear()
        except NoSuchElementException:
            print('예외 발생 where : current_temp or location or compare_to or up_down')
        except InvalidSelectorException:
            print('InvalidSelectorException')
        except JavascriptException:
            print('오류나니까 한번더')
            notification_rain_today(driver,tabs)            
    except NoSuchElementException:
        print('NoSuchElement by crolling')    

def set_luck(driver,tabs,url_arr):
    global luck_arr   
    try:
        #드라이버 경로는 Service객체를 넘겨줘야함
        driver.switch_to.window(tabs[0])
        #윈도우 열기
        driver.get('https://www.naver.com')
        #명시적대기(10초)
        driver.implicitly_wait(10)
        ##########데이터수집(오늘의 운세)##########
        text = driver.find_element(by=By.XPATH,value='//*[@id="query"]')
        text.send_keys('오늘의 운세',Keys.ENTER)

        data = {"gender":"f","birth":"19941005","solarCal":"solar","time":"5"}
        json_data = json.dumps(data)
        script = f"localStorage.setItem('_fortune_birthday', '{json_data}');"
        driver.execute_script(script)
        time.sleep(2)
        driver.find_element(By.XPATH,'//*[@id="fortune_birthCondition"]/div[1]/fieldset/input').click()

        # 총운
        total_header = driver.find_element(By.XPATH,'//*[@id="fortune_birthResult"]/dl[1]/dd/strong').text
        total_body = driver.find_element(By.XPATH,'//*[@id="fortune_birthResult"]/dl[1]/dd/p').text
        total = total_header + '\n' + total_body

        # 애정운
        driver.find_element(By.XPATH,'//*[@id="fortune_birthResult"]/ul[2]/li[2]/a/div').click()
        love_body = driver.find_element(By.XPATH,'//*[@id="fortune_birthResult"]/dl[1]/dd/p').text    

        # 금전운
        driver.find_element(By.XPATH,'//*[@id="fortune_birthResult"]/ul[2]/li[3]/a/div').click()
        money_body = driver.find_element(By.XPATH,'//*[@id="fortune_birthResult"]/dl[1]/dd/p').text

        # 회사
        driver.find_element(By.XPATH,'//*[@id="fortune_birthResult"]/ul[2]/li[4]/a/div').click()
        company_body = driver.find_element(By.XPATH,'//*[@id="fortune_birthResult"]/dl[1]/dd/p').text

        driver.find_element(By.XPATH,'//*[@id="fortune_birthResult"]/ul[2]/li[5]/a/div').click()
        study_body = driver.find_element(By.XPATH,'//*[@id="fortune_birthResult"]/dl[1]/dd/p').text
        
        # arr[0]
        luck_arr.append('[총운]'+'\n'+total)
        # arr[1]
        luck_arr.append('[애정운]'+'\n'+love_body)
        # arr[2]
        luck_arr.append('[금전운]'+'\n'+money_body)
        # arr[3]
        luck_arr.append('[직장운]'+'\n'+company_body)
        # arr[4]
        luck_arr.append('[학업,성적운]'+'\n'+study_body)
        ###################################           
        # 반복문으로 운세 set
        ###################################           
        for i in range(5):
            driver.get(url_arr[i])
            luck_text = driver.find_element(By.XPATH,'//*[@id="mArticle"]/div/form/fieldset/div[1]/div[1]/div/div[2]/div/div/textarea')
            # textarea 활성화
            actions = ActionChains(driver)
            actions.move_to_element(luck_text).click().perform()    
            luck_text.clear()        
            luck_text.send_keys(luck_arr[i])
            try:
                driver.find_element(By.XPATH,'//*[@id="mArticle"]/div/form/fieldset/div[2]/button[2]').click()
                driver.find_element(By.XPATH,'/html/body/div[4]/div/div/div/div/div/button').click()
            except ElementClickInterceptedException:
                print('ElementClickInterceptedException 예외 발생')     
        luck_arr.clear()
    except NoSuchElementException:
        print('NoSuchElementException')


