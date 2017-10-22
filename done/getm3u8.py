from sys import stdin
import shutil, re, requests, json, urllib2


#get video link from user
print "Give us a Twitch Video: "
vid_url = stdin.readline()

#get video id from link
id_index = vid_url.find("/videos/") + 8
vid_id = vid_url[id_index:]

#setup Kraken
twitch_kraken = "https://api.twitch.tv/kraken/videos/v"
twitch_kraken += vid_id
#set up http request with header
kraken_get = urllib2.Request(twitch_kraken)
kraken_get.add_header('Client-ID','xjsxsufrpnglaom1ppv7j9jqr4n9vc')
kraken_resp = urllib2.urlopen(kraken_get)
#json data dump
data = json.load(kraken_resp)
path = data["preview"]
#find path from thumbnail preview
path_start = path.find('/s3_vods/')
path_end = path.find('/thumb/')
#parse for vid_path
vid_path = path[path_start+9:path_end]

#fastly.vod.hls.ttvnw.net/<video path>/<ENCODING>/index-dvr.m3u8
m3u8_url = "https://fastly.vod.hls.ttvnw.net/"
encoding_index = "/160p30/index-dvr.m3u8"
m3u8_url += vid_path
m3u8_url += encoding_index

#download m3u8 file
m3u8_download = urllib2.urlopen(m3u8_url)
print m3u8_download.read()