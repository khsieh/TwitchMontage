import json
import datetime
import time

jsong = open('text.json')
data = json.load(jsong)
jsong.closed
first = True
first_time = 0
with open('timestamps.txt','w+') as f:
	for object in data:
		string = object["created_at"]
		string = string[11:19]
		x = time.strptime(string,'%H:%M:%S')
		float_val = datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()
		if first:
			first_time = float_val
			first = False
		float_val -= first_time
		f.write(str(float_val) + "\n")
		
f.closed
