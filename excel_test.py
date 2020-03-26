import xlrd
import send_email as sm
import send_sms as ssms
import requests
from bs4 import BeautifulSoup as bs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


loc = 'C:\Users\hi\Dropbox\Nikhil\Solverfiles\AllPyScripts\Others\NLP\Template_Final.xlsm'

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

Name = sheet.cell_value(2, 1)
Website =  sheet.cell_value(3, 1)
URL = sheet.cell_value(4, 1)
Phone_no = sheet.cell_value(5, 1)
email = sheet.cell_value(6, 1)

print 'Name :- ',Name
print 'Website :- ',Website
print 'URL :- ',URL
print 'Phone_no :- ',Phone_no
print 'email :- ',email

def get_current_price(URL):
    response = requests.get(URL)
    soup = bs(response.content, 'html.parser')
    product_price = soup.find("div", class_="_1vC4OE _3qQ9m1")
    prduct_name = soup.find("span", class_="_35KyD6")
    price = float(product_price.text[1:].replace(",", ""))
    prod_name = prduct_name.text
    print price
    print prod_name
    return prod_name,price

def notify_registration_user():

    pname,pprice = get_current_price(str(URL))

    from_email = "saddlepoint.test@gmail.com"
    pwd = "saddlepoint@123"

    message = "Hi "+Name+",\n\n"+ "Thanks for Registering to Global Notify.\n\nCurrent price" \
            " for "+str(pname)+" is "+str(pprice)+".\n\nNotification well be sent to your registered " \
            "email/Phone when price drops below "+str(pprice)+".\n\nCheers :)"

    notif_subject = "Global Notify"
    sm.sendEmail(from_email,pwd,[email],notif_subject,Name,message)
    # ssms.sendSMS(Name,str(int(Phone_no)),message,notif_subject)

    print 'Registration Notification sent.'

def notify_price_drop_user():
    print 'In Price Drop Notif'

notify_registration_user()
