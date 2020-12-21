from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.common.exceptions import NoSuchElementException, TimeoutException,StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
import requests
import time



class Result_node():

    def __init__(self,channel_name, subscriber_num,not_int_subscriber_num, profile_url):
        self.channel_name = channel_name
        self.subscriber_num = subscriber_num
        self.not_int_subscriber_num = not_int_subscriber_num
        # self.channel_avg_visit_num = channel_avg_visit_num
        self.profile_url = profile_url

def croller(search):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options = chrome_options) #NAS에 올릴 때
    #driver = webdriver.Chrome('/Users/choijungho/Desktop/Django 프로젝트/chromedriver', chrome_options = chrome_options) # 로컬에서 돌릴때
    
    #인스타 관련 해시태그 가져오기
    driver.get('https://www.tagsfinder.com/ko-kr/?hashtag='+search+'&limit=30&country=kr&fs=off&fp=off&fg=off&custom=&type=live')
    time.sleep(3)
    relevent_search = driver.find_elements_by_class_name('tag')
    relevent_keyword_list = []
    for element in relevent_search:
        keyword = element.text.replace('#',"")
        if '\nX' in keyword:
            keyword = keyword.replace('\nX','')
        relevent_keyword_list.append(keyword)


    # Youtube 접속

    driver.get('https://www.youtube.com/')
    driver.implicitly_wait(1)


    # 검색
    youtube_search = search
    search_url = urllib.parse.quote(youtube_search)
    #필터를 채널, 조회순 정렬로 변경하면서 검색
    driver.get('https://www.youtube.com/results?search_query='+search_url+'&sp=EgIQAg%253D%253D')
    time.sleep(1)
    search_channel = driver.find_element_by_xpath('//*[@id="container"]/ytd-toggle-button-renderer/a')
    search_channel.click()
    time.sleep(1)
    # 계정 이름 리스트
    channel_name_list = []

    # 구독자 수 리스트
    subscriber_num_list = []

    # 채널 프로필 url 리스트
    channel_url_list = []

    not_int_subscriber_num = []


    #스크롤 미리 내려서 충분한 유튜버 확보
    number_of_scroll = 50
    body = driver.find_element_by_tag_name('body')

    while number_of_scroll:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)
        number_of_scroll -= 1



    # 모든 동영상 리스트
    channel_list = driver.find_elements_by_id('main-link')
    subscriber_list = driver.find_elements_by_id('subscribers')
    channel_name = driver.find_elements_by_class_name('style-scope ytd-channel-name')
    

    for obj in channel_list:
        url = obj.get_attribute('href')
        channel_url_list.append(url)

    for name in channel_name:
        channel_name_list.append(name.text)

    for obj in subscriber_list:
        sub_num = obj.text
        if sub_num == '':
            not_int_subscriber_num.append('0명')
        else:
            not_int_subscriber_num.append(sub_num.replace('구독자 ','').replace(' subscribers','').replace(' subscriber',''))
            sub_num = sub_num.replace('구독자 ','').replace('명','').replace(' subscribers','').replace(' subscriber','')
        
        if sub_num == "":
            subscriber_num_list.append(0)
        elif sub_num[-1] == 'K':
            sub_num = int(float(sub_num[:-1])*1000)
            subscriber_num_list.append(sub_num)
        elif sub_num[-1] == 'M':
            sub_num = int(float(sub_num[:-1])*1000000)
            subscriber_num_list.append(sub_num)
        elif sub_num[-1] == '만':
            sub_num = int(float(sub_num[:-1]) * 10000)
            subscriber_num_list.append(sub_num)
        elif sub_num[-1] == '천':
            sub_num = int(float(sub_num[:-1]) * 1000)
            subscriber_num_list.append(sub_num)
        else:
            sub_num = int(sub_num)
            subscriber_num_list.append(sub_num)

    result_list = []
    channel_name_list = channel_name_list[:-1]
    for i in range(len(channel_name_list)):
        new_node = Result_node(channel_name_list[i],subscriber_num_list[i],not_int_subscriber_num[i],channel_url_list[i])
        result_list.append(new_node)



    driver.close()

    return result_list
