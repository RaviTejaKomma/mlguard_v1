import telepot
from telepot.loop import MessageLoop
import requests 

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
    filename = input("Enter the path : ")
    sendImage(filename)
