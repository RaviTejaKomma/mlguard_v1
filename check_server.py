# Script to check if the server is running or not
import os
import requests
import time

def send_to_telegram():
	chat_id = '454098853'
	chat_api = '579446109:AAHoqiZCwRQriftAIwyeCEIfyRPGyZicHhI'
	message = "The server is down !! Please fix as soon as possible."
	url = "https://api.telegram.org/bot"+chat_api+"/sendMessage?chat_id="+chat_id+"&text='"+message+"'"	
	r = requests.post(url)
	
hostname = "107.180.71.58"

while(1):
	response = os.system("ping -c 1 " + hostname)
	if response == 0:
		print(hostname, ' is up!')
	else:
		print (hostname, ' is down!')
		send_to_telegram()
	time.sleep(300)
