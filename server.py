# server.py
import time,datetime  
import socket                       # Import socket module
from time import gmtime, strftime   


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
            print 'Got connection from', addr
            data = conn.recv(4096)

            filename = "images/" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ".jpg"
            f = open(filename,'wb')     # open the file
            f.write(data)               # write the received data into the file
            print("File saved")
            f.close()                   #close the file

            conn.send("Done")           #send the acknowledgement to the client
            print("Sent back")
    except KeyboardInterrupt as e:
        s.close()
        print("Exception is :", e)
    finally:
        s.close()