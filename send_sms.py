import requests

def sendSMS(name,phone_number,message,sms_subject):
    Found_Screens_String = message

    url = "https://www.fast2sms.com/dev/bulk"
    payload = "sender_id=FSTSMS&message="+str(sms_subject)+"\n" + str(Found_Screens_String) + " \
              ""&language=unicode&route=p&numbers="+phone_number
    headers = {
        'authorization': "PErkusfSq7XctRiwH0G6Wbp1m9Q8ogMz2VFnIlKvLJThxB5CaNCj4ye908klaUxWuzFvOB3ArsY7Shbd",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)

