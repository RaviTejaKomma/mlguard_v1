import MySQLdb
import telepot
from telepot.loop import MessageLoop
import requests

def get_telegram_details(cid):
	conn = MySQLdb.connect(host="107.180.71.58", port=3306, user="root", passwd="root", db="mlcharts")
	cur = conn.cursor()
	query = "SELECT chat_id, chat_api FROM chat_table where cid=" + str(cid)
	cur.execute(query)
	result = cur.fetchall() 
	return result[0][0], result[0][1]
	
def send_to_telegram(cid):
	chat_id, chat_api = get_telegram_details(cid)
	print(cid)
	message = "Your MLGuard camera is DOWN !!"
	url = "https://api.telegram.org/bot"+chat_api+"/sendMessage?chat_id="+chat_id+"&text='"+message+"'"	
	r = requests.post(url)
	
def check_camera_status():
	conn = MySQLdb.connect(host="107.180.71.58", port=3306, user="root", passwd="root", db="mlcharts")
	cur = conn.cursor()
	query = "SELECT cid, status FROM check_camera"
	cur.execute(query)
	result = cur.fetchall()	
	for i in range(len(result)):
		if(result[i][1] == "Camera is not working"):
			send_to_telegram(result[i][0])
	
check_camera_status()