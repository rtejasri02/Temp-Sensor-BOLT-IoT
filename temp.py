import config
from boltiot import Sms,Email, Bolt

import json, time

minimum_limit = 150
maximum_limit = 160  

def buzzer_alert():
    response = mybolt.digitalWrite("0", "HIGH")		#Turning ON the buzzer
    data_b = json.loads(response)
    if data_b["success"]!=1:
        print("There was an error while sending a sound alert:", data_b["value"])
    time.sleep(1)					                 #Sounding the buzzer for 1 second
    response = mybolt.digitalWrite("0", "LOW")		#Turning OFF the buzzer


mybolt = Bolt(config.API_KEY, config.DEVICE_ID)
sms = Sms(config.SID, config.AUTH_TOKEN, config.TO_NUMBER, config.FROM_NUMBER)
mailer = Email(config.MAILGUN_API_KEY, config.SANDBOX_URL, config.SENDER_EMAIL, config.RECEPIENT_EMAIL)


while True: 
    print ("Reading sensor value")
    response = mybolt.analogRead('A0') 
    data = json.loads(response) 
    print("Sensor value is: " + str(data['value']))
    
    try: 
        sensor_value = int(data['value']) 
        if sensor_value > maximum_limit or sensor_value < minimum_limit:
            buzzer_alert()
            print("Making request to Twilio to send a SMS")
            Temperature=(100*sensor_value)/1024 
            response = sms.send_sms("The Current temperature is " +str(Temperature)+"(C)  CAUTION ! Anomaly Detected")
            print("Response received from Twilio is: " + str(response))
            print("Status of SMS at Twilio is :" + str(response.status))
            print("Making request to Mailgun to send an email")
            response = mailer.send_email("Alert!!", "The Current temperature is " +str(Temperature)+ "(C)")
           
            response_text = json.loads(response.text)
            print("Response received from Mailgun is: " + str(response_text['message']))
            
    except Exception as e: 
        print ("Error occured: Below are the details")
        print (e)
    time.sleep(10)
   