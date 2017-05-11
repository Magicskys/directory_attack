#coding:utf-8
import urllib2
import threading
import Queue
import sys

threads=25
target_url=sys.argv[1]
wordlist_file=sys.argv[2]
header={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0"}
write_list = []

def build_wordlist(wordlist_file,extension):
    fd=open(wordlist_file,"rb")
    raw_words=fd.readlines()
    fd.close()

    words=Queue.Queue()
    for word in raw_words:
        word=word.rstrip()
        if extension is not None:
            word=word.replace("%.type%",extension)
            words.put(word)
            print word
        else:
            words.put(word)
            print word

    return words

def dir_bruter(word_queue):
    while not word_queue.empty():
        attempt=word_queue.get()
        try:
            req=urllib2.Request(target_url+attempt,headers=header)
            response=urllib2.urlopen(req)
            if len(response.read()) and response.code!=404:
                write_list.append("[*]%d=>%s"%(response.code,target_url+attempt))
        except urllib2.HTTPError,e:
            if hasattr(e,'code') and e.code!=404:
                write_list.append("[!]%d=>%s"%(e.code,target_url+attempt))
            pass


if __name__ == '__main__':
    try:
        extension=sys.argv[3]
    except:
        extension=None
    word_queue=build_wordlist(wordlist_file,extension)
    for i in range(threads):
        t=threading.Thread(target=dir_bruter(word_queue))
        t.start()
    print write_list
    with open("./log.txt", "w") as f:
        for i in range(len(write_list)):
            f.write(write_list[i]+'\n')
