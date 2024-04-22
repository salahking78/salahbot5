import telebot
import hashlib
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import requests

bot = telebot.TeleBot('7100805143:AAFuIuWZFNig0TZMf0BFC2WXqdPc3Zcz5l4')

START, PHONE, PASSWORD = range(3)
current_state = {}
phone_pattern = r"01[0-9]{9}$"

@bot.message_handler(commands=['start'])

def start (message):
 
        current_state[message.chat.id] = PHONE
        msg = bot.send_message(message.chat.id, "قم بإدخال رقم هاتفك")
        bot.register_next_step_handler(msg, process_phone_step)
        
def process_phone_step(message):
    current_state[message.chat.id] = PASSWORD
    phone_number = message.text
    current_state['nu'] = phone_number
    user_data = {
        "phone_number": phone_number,
    }

    msg = bot.send_message(message.chat.id, "قم بإدخال كلمة مرور تطبيق أورنج")
    bot.register_next_step_handler(msg, process_password_step, user_data=user_data)

def process_password_step(message, user_data):
    current_state['pas'] = message.text
    nu = current_state['nu']
    pas = current_state['pas']
 
    url = "https://services.orange.eg/GetToken.svc/GenerateToken"

    header = {
"Content-type":"application/json", 
  "Content-Length":"78", 
  "Host":"services.orange.eg",
    "Connection":"Keep-Alive" ,
    "User-Agent":"okhttp/3.12.1"
            }

    data = '{"appVersion":"2.9.8","channel":{"ChannelName":"MobinilAndMe","Password":"ig3yh*mk5l42@oj7QAR8yF"},"dialNumber":"%s","isAndroid":true,"password":"%s"}' %(nu,pas)    
    ctv = requests.post(url,headers=header,data = data).json()["GenerateTokenResult"]["Token"]
    
    key = ',{.c][o^uecnlkijh*.iomv:QzCFRcd;drof/zx}w;ls.e85T^#ASwa?=(lk'
    
    htv=(str(hashlib.sha256((ctv+key).encode('utf-8')).hexdigest()).upper())

    		
    url2 = "https://services.orange.eg/SignIn.svc/SignInUser"


    header2 = {
"ctv": ctv,
"htv": htv,
"net-msg-id": "61f91ede006159d16840827295301013",
"x-microservice-name": "APMS",
"Content-Type": "application/json; charset=UTF-8",
"Content-Length": "166",
"Host": "services.orange.eg",
"Connection": "Keep-Alive",
"Accept-Encoding": "gzip",
"User-Agent": "okhttp/3.14.9",
    }
    data2= '{"appVersion":"2.9.8","channel":{"ChannelName":"MobinilAndMe","Password":"ig3yh*mk5l42@oj7QAR8yF"},"dialNumber":"%s","isAndroid":true,"password":"%s"}' % (nu,pas)     
    r2 = requests.post(url2, headers=header2,data=data2).json()
    hk=r2["SignInUserResult"]["ErrorCode"]
    
    if hk == 0:
    	
    	msg = bot.send_message(message.chat.id, "تم تسجيل الدخول للحساب بنجاح ")
    	
    	msg = bot.send_message(message.chat.id, "انتظر يتم الحصول علي العرض")
    	
    else:
    		
    		msg = bot.send_message(message.chat.id, "رقم الهاتف او كلمة المرور خطأ اعد المحاولة مره اخري")
    		
    		return
            
                    
    
    url3="https://services.orange.eg/APIs/Entertainment/api/EagleRevamp/Fulfillment"
    
    data3='{"ChannelName":"MobinilAndMe","ChannelPassword":"ig3yh*mk5l42@oj7QAR8yF","Dial":"%s","Language":"ar","Password":"%s","ServiceID":"5"}' %(nu,pas)
    
    header3={
    "_ctv": ctv,
"_htv": htv,
"net-msg-id": "c9e426a1017474d16840837286861043",
"x-microservice-name": "APMS",
"Content-Type": "application/json; charset=UTF-8",
"Content-Length": "142",
"Host": "services.orange.eg",
"Connection": "Keep-Alive",
"Accept-Encoding": "gzip",
"User-Agent": "okhttp/3.14.9",
    }
    
    r3=requests.post(url3,headers=header3,data=data3).json()
    
    pl=r3["ErrorCode"]
    
    if pl == 0:
    	msg = bot.send_message(message.chat.id, "تم الحصول علي العرض بنجاح ")
    	
    else:
    		
    		msg = bot.send_message(message.chat.id, "انت مشترك في العرض بالفعل ")
    		
if __name__ == '__main__':
    bot.polling(none_stop=True)
    print("")
    print(" تم تشغيل البوت بنجاح")
   

    
