from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions as exceptions
import time
from datetime import datetime
import random
from NumberParse import NumberParse


driver = webdriver.Firefox()
driver.implicitly_wait(30)
facebook_login = "http://www.facebook.com/login.php"
usemail = "jasonzhanglc3@gmail.com"
uspsw = "1992928zjs"
driver.get(facebook_login)
driver.find_element_by_id("email").send_keys("%s" % usemail)
driver.find_element_by_id("pass").send_keys("%s" % uspsw)
driver.find_element_by_name("login").submit()
time.sleep(1)



DATE_LAUNCH = datetime.strptime("March01 2016", "%B%d %Y")
TIME_SCROLL = 20
TIME_NEWPAGE = 10
TIME_LOAD = 2
MAX_POSTS_PER = 100
MAX_SHOW_MORE = 10000

def PostsFetch(url):
    driver.get(url)
    posts = []
    ######### scroll down ############
    ele_html = driver.find_element_by_tag_name("html")
    try:
        ele_posts = driver.find_elements_by_xpath("//div[@class='userContentWrapper _5pcr']")
    except exceptions.NoSuchElementException, e:
        print "no posts"
        return posts
    old_len = 0
    while len(ele_posts) > old_len and old_len < MAX_POSTS_PER:
        old_len = len(ele_posts)
        ele_html.send_keys(Keys.END)
        time.sleep(TIME_LOAD)
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
            break # default the post order in ele_posts is temporal

        likerlist = {}
        emoticons = {}
        text = ""
        url_post = ""
        
        ####### url_post ###########
        try:
            ele_url_post = ele_post.find_element_by_xpath(".//a[@class = '_5pcq']")
            url_post = ele_url_post.get_attribute("href")
        except exceptions.NoSuchElementException, e:
            print "inormal post"
            continue
        ####### text ###########
        try:
            ele_text = ele_post.find_element_by_xpath(".//div[@class='_5pbx userContent']/p")
            text = ele_text.text
        except exceptions.NoSuchElementException, e:
            print "no text"
            #continue
        ####### url_liker #########
        try:
            ele_liker_link = ele_post.find_element_by_xpath(".//a[@class='_2x4v']")
            link_url = ele_liker_link.get_attribute("href")
            likerlist["url_liker"] = link_url
        except exceptions.NoSuchElementException, e:
            print "no likes"
            continue
        ####### liker numbers #########
        ele_liker_link = ele_post.find_element_by_xpath(".//a[@class='_2x4v']")
        ele_liker_link.click()
        time.sleep(TIME_LOAD)
        ele_emoticons = driver.find_elements_by_xpath(".//li[@class='_ds- _45hc']/a/span/span")
        if len(ele_emoticons) == 0:
            try:
                ele_emoticon = driver.find_element_by_xpath(".//li[@class='_ds- _45hc _1hqh']/a/span/span")
                emoticonstatus = ele_emoticon.get_attribute("aria-label")
                words = emoticonstatus.split()
                emoticon = words[-1]
                num = NumberParse(words[1])
                emoticons[emoticon] = num
            except exceptions.NoSuchElementException, e:
                print "no likes"
        for ele_emoticon in ele_emoticons:
            emoticonstatus = ele_emoticon.get_attribute("aria-label")
            words = emoticonstatus.split()
            emoticon = words[-1]
            num = NumberParse(words[1])
            emoticons[emoticon] = num
        time_sleep = random.random() * TIME_SCROLL
        time.sleep(time_sleep)
        print emoticons

        post = {"url_post": url_post, "emoticons": emoticons, "text": text, "likerlist": likerlist}
        posts.append(post)
    ############ crawl likers #################   
    # for post in posts:
    #     post["likerlist"] = Likers(post["likerlist"])
    #     time_sleep = random.random() * TIME_NEWPAGE
    #     time.sleep(time_sleep)
    print posts
    return posts

def Likers(likerlist):
    link_url = likerlist["url_liker"]
    driver.get(link_url)
    ########### show all #############
    liker_old = 0
    for i in range(MAX_SHOW_MORE):
        print "%dth show more" % i
        ele_showmore = driver.find_element_by_xpath("//div[@class = 'clearfix mtm uiMorePager stat_elem _52jv']/div/a")
        ele_showmore.click()
        time.sleep(TIME_LOAD)
        ele_likers = driver.find_elements_by_xpath("//ul[@class ='uiList _5i_n _4kg _6-h _6-j _6-i']\
        /li//a[@class ='_5i_s _8o _8r lfloat _ohe']")
        if len(ele_likers) == liker_old:
            print "no more"
            break
        else:
            liker_old = len(ele_likers)
        time_sleep = random.random() * TIME_SCROLL
        time.sleep(time_sleep)
    ########## write to list ###########
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
    date_early = datetime.strptime("January01 2016","%B%d %Y")
    words = str.split()
    if len(words)<2:
        print words
        return date_early
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
        
if __name__ =="__main__":
    posts = []
    n = 10000    ### crawl n posters
    posterfile = open("poster.txt","r")
    ######### skip first k posters #####
    k = 0     ### skip first k posters
    for i in range(k):
        posterfile.readline()
    ######### crawl n posters ###########
    posters = []
    for i in range(n):
        posters.append(posterfile.readline())
    print "total %d posters" % len(posters)
    posterfile.close()
    i = k
    for poster in posters:
        print "%dth poster" % (i+1)
        url = poster.rstrip()
        poster_post = {}
        poster_post[url]=PostsFetch(url)
        posts.append(poster_post)
        i += 1
        postfile = open("posts.txt","a")
        postfile.write(str(poster_post))
        postfile.write("\n")
        postfile.close()
    # url = "https://www.facebook.com/playboy/?fref=nf"
    # PostsFetch(url)
