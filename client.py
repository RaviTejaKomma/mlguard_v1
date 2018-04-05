import socket   # Import socket module
def send_data(filename):
    try:
        s = socket.socket()            # Create a socket object
        host = '107.180.71.58'         # Get local machine name
        port = 8000                # Reserve a port for your service.
        s.connect((host, port))
        blob = open(filename,'rb').read()
        print('Actual image size: {}'.format(len(blob)))
        #raw_size = str.encode('{}\n{}'.format(image.size[0], image.size[1]))
        raw_size = str.encode('{}'.format(len(blob)))
        s.send(raw_size)
        x = 512
        y = 0
        while y < len(blob):
            s.send(blob[y:x])
            y = x
            x += 512

        # tell the server that the client is done sending the data
        s.send(b'sent')
        print("Data sent to the server successfully!")
    except KeyboardInterrupt as e:
        print("Exception is :",e)
    finally:
        s.close()
        print('Connection closed!')

if __name__ == "__main__":
    filename = input("Enter the file path : ")
    send_data(filename)