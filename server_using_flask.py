from flask import Flask, request, Response
import jsonpickle
import numpy as np
import base64
from PIL import Image
from io import BytesIO
import telepot
from telepot.loop import MessageLoop
import requests
import datetime
import MySQLdb

bot = telepot.Bot("585184839:AAGaTVTymWCTEwk3xTOYL-QDAwo8jNonUkk")
url = "https://api.telegram.org/bot585184839:AAGaTVTymWCTEwk3xTOYL-QDAwo8jNonUkk/sendPhoto";

def sendImage(filename):
    files = {'photo': open(filename, 'rb')}
    data = {'chat_id' : "460626793"}
    text_data = "Person Detected"
    bot.sendMessage(data['chat_id'], text=text_data)
    r= requests.post(url, files=files, data=data)
    print("Image sent to telegram")

def log_in_db(filename):
    company_id = 3
    blob_value = open(filename,'rb').read()
    in_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = MySQLdb.connect(host="107.180.71.58",
              port=3306,
              user="root",
              passwd="root",
              db="mlcharts")
    cur=conn.cursor()
    cur.execute("""INSERT INTO faces_log(face_image,in_time,cid,name) VALUES (%s,%s,%s,%s)""",(blob_value,in_time,company_id,'UNKNOWN'))
    conn.commit()
    print("Logged Successfully")

# Initialize the Flask application
app = Flask(__name__)

# route http posts to this method
@app.route('/api/test', methods=['POST'])
def test():
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # # decode image

    img = base64.b64decode(nparr)
    file_like = BytesIO(img)
    img = Image.open(file_like)
    present_time = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    filename = "../images/"+ present_time +".jpg"
    img.save(filename)
    # do some fancy processing here....

    # build a response dict to send back to client
    response = {'message': 'image received'}
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)
    print("Image Recieved")

    sendImage(filename)
    log_in_db(filename)

    return Response(response=response_pickled, status=200, mimetype="application/json")

# start flask app
app.run(host="107.180.71.58", port=5000)