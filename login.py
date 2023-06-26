import selenium
from selenium import webdriver
import pyautogui as p
import pyperclip as c
import time
from selenium.webdriver.common.by import By


def kakao_login(driver,tabs):
    driver.find_element(By.XPATH,'//*[@id="loginKey--1"]').click()
    p.typewrite('sya6636@naver.com')
    p.press('tab',presses=2)
    p.typewrite('')
    time.sleep(3)
    p.press('enter')
    time.sleep(1)
    driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/div/a').click()
    time.sleep(1)
    driver.switch_to.window(tabs[0])
    time.sleep(5)
    driver.get('https://mail.naver.com')
    time.sleep(5)
    keyword = '[Kakao] 카카오계정 비상연락용 이메일 인증번호'
    arr2 = driver.find_elements(By.CSS_SELECTOR,r'#mail_list_wrap > ul > li.mail_item > div > div.mail_inner > div > a > span.text')
    print(len(arr2))
    for i in arr2:
        if i.text == keyword:
            print('ss::',i.text)
            i.click()
            break;
    auth = driver.find_element(By.XPATH,'//*[@id="mail_read_scroll_view"]/div/div[2]/div/div/div/table/tbody/tr[1]/td/table/tbody/tr[9]/td[2]/table/tbody/tr[5]/td[3]').text
    driver.switch_to.window(tabs[1])

    driver.find_element(By.XPATH,'//*[@id="passcode--5"]').click()
    print(auth)
    p.typewrite(auth)
    time.sleep(1)
    # driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/div/form/div[4]/button').click()
    p.press('enter')




def naver_login(driver):
    driver.find_element(By.XPATH,'//*[@id="id"]').click()
    c.copy('aidencjswo1')
    p.hotkey('ctrl','v')
    p.press('tab')
    c.copy('sya6636!@#')
    p.hotkey('ctrl','v')
    time.sleep(1)
    driver.find_element(By.XPATH,'//*[@id="log.login"]').click()