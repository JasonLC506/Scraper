from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions as exceptions
import time
from datetime import datetime
import random
import re

driver = webdriver.Firefox()
driver.implicitly_wait(30)
facebook_login = "http://www.facebook.com/login.php"
usemail = "jasonzhanglc1@gmail.com"
uspsw = "1992928zjs"
driver.get(facebook_login)
driver.find_element_by_id("email").send_keys("%s" % usemail)
driver.find_element_by_id("pass").send_keys("%s" % uspsw)
driver.find_element_by_name("login").submit()
time.sleep(1)



DATE_LAUNCH = datetime.strptime("March01 2016", "%B%d %Y")
TIME_SCROLL = 5
MAX_POSTS_PER = 20


def PostsText(url):
    driver.get(url)
    posts = []
    ######### scroll down ############
    ele_html = driver.find_element_by_tag_name("html")
    ele_posts = driver.find_elements_by_xpath("//div[@class='userContentWrapper _5pcr']")
    old_len = 0
    while len(ele_posts) > old_len and old_len < MAX_POSTS_PER:
        old_len = len(ele_posts)
        ele_html.send_keys(Keys.END)
        ele_posts = driver.find_elements_by_xpath("//div[@class='userContentWrapper _5pcr']")
        ####### later than emoticon launch ######
        ele_post = ele_posts[len(ele_posts) - 1]
        ele_time_post = ele_post.find_element_by_xpath(".//span[@class='timestampContent']")
        time_post = TimeParse(ele_time_post.text)
        if time_post < DATE_LAUNCH:
            break
        time_sleep = random.random() * TIME_SCROLL
        time.sleep(time_sleep)

    ######### scrape posts ############
    print len(ele_posts)
    for ele_post in ele_posts:
        ########## later than emoticon launch ##########
        ele_time_post = ele_post.find_element_by_xpath(".//span[@class='timestampContent']")
        time_post = TimeParse(ele_time_post.text)
        if time_post < DATE_LAUNCH:
            break
        # print "dada"
        likerlist = {}
        text = ""
        ####### text ###########
        try:
            ele_text = ele_post.find_element_by_xpath(".//div[@class='_5pbx userContent']/p")
            text = ele_text.text
        except exceptions.NoSuchElementException, e:
            print "no text"
            continue
        ####### likerlist #########
        try:
            ele_liker_link = ele_post.find_element_by_xpath(".//a[@class='_2x4v']")
            link_url = ele_liker_link.get_attribute("href")
            likerlist["url"] = link_url
        except exceptions.NoSuchElementException, e:
            print "no likes"
        post = {"text": text, "likerlist": likerlist}
        posts.append(post)
    for post in posts:
        post["likerlist"] = Likers(post["likerlist"])
    print posts
    return posts

def Likers(likerlist):
    link_url = likerlist["url"]
    driver.get(link_url)
    ele_ul = driver.find_element_by_xpath("//ul[@class ='uiList _5i_n _4kg _6-h _6-j _6-i']")
    ele_lis = ele_ul.find_elements_by_xpath("./li")
    for ele_li in ele_lis:
        ele_emoticon = ele_li.find_element_by_xpath("./div[@class ='_3p56']")
        emoticon = ele_emoticon.text
        ele_likers = ele_li.find_elements_by_xpath(".//a[@class ='_5i_s _8o _8r lfloat _ohe']")
        likers = []
        for ele_liker in ele_likers:
            likers.append(ele_liker.get_attribute("href"))
        likerlist[emoticon] = likers
    return likerlist

def TimeParse(str):
    #### str format March 12 * or March 12, 2015
    #### valid in 2016
    words = str.split()
    date_early = datetime.strptime("January01 2016","%B%d %Y")
    if "," in words[1]:
        return date_early
    elif not words[1].isnumeric():
        #### hrs or mins
        return datetime.now() # approximate now
    else:
        if len(words[1]) == 1:
            words[1] = "0" + words[1]
        time_post = words[0] + words[1] + " 2016"
        time_post = datetime.strptime(time_post, "%B%d %Y")
        return time_post

url = "https://www.facebook.com/playboy/?fref=nf"
PostsText(url)