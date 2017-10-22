
#given an input time and end time
#divide by 6 = x and y, take upper and lower clips 
#increment through extinf by x and y times
#or just do x =
#retrieve next line (example on parse text has this done)
#return next line to array/list/ whatever is storing the time frames for clip
#do while inputtime + 6 < end time


time_at_peak=13410

inputtime= time_at_peak-14 #given highlight times
endtime = time_at_peak+15

xint = inputtime/6 #timestamp of them in VoD
yint = endtime/6

length = (yint-xint)*2 #length for array 

results = [] #array for clips
cliptag = '#EXTINF:6.000,' # text tag on twitch document

count = 0 # to count through the time staps
extinfcount = 0 #tag count

file = open("index-dvr.m3u8").read().splitlines() #number the lines



while True: # do while 


	for index, line in enumerate(file): #twitch videofile
	

		count = xint    #highlight      
		if "EXTINF" in line: 

			extinfcount = extinfcount+1  # count through the timestamps
 		
			if extinfcount == count: 
				
				results = file[index+1:index+length] 	#store video timestaps in array 		
	inputtime=inputtime+6 
	if(endtime<=inputtime):  #end clip retrieval when 2nd time is less than initial time
		break			



while cliptag in results: results.remove(cliptag)  # remove tag from array

print results # print array
			




