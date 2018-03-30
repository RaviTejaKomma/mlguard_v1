import socket   # Import socket module
def send_data(filename):
    try:
        s = socket.socket()            # Create a socket object
        host = '107.180.71.58'         # Get local machine name
        port = 8000                    # Reserve a port for your service.
        s.connect((host, port))
        blob = open(filename,'rb').read()
        s.send(blob)
        print("Data sent to the server successfully!")
    except KeyboardInterrupt as e:
        print("Exception is :",e)
    finally:
        s.close()
        print('Connection closed!')

if __name__ == "__main__":
    filename = input("Enter the file path : ")
    send_data(filename)