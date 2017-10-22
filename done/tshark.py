###
# establish socket conection with given url
# wait until tshark fetches the index url
# closes the connection
###
import sys, os, socket, time

HOST = "https://go.twitch.tv"
PORT = 80

ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.settimeout(30)

# connet to host
try:
    ss.connect((HOST,PORT))
except: 
    print "Failure to connect to", HOST
    ss.close
    sys.exit()

#run tShark command here

#wait for response
#close connection
ss.close