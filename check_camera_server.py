import MySQLdb
import telepot
from telepot.loop import MessageLoop
import requests
import logging

logging.basicConfig(filename='error_log.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

host_ip = "107.180.71.58"
port = 3306
user = "root"
pwd = "root"
db_name = "mlcharts"

def get_telegram_details(cid):
	conn = MySQLdb.connect(host=host_ip, port=port, user=user, passwd=pwd, db=db_name)
	cur = conn.cursor()
	query = "SELECT chat_id, chat_api FROM chat_table where cid=" + str(cid)
	cur.execute(query)
	result = cur.fetchall() 
	conn.close()
	return result[0][0], result[0][1]
	
def send_to_telegram(cid):
	chat_id, chat_api = get_telegram_details(cid)
	print(cid)
	message = "Your MLGuard camera is DOWN !!"
	url = "https://api.telegram.org/bot"+chat_api+"/sendMessage?chat_id="+chat_id+"&text='"+message+"'"	
	r = requests.post(url)
	
def check_camera_status():
	conn = MySQLdb.connect(host=host_ip, port=port, user=user, passwd=pwd, db=db_name)
	cur = conn.cursor()
	query = "SELECT cid, status FROM check_camera"
	cur.execute(query)
	result = cur.fetchall()	
	conn.close()
	for i in range(len(result)):
		if(result[i][1] == "Camera is not working"):
			send_to_telegram(result[i][0])

if __name__ == "__main__":
	try:
		check_camera_status()
	except Exception as e:
		logger.error(e)