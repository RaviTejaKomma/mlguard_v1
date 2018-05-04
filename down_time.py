import os
import MySQLdb
import time
from datetime import datetime
import telepot
from telepot.loop import MessageLoop
import requests
import logging

logging.basicConfig(filename='error_log.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

def check_status():
	uptimes_all = {}
	down_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	down_time = datetime.strptime(down_time, '%Y-%m-%d %H:%M:%S')
	
	query =  "SELECT cid, last_uptime FROM uptime"
	conn = MySQLdb.connect(host="107.180.71.58", port=3306, user="root", passwd="root", db="mlcharts")
	cur=conn.cursor()   
	cur.execute(query)
	rows = cur.fetchall()
	
	for i in range(len(rows)):
		uptimes_all[rows[i][0]] = rows[i][1]    
		
	for cid, uptime in uptimes_all.items():     
		if uptime == None:
			uptime = datetime.strptime('2018-03-15 00:00:00', '%Y-%m-%d %H:%M:%S')
		diff_time = down_time-uptime
		#print("Difference is ", diff_time.seconds)     
		if(diff_time.seconds > 3900):
			#print("MLGuard "+str(cid)+" is down !!")           
			store_downtime(cid)
		else:
			print("MLGuard "+str(cid)+" is up !!")
	
def store_downtime(cid):    
	down_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	query = "INSERT INTO downtime(cid,last_downtime) VALUE('" + str(cid) + "','" + str(down_time) + "')"    
	try:
		conn = MySQLdb.connect(host="107.180.71.58", port=3306, user="root", passwd="root", db="mlcharts")
		cur=conn.cursor()   
		cur.execute(query)
		conn.commit()   
	except Exception as e:
		cur.rollback()
	conn.close()
	print("DownTime logged")
	

if __name__ == "__main__":
	try:
		check_status()
	except Exception as e:
		logger.error(e)