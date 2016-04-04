from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions as exceptions
import time
from datetime import datetime
import random
from post_selenium import TimeParse

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
TIME_SCROLL = 20
TIME_NEWPAGE = 10
TIME_LOAD = 2
MAX_SHOW_MORE = 10000
MAX_POST_PER = 10

def PosterPost(root, posters):
    ##### BFS find large set of poster through post-like relation ####
    ##### similar to PostsFetch in post_selenium but compacter ####
    driver.get(root)
    url_likers = []
    ######### scroll down ############
    ele_html = driver.find_element_by_tag_name("html")
    try:
        ele_posts = driver.find_elements_by_xpath("//div[@class='userContentWrapper _5pcr']")
    except exceptions.NoSuchElementException, e:
        print "no posts"
        return posters
    old_len = 0
    while len(ele_posts) > old_len and old_len < MAX_POST_PER:
        old_len = len(ele_posts)
        print "old_len is %d" % old_len
        ele_html.send_keys(Keys.END)
        time.sleep(TIME_LOAD)
        ele_posts = driver.find_elements_by_xpath("//div[@class='userContentWrapper _5pcr']")
        print "new_len is %d" % len(ele_posts)
        ####### later than emoticon launch ######
        ele_post = ele_posts[len(ele_posts) - 1]
        try:
            ele_time_post = ele_post.find_element_by_xpath(".//span[@class='timestampContent']")
            time_post = TimeParse(ele_time_post.text)
        except:
            print "error: ele_time_post not found"
            continue

        if time_post < DATE_LAUNCH:
            print "too early"
            break
        time_sleep = random.random() * TIME_SCROLL
        time.sleep(time_sleep)
    ######## scrape posts #############   
    for ele_post in ele_posts:
        try:
            ele_liker_link = ele_post.find_element_by_xpath(".//a[@class='_2x4v']")
            link_url = ele_liker_link.get_attribute("href")
            url_likers.append(link_url)
        except exceptions.NoSuchElementException, e:
            print "no likes"
    ######## scrape likers ##############
    for url_liker in url_likers:
        driver.get(url_liker)
        ########### show all #############
        liker_new = 0
        for i in range(MAX_SHOW_MORE):
            print "%dth show more" % i
            try:
                ele_showmore = driver.find_element_by_xpath("//div[@class = 'clearfix mtm uiMorePager stat_elem _52jv']/div/a")
                ele_showmore.click()
                time.sleep(TIME_LOAD)
                ele_likers = driver.find_elements_by_xpath("//ul[@class ='uiList _5i_n _4kg _6-h _6-j _6-i']\
                /li//a[@class ='_5i_s _8o _8r lfloat _ohe']")
                # if len(ele_likers) == liker_old:
                #     print "no more"
                #     break
                # else:
                #     liker_old = len(ele_likers)
                resultfile = open("poster.txt", "a")
                for ele_liker in ele_likers:
                    liker = ele_liker.get_attribute("href")
                    if liker not in posters:
                        posters.append(liker)
                        resultfile.write("%s\n" % liker)
                        liker_new += 1
                resultfile.close()
                print datetime.now()
                print "already %d new poster from this post" % liker_new
                time_sleep = random.random() * TIME_SCROLL
                time.sleep(time_sleep)
            except exceptions.NoSuchElementException, e:
                print "no more"
                print "got %d likers in this post" % (len(ele_likers))
                break
        print "%d posters until now" % len(posters)
        print datetime.now()
        time_sleep = random.random() * TIME_NEWPAGE
        time.sleep(time_sleep)
    return posters


def PosterBSF(root, depth=1):
    try:
        resultfile = open("poster.txt","r")
        posters = resultfile.readlines()
        posters = map(lambda x: x.rstrip(),posters)
        resultfile.close()
    except:
        posters = []
    posters = PosterPost(root, posters)
    ind_new_poster = 0
    for d in range(depth - 1):
        L = len(posters)
        for i in range(ind_new_poster, L):
            posters = PosterPost(posters[i], posters)
        ind_new_poster = L
    print "crawl %d posters" % len(posters)
    return posters


if __name__ == "__main__":

    posters = PosterBSF("https://www.facebook.com/zuck")
    print len(posters)
