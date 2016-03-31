
def NumberParse(word):
    # type: (object) -> object
    #### large number #####
    if word.isnumeric():
        return int(word)
    elif "K" in word:
        word = word.replace("K" ,"")
        return int(float(word ) *1000)
    elif "M" in word:
        word = word.replace("M" ,"")
        return int(float(word ) *1000000)
    else:
        print "out of scope"
        return -1

if __name__ == "__main__":
    data1 = u"1.3K"
    data2 = u"1M"
    data3 = u"1002"
    print NumberParse(data1)
    print NumberParse(data2)
    print NumberParse(data3)
