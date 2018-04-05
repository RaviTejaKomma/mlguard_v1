# # server.py
import time,datetime  
import socket                       # Import socket module
from time import gmtime, strftime
import telepot
from telepot.loop import MessageLoop
import requests 


# if __name__ == "__main__": 

#     try:
#       port = 8000                     # Reserve a port for your service.
#       s = socket.socket()             # Create a socket object
#       host = '107.180.71.58'          # Get local machine name
#       s.bind((host, port))            # Bind to the port
#       s.listen(10)                    # Now wait for client connection.
#       print(socket.gethostname())
#       print('Server listening....')

#       while True:
#           conn, addr = s.accept()     # Establish connection with client.
#           print 'Got connection from', addr
#           data = conn.recv()

#           filename = "images/" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ".jpg"
#           f = open(filename,'wb')     # open the file
#           f.write(data)               # write the received data into the file
#           print("File saved")
#           f.close()                   #close the file

#           conn.send("Done")           #send the acknowledgement to the client
#           print("Sent back")
#     except KeyboardInterrupt as e:
#         s.close()
#         print("Exception is :", e)
#     finally:
#         s.close()

# from soaplib.core.service import rpc, DefinitionBase
# from soaplib.core.model.primitive import String, Integer
# from soaplib.core.model.clazz import Array
# from soaplib.core.model.binary import Attachment
# from soaplib.core.server import wsgi

# from tempfile import mkstemp
# import os

# class DocumentArchiver(DefinitionBase):

#     @soap(Attachment,_returns=String)
#     def archive_document(self,document):
#         '''
#         This method accepts an Attachment object, and returns the filename of the
#         archived file
#         '''
#         fd,fname = mkstemp()
#         os.close(fd)

#         document.file_name = fname
#         document.save_to_file()

#         return fname

#     @soap(String,_returns=Attachment)
#     def get_archived_document(self,file_path):
#         '''
#         This method loads a document from the specified file path
#         and returns it.  If the path isn't found, an exception is
#         raised.
#         '''
#         if not os.path.exists(file_path):
#             raise Exception("File [%s] not found"%file_path)

#         document = Attachment(file_name=file_path)
#         # the service automatically loads the data from the file.
#         # alternatively, The data could be manually loaded into memory
#         # and loaded into the Attachment like:
#         #   document = Attachment(data=data_from_file)
#         return document



# if __name__=='__main__':
#     from wsgiref.simple_server import make_server
#     soap_app = soaplib.core.Application([DocumentArchiver], 'tns')
#     wsgi_app = wsgi.Application(soap_app)
#     server = make_server('localhost', 7789, wsgi_app)
#     server.serve_forever()

bot = telepot.Bot("585184839:AAGaTVTymWCTEwk3xTOYL-QDAwo8jNonUkk")
url = "https://api.telegram.org/bot585184839:AAGaTVTymWCTEwk3xTOYL-QDAwo8jNonUkk/sendPhoto";

def sendImage(filename):
    print("Entered function")
    files = {'photo': open(filename, 'rb')}
    data = {'chat_id' : "460626793"}
    text_data = "Person Detected"
    bot.sendMessage(data['chat_id'], text=text_data)
    r= requests.post(url, files=files, data=data)
    print(r)

if __name__ == "__main__": 

    try:
        port = 8000                   # Reserve a port for your service.
        s = socket.socket()             # Create a socket object
        host = '107.180.71.58'          # Get local machine name
        s.bind((host, port))            # Bind to the port
        s.listen(10)                    # Now wait for client connection.
        print(socket.gethostname())
        print('Server listening....')

        while True:
            conn, addr = s.accept()     # Establish connection with client.
            print('Got connection from', addr)
            img_size = str(conn.recv(1024), 'utf-8', errors='ignore')
            # width = int(img_size.split('\n')[0])
            # height = int(img_size.split('\n')[1])

            raw_img = b''
            while True:
                raw_prt = conn.recv(512)
                # "sent" will be sent by the client indicating that all data has been transferred
                if b'sent' in raw_prt:
                    break
                raw_img += raw_prt

            print('Received image size: {}'.format(len(raw_img)))

            filename = strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ".jpg"
            f = open(filename,'wb')     # open the file
            f.write(raw_img)               # write the received data into the file
            print("File saved")
            f.close()                   #close the file
            print("File closed")
            sendImage(filename)
            print("Image sent to telegram")
            conn.send(b'Done')           #send the acknowledgement to the client
    except KeyboardInterrupt as e:
        s.close()
        print("Exception is :", e)
    finally:
        s.close()
