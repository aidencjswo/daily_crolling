import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import schedule
import time
from selenium.webdriver.chrome.service import Service
import pyperclip as c
import pyautogui as p
from selenium.webdriver.common.by import By
from login import kakao_login,naver_login
from selenium.webdriver.chrome.options import Options
from get_info import set_weather,set_luck, notification_rain_today,notification_rain_tommorow
from auto_chat import read_chat
import tkinter


total_url = 'https://center-pf.kakao.com/_mSsyxj/custom_menus/auto_replies/keyword/1961670'
love_url = 'https://center-pf.kakao.com/_mSsyxj/custom_menus/auto_replies/keyword/1961672'
money_url = 'https://center-pf.kakao.com/_mSsyxj/custom_menus/auto_replies/keyword/1961673'
company_url = 'https://center-pf.kakao.com/_mSsyxj/custom_menus/auto_replies/keyword/1961674'
study_url = 'https://center-pf.kakao.com/_mSsyxj/custom_menus/auto_replies/keyword/1961675'

url_arr = [total_url,love_url,money_url,company_url,study_url]

window = tkinter.Tk()

window.geometry("650x650")

frame1 = tkinter.Frame(relief='ridge',bd=1,borderwidth=3)
frame1.pack(side='left',fill='y',padx=15,pady=15)
frame2 = tkinter.Frame(relief='ridge',bd=1,borderwidth=3)
frame2.pack(side='left',fill='y',pady=15)
frame3 = tkinter.Frame(relief='ridge',bd=1,borderwidth=3)
frame3.pack(side='left',fill='y',padx=15,pady=15)

naver_id_input_label = tkinter.Label(frame1,text='네이버 아이디를 입력해주세요')
naver_id_input_label.pack()
naver_id_input = tkinter.Entry(frame1,width='15')
naver_id_input.pack()
naver_id_button = tkinter.Button(frame1,text='입력')
naver_id_button.pack()

naver_pw_input_label = tkinter.Label(frame1,text='비밀번호를 입력해주세요')
naver_pw_input_label.pack()
naver_pw_input = tkinter.Entry(frame1, show='*',width='15')
naver_pw_input.pack()
naver_pw_button = tkinter.Button(frame1,text='입력')
naver_pw_button.pack()

#url 입력란
kakao_business_channel_url_label = tkinter.Label(frame2,text='카카오비즈니스채널url입력')
kakao_business_channel_url_label.pack()
kakao_business_channel_url_input = tkinter.Entry(frame2,width='15')
kakao_business_channel_url_input.pack()
kakao_business_channel_url_button = tkinter.Button(frame2,text='입력')
kakao_business_channel_url_button.pack()

text_area_label = tkinter.Label(frame2,text='url입력란')
text_area_label.pack()

total_area_label = tkinter.Label(text='총운url')
total_area1 = tkinter.Entry(frame2)
total_area1.pack()

kakao_client_talk_room_label = tkinter.Label(frame3,text='날씨 정보 받는 사람')
kakao_client_talk_room_label.pack()
kakao_client_talk_room_input = tkinter.Entry(frame3,width='15')
kakao_client_talk_room_input.pack()
kakao_client_talk_room_button = tkinter.Button(frame3,text='입력')
kakao_client_talk_room_button.pack()



window.mainloop()


# chrome_options = Options()
# chrome_options.add_argument("--disable-notifications")  # 알림 차단
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
# driver.get('https://mail.naver.com')
# driver.execute_script('window.open("https://center-pf.kakao.com/_mSsyxj/custom_menus/auto_replies", "_blank");')
# driver.implicitly_wait(10)
# tabs = driver.window_handles
# print(tabs)
# driver.switch_to.window(tabs[0])
# time.sleep(1)

# # 네이버 로그인
# naver_login(driver)
# driver.switch_to.window(tabs[1])
# time.sleep(1)

# driver.switch_to.window(tabs[1])
# kakao_login(driver,tabs)
# driver.switch_to.window(tabs[0])

# read_chat()

# def batch1():
#     set_weather(driver,tabs)

# def batch2():
#     set_luck(driver,tabs,url_arr)

# def batch3():
#     notification_rain_tommorow(driver,tabs)

# def batch4():
#     notification_rain_today(driver,tabs)

# def naver_login():
#     naver.switch_to.window(naver.current_window_handle)
#     naver.execute_script("window.focus();")
#     naver.get_window_position
#     naver.find_element(By.XPATH,'//*[@id="id"]').click()
#     c.copy('aidencjswo1')
#     p.hotkey('ctrl','v')
#     p.press('tab')
#     c.copy('sya6636!@#')
#     p.hotkey('ctrl','v')
#     p.press('tab',presses=3)
#     p.press('enter')
#     keyword = '[Kakao] 카카오계정 비상연락용 이메일 인증번호'
#     arr2 = naver.find_elements(By.CSS_SELECTOR,r'#mail_list_wrap > ul > li.mail_item > div > div.mail_inner > div > a > span.text')
#     for i in arr2:
#         if i.text == keyword:
#             print('ss::',i.text)
#             i.click()
#             break;
#     auth = naver.find_element(By.XPATH,'//*[@id="mail_read_scroll_view"]/div/div[2]/div/div/div/table/tbody/tr[1]/td/table/tbody/tr[9]/td[2]/table/tbody/tr[5]/td[3]').text
#     print(auth)


def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


schedule.every(1).minutes.do(batch1)
schedule.every().day.at("07:30:00").day.do(batch2)
schedule.every().day.at("22:00:00").day.do(batch3)
schedule.every().day.at("07:00:00").day.do(batch4)

run_schedule()

time.sleep(5)