import urllib2
from bs4 import BeautifulSoup

COOKIE = "datr=5X3TVfiAM3QQiCkegUS5tIg3; pl=n; lu=ggwN-OJhQCUlcVyiEI3SRZPg; a11y=%7B%22sr%22%3A0%2C%22sr-ts%22%3A1458667471389%2C%22jk%22%3A0%2C%22jk-ts%22%3A1458667471389%2C%22kb%22%3A1%2C%22kb-ts%22%3A1458667471389%2C%22hcm%22%3A0%2C%22hcm-ts%22%3A1458667471389%7D; p=-2; c_user=100010108026375; fr=0jcbdAz2wElKthFiD.AWUB0S-pwWeChLHr3J7CyFIS_BI.BV0336.R6.Fbx.0.AWVPWlNH; xs=139%3Ax37e4PQhckmCDA%3A2%3A1455920229%3A20772; csm=2; s=Aa5mFnUO8yBfRZNR.BWx5Rl; act=1458762977787%2F13; presence=EDvF3EtimeF1458763401EuserFA21B10108026375A2EstateFDsb2F0Et2F_5b_5dElm2FnullEuct2F14587533B00EtrFnullEtwF437305901EatF1458763400239G458763401170CEchFDp_5f1B10108026375F248CC; wd=724x615"

def PostFetch(url):
    handler = urllib2.HTTPHandler(debuglevel = 1)
    req = urllib2.Request(url)
    req.add_header("Cookie",(COOKIE))
    
    opener = urllib2.build_opener(handler)
    urllib2.install_opener(opener)
    
    resp = urllib2.urlopen(req)
    if resp.getcode() != 200:
        print "request error"
        print resp.getcode()
        return None
    ###### test
    data0 = resp.read()
    data = data0.replace("<!--","")
    data = data.replace("-->","")
    file = open("try.html","w")
    file.write(data)
    file.close()       
    print ("userContentWrapper _5pcr" in data)
    ############ parse ############
    
    soup = BeautifulSoup(data,"lxml")
    ########### test
    print soup.prettify()[0:1000]
    
    posts = soup.find_all("div",{'class':"userContentWrapper _5pcr"})
    postsTL = []
    print "num of post is %d" % len(posts)
    print posts[0]
    if len(posts) == 0:
        print "no posts"
        return None
    for post in posts:
        postT = []
        photos = post.find_all("div", class_="_3x-2")
        if len(photos)>0:
            continue
        posttexts = post.find_all("div", class_="_5pbx userContent")
        for posttext in posttexts:
            postT.append(posttext.p.get_text())
        ###### test
        print postT

PostFetch("https://www.facebook.com/RWirth")