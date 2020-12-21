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
    def __init__(self,insta_id,profile_url):
        self.insta_id = insta_id
        # self.profile_img = profile_img
        self.profile_url = profile_url

# 순서유지 LIST 중복 제거
def OrderedSet(list):
    my_set = set()
    res = []
    for e in list:
        if e not in my_set:
            res.append(e)
            my_set.add(e)

    return res

def insta_croller(search):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Instagram 자동로그인
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


    
    driver.get('https://www.instagram.com/accounts/login')
    driver.implicitly_wait(1)
    email = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
    email.send_keys("cellyapply9")
    password = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
    password.send_keys("10wonders123@",Keys.ENTER)
    time.sleep(3)
    
    result = []

    for i in range(len(relevent_keyword_list)):
        
        keyword = relevent_keyword_list[i]
        driver.get('https://www.instagram.com/explore/tags/'+keyword)    
        time.sleep(3)
        url_list = []    

        for a in range(1,4):
            for b in range(1,4):
                hot_post = WebDriverWait(driver,10).until(
                    EC.presence_of_element_located((By.XPATH,'//*[@id="react-root"]/section/main/article/div[1]/div/div/div['+str(a)+']/div['+str(b)+']/a'))
                )
                url_list.append(hot_post.get_attribute('href'))


        influencer_list = []
        for url in url_list:
            try:
                driver.get(url)
                influencer = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/header/div[2]/div[1]/div[1]/span/a').text

                if influencer not in influencer_list:
                    influencer_list.append(influencer)
            except TimeoutException :
                pass

        driver.get('https://www.instagram.com/explore/tags/'+keyword)
        time.sleep(2)      

        
        influencer_list = list(set(influencer_list))

        for t in range(len(influencer_list)):
            new_node = Result_node(influencer_list[t],'https://www.instagram.com/'+influencer_list[t])
            result.append(new_node)

    return result, relevent_keyword_list
