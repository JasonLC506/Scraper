# import ast
# postfile = open("posts.txt","r")
# for item in postfile.readlines():
    # poster_post = ast.literal_eval(item)
    # poster = poster_post.keys()[0]
    # posts = poster_post[poster]
    # for post in posts:
        # print post["likerlist"]["url_liker"]
file = open("poster.txt","r")
posters = file.readlines()
posters = map(lambda x: x.rstrip(), posters)
n = 0
for i in range(len(posters)):
    if posters[i] in posters[:i]:
        print "duplicate"
        print "%d: " % i, posters[i]
        for j in range(i):
            if posters[j] == posters[i]:
                print "%d: " % j, posters[j]
        n += 1

print n
file.close()
# posters_set = list(set(posters))
# resultfile = open("poster_set.txt","w")
# for poster in posters_set:
#     resultfile.write("%s\n" % poster)
# resultfile.close()
