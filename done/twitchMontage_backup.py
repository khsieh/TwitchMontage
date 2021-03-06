from sys import stdin
from pprint import pprint
import numpy as np
import re, requests, json, urllib2, datetime, time, math, calendar, sys

#twitch api auth endpoint token
cid = "xjsxsufrpnglaom1ppv7j9jqr4n9vc"

#get video link from user
print "Give us a Twitch Video: "
vid_url = stdin.readline()

#get video id from link
id_index = vid_url.find("/videos/") + 8
vid_id = vid_url[id_index:-1]
#setup Kraken API 
twitch_kraken = "https://api.twitch.tv/kraken/videos/v"
twitch_kraken += vid_id
#set up http request with header
kraken_get = urllib2.Request(twitch_kraken)
kraken_get.add_header('Client-ID',cid)
vod_info_resp = urllib2.urlopen(kraken_get)
vod_info = json.load(vod_info_resp)

#getting vod info path from tumbnail preview
preview_data = vod_info["preview"]
path_start = preview_data.find('/s3_vods/')
path_end = preview_data.find('/thumb/')
vid_path = preview_data[path_start+9:path_end]

#fetching index-dvr.m3u8
#fastly.vod.hls.ttvnw.net/<video path>/<ENCODING>/index-dvr.m3u8
m3u8_url = "https://fastly.vod.hls.ttvnw.net/"
encoding_index = "/160p30/index-dvr.m3u8"
m3u8_url += vid_path
m3u8_url += encoding_index

#index-dvr.m3u8 IS HERE!
m3u8_download = urllib2.urlopen(m3u8_url)
# m3u8_data = json.load(m3u8_download)

# print m3u8_download.read()
# exit()


#getting broadcast started time for timestamps
broadcast_started = vod_info["created_at"]
broadcast_started = broadcast_started[11:19]
#broadcast start time in seconds
s_bs = time.strptime(broadcast_started,'%H:%M:%S')
s_bs = datetime.timedelta(hours=s_bs.tm_hour,minutes=s_bs.tm_min,seconds=s_bs.tm_sec).total_seconds()
# print s_bs


#fetching total length of vod in seconds
total_length = vod_info["length"]

###
# Snippet from https://github.com/KunaiFire/rechat-dl
# modified to work with our api token
# modified to clean up json for only time stamps
###
file_name = "rechat-" + vid_id + ".json"

CHUNK_ATTEMPTS = 6
CHUNK_ATTEMPT_SLEEP = 10

response = None
messages = []

print "\ndownloading chat messages for vod " + vid_id + "..."
while response == None or '_next' in response:
    
    query = ('cursor=' + response['_next']) if response != None and '_next' in response else 'content_offset_seconds=0'
    for i in range(0, CHUNK_ATTEMPTS):
        error = None
        try:
            twitch_v5 = "https://api.twitch.tv/v5/videos/" + vid_id + "/comments?" + query
            v5_get = urllib2.Request(twitch_v5)
            v5_get.add_header('Client-ID', cid)
            v5_response = urllib2.urlopen(v5_get)
            response = json.load(v5_response)
        except requests.exceptions.ConnectionError as e:
            error = str(e)
        else:
            if "errors" in response or not "comments" in response:
                error = "error received in chat message response: " + str(response)
        
        if error == None:
            messages += response["comments"]
            break
        else:
            print "\nerror while downloading chunk: " + error
            
            if i < CHUNK_ATTEMPTS - 1:
                print "retrying in " + str(CHUNK_ATTEMPT_SLEEP) + " seconds " + ""
                print "(attempt " + str(i + 1) + "/" + str(CHUNK_ATTEMPTS) + ")"
            
            if i < CHUNK_ATTEMPTS - 1:
                time.sleep(CHUNK_ATTEMPT_SLEEP)
    
    if error != None:
        sys.exit("max retries exceeded.")


print "saving to " + file_name

f = open(file_name, "w")
f.write(json.dumps(messages))
f.close()
print "messages download completed"
###
# End snippet
###


#clean up data from snippet
s_messages = []
# print response
with open(file_name) as data_file:
    data = json.load(data_file)
    for v in data:
        comment_time = v["created_at"]
        #clean up each time_stamp
        comment_time = comment_time[11:19]
        time_stamp = time.strptime(comment_time,'%H:%M:%S')
        s_time = datetime.timedelta(hours=time_stamp.tm_hour,minutes=time_stamp.tm_min,seconds=time_stamp.tm_sec).total_seconds()
        s_time -= s_bs
        # print "s_time:", s_time
        s_messages.append(s_time)

# print s_messages[len(s_messages)-1]

#caculate frequency
num_buckets = total_length/30
if total_length % 30 != 0:
    num_buckets+=1

buckets = [0]*num_buckets

# print s_messages

bucket_range = 30
bucket_lower = 0
bucket_upper = 30
bucket_num = 0

for msg in s_messages:
    if msg >= bucket_lower and msg < bucket_upper:
        buckets[bucket_num] += 1
    elif msg >= bucket_upper:
        bucket_num += 1
        if bucket_num > total_length or bucket_num >= num_buckets:
            break
        buckets[bucket_num] += 1
        bucket_lower += bucket_range
        bucket_upper += bucket_range
print buckets

#go through buckets to get time frames
num_tops = 5
tops = np.argsort(buckets)[::-1][:num_tops]
# print tops

highlights = []
for t in tops:
    peak = bucket_range*t
    highlights += peak

