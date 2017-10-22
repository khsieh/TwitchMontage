from sys import stdin
import shutil, re, requests, json, urllib2


#get video link from user
print "Give us a Twitch Video: "
vid_url = stdin.readline()

#get video id from link
id_index = vid_url.find("/videos/") + 8
vid_id = vid_url[id_index:]

#setup Kraken API 
twitch_kraken = "https://api.twitch.tv/kraken/videos/v"
twitch_kraken += vid_id
#set up http request with header
kraken_get = urllib2.Request(twitch_kraken)
kraken_get.add_header('Client-ID','xjsxsufrpnglaom1ppv7j9jqr4n9vc')
kraken_resp = urllib2.urlopen(kraken_get)
#json data dump
data = json.load(kraken_resp)

print data