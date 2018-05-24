from flask import Flask, request, Response
import numpy as np
import json
import base64
from PIL import Image
from io import BytesIO
import telepot
from telepot.loop import MessageLoop
import requests
import datetime
import MySQLdb
import pickle
from threading import Thread
import logging
from pytz import timezone  

logging.basicConfig(filename='error_log.log', level=logging.ERROR, 
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

def get_connection():
	conn = MySQLdb.connect(host="107.180.71.58",
			  port=3306,
			  user="root",
			  passwd="root",
			  db="mlcharts")
	return conn

def retrieve_telegram_details(cid):
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("SELECT chat_id,chat_api from chat_table WHERE cid="+str(cid))
	data = cur.fetchall()
	conn.close()
	chat_id = data[0][0]
	chat_api = data[0][1]
	return [chat_id,chat_api]

def sendImage(filename, cid, flag, client_timezone):
	tz = timezone(client_timezone)
	present_time = datetime.datetime.now(str(tz)).strftime('%Y-%m-%d %H:%M:%S')
	chat_id, chat_api = retrieve_telegram_details(cid)
	bot = telepot.Bot(chat_api)
	url = "https://api.telegram.org/bot"+chat_api+"/sendPhoto"
	files = {'photo': open(filename, 'rb')}
	text_data = "Person Detected"
	if(flag == 10):
		text_data = "Person Detected after server failure in MLGuard-" + str(cid) + " at " + str(present_time)
	elif(flag==0):
		text_data = "Person Detected in MLGuard-" + str(cid) + " at " + str(present_time)
	else:
		text_data = 'MLGuard-' + str(cid) + 'has started at ' + str(present_time)
	data = {'chat_id' : chat_id, "caption":text_data}
	r= requests.post(url, files=files, data=data)
	print("Image sent to telegram")

def log_in_db(filename, cid):
	blob = open(filename,'rb').read()
	encoded_blob = base64.b64encode(blob)
	in_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	try:
		conn = get_connection()
		cur = conn.cursor()
		cur.execute("""INSERT INTO faces_log(face_image,in_time,cid,name) VALUES (%s,%s,%s,%s)""",(encoded_blob,in_time,cid,'UNKNOWN'))
		conn.commit()
	except Exception as e:
		conn.rollback()
		logger.error(e)
	conn.close()
	print("Logged Successfully")
	
def log_in_db_cam_status(filename, cid):
	blob = open(filename,'rb').read()
	encoded_blob = base64.b64encode(blob)
	in_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	try:
		conn = get_connection()
		cur = conn.cursor() 
		cur.execute("""UPDATE check_camera SET image=%s, in_time=%s where cid=%s""",(encoded_blob, in_time, cid))
		conn.commit()
	except Exception as e:
		conn.rollback()
		logger.error(e)
	conn.close()
	print("Logged Successfully")

def send_error_to_telegram(msg):
	chat_id = '454098853'
	chat_api = '579446109:AAHoqiZCwRQriftAIwyeCEIfyRPGyZicHhI'
	message = msg
	url = "https://api.telegram.org/bot"+chat_api+"/sendMessage?chat_id="+chat_id+"&text='"+message+"'"	
	r = requests.post(url)	

# Initialize the Flask application
app = Flask(__name__)

# route http posts to this method
@app.route('/api/test', methods=['POST'])
def test():
	try:
		data = pickle.loads(request.data)
		cid = int(data['cid'])
		client_timezone = data['timezone']
		# # decode image
		img = base64.b64decode(data['img'])
		file_like = BytesIO(img)
		img = Image.open(file_like)
		present_time = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
		filename = "../images/"+present_time +".jpg"
		img.save(filename)
		# do some fancy processing here....

		# build a response dict to send back to client
		response = {'message': 'image received'}

		# encode response using json
		response_pickled = json.dumps(response)
		print("Image Recieved")

		if(int(data['flag']) == 0):
			log_in_db(filename, cid)
		else:
			log_in_db_cam_status(filename, cid)
		thread = Thread(target = sendImage, args = (filename, cid, int(data['flag']), client_timezone))
		thread.start()

		return Response(response=response_pickled, status=200, mimetype="application/json")
	except Exception as e:
		logger.error(e)	
		send_error_to_telegram('There is an error in the server. Please fix as soon as possible')

# start flask app
print('Server has started running.')
app.run(host="192.168.50.252", port=5000)