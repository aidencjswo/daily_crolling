import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, InvalidSelectorException, JavascriptException
from selenium.webdriver.common.keys import Keys
import schedule
from selenium.webdriver.common.action_chains import ActionChains
import json



past_chat = '오팬무'

## 채팅 읽기
def read_chat():
    option1 = Options()
    #Headless 설정
    option1.headless = False
    readChatDriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=option1)    
    readChatDriver.get('https://center-pf.kakao.com/_mSsyxj/chats/4876828594679908')
    try:
        # driver.execute_script("var elements = document.querySelectorAll('.item_chat:not(.item_me)');")
        # text = driver.execute_script("return elements.item(elements.length-1).getElementsByTagName('span')[0].innerText")
        text = readChatDriver.execute_script('''
                                    var elements = document.querySelectorAll('.item_chat:not(.item_me)');
                                    return elements.item(elements.length-1).getElementsByTagName('span')[0].innerText;
                                    ''')
        # 현재 시간을 가져옴
        current_time = time.localtime()
        # 시간 정보 추출
        hour = current_time.tm_hour
        minute = current_time.tm_min
        # 시간 형식 변환
        if hour < 12:
            am_pm = '오전'
            if hour == 0:
                hour = 12
        else:
            am_pm = '오후'
            if hour > 12:
                hour -= 12
        # 출력
        formatted_time = f"{am_pm}{hour:02d}:{minute:02d}"
        send_time = readChatDriver.execute_script('''
                                    var elements = document.querySelectorAll('.item_chat:not(.item_me)');
                                    return elements.item(elements.length-1).getElementsByTagName('span')[2].innerText;
                                    ''')        
        print(text)
        if past_chat == text and send_time == formatted_time:
            send_message = readChatDriver.find_element(By.XPATH,'//*[@id="chatWrite"]')
            send_message.send_keys('빨강❤️',Keys.ENTER)
        else:
            print('더이상 보낸 문자가 없음')
    except JavascriptException as e:
        print('javaScript exception:',e.with_traceback)
