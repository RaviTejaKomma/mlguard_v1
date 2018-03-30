# server.py
import time,datetime  
import socket                       # Import socket module
from time import gmtime, strftime 
import telepot
from telepot.loop import MessageLoop
import requests

bot = telepot.Bot('585184839:AAGaTVTymWCTEwk3xTOYL-QDAwo8jNonUkk')
def sendImage(filename):
    url = "https://api.telegram.org/bot585184839:AAGaTVTymWCTEwk3xTOYL-QDAwo8jNonUkk/sendPhoto";
    files = {'photo': open(filename, 'rb')}
    data = {'chat_id' : "460626793"}
    text_data = "Person Detected"
    bot.sendMessage(data['chat_id'], text=text_data)
    r = requests.post(url, files=files, data=data)
    #print(r.status_code, r.reason, r.content)  


if __name__ == "__main__": 

    try:
        port = 8000                     # Reserve a port for your service.
        s = socket.socket()             # Create a socket object
        host = '107.180.71.58'          # Get local machine name
        s.bind((host, port))            # Bind to the port
        s.listen(10)                    # Now wait for client connection.
        print(socket.gethostname())
        print('Server listening....')

        while True:
            conn, addr = s.accept()     # Establish connection with client.
            print('Got connection from', addr)
            data = conn.recv(4096)

            filename = "../images/" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ".jpg"
            f = open(filename,'wb')     # open the file
            f.write(data)               # write the received data into the file
            print("File saved")
            f.close()                   #close the file

            sendImage(filename)         # send images to telegram

            conn.send(b'Done')           #send the acknowledgement to the client
            print("Sent back")
    except KeyboardInterrupt as e:
        s.close()
        print("Exception is :", e)
    finally:
        s.close()