import requests
import json
from bs4 import BeautifulSoup as bs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from bs4 import NavigableString
import pandas as pd

prod_price_details,Order_Details = {},{}
inp_prod = ["lights"]

inp_rating = raw_input('Rating of the Product on a scale of 5:-')
isbranded = raw_input('Branded (Y or N or Yes or No) :- ')

def flipkart(inp_prod):
    try:
        res = requests.get('https://www.flipkart.com/search?q='+str(inp_prod[0]).replace(" ","%20")+'&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off')
        soup_temp = bs(res.content, 'html.parser')
        page_num = soup_temp.findAll("div", class_="_2zg3yZ")
        for i in page_num:
            if 'Page' in str(i.text):
                a = str(i.text).split(' ')
                No_of_pages = a[3][:3]
    except Exception as x:
        print 'Error While getting No of pages'
        No_of_pages = 10
    print 'Total No of Pages found for Product:- ',inp_prod[0]

    for ip in inp_prod:
        page_count = 0
        for i in range(0,int(1)):
            try:
                response = requests.get('https://www.flipkart.com/search?q='+str(ip).replace(" ","%20")+'&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page='+str(i))
                stat_code = str(response.status_code)
                # if stat_code[0] == '2':
                page_count += 1
                prod_count = 0
                soup = bs(response.content, 'html.parser')
                product_details = soup.findAll("div", class_="_3liAhj _1R0K0g")
                for prod_details in  product_details:
                    prod_count += 1
                    prod_name = prod_details.find('a', {'class': '_2cLu-l'})
                    prod_name = prod_name.text
                    try:
                        price =  prod_details.find("div", class_="_1vC4OE")
                        price = float(price.text[1:].replace(",",""))
                    except Exception as x:
                        price = 0
                    try:
                        No_of_reviews = prod_details.find("span", class_="_38sUEc")
                        No_of_reviews = int(No_of_reviews.text.replace("(","").replace(")","").replace(",",""))
                    except Exception as x:
                        No_of_reviews = 0
                    try:
                        Rating = prod_details.find("div", class_="hGSR34")
                        Rating = Rating.text
                    except Exception as x:
                        Rating = 0
                    try:
                        Actual_Price = prod_details.find("div", class_="_3auQ3N")
                        Actual_Price = float(Actual_Price.text[1:].replace(",", ""))
                    except Exception as x:
                        Actual_Price = 0
                    try:
                        offer = prod_details.find("div", class_="VGWI6T")
                        offer = offer.text.split()[0].replace('%','')
                    except Exception as x:
                        offer = 0
                    Order_Details[prod_name+str(prod_count)] = [No_of_reviews,Rating,price,Actual_Price,offer]
                print 'No of Products in Products in page No',i,' -- ',len(Order_Details)
                # elif stat_code[0] in ['4','5']:
                #     print '******************************* Error :- Check URL *******************************'
                #     print 'Status Code:- ',stat_code
                #     break
            except Exception as x:
                print '******************* Connection lost at Page No:- '+str(page_count)+ '******************* '
                print 'Error :- ',x
                continue

        flipkart_df = pd.DataFrame.from_dict(Order_Details, orient='index',columns=["No_of_Reviews","Rating","Price","Actual_Price","offer"]).reset_index()
        flipkart_df[["Rating","offer"]] = flipkart_df[["Rating","offer"]].astype(float)
        filtered_flipkart_df = flipkart_df.loc[flipkart_df['Rating'] >= float(inp_rating)]
        if isbranded in ['n', 'N', 'NO', 'No', 'no']:
            sorted_flipkart_df = filtered_flipkart_df.sort_values(["No_of_Reviews","Rating","Price"], ascending=[False, False,True])
        elif isbranded == ['y','Y','YES','yes','Yes']:
            sorted_flipkart_df = filtered_flipkart_df.sort_values(["No_of_Reviews", "Rating", "Price"],ascending=[False, False, False])
        flipkart_top_deals = sorted_flipkart_df[:5]
        with pd.ExcelWriter('E:\\Flipkart.xlsx') as writer:
            flipkart_df.to_excel(writer, sheet_name='All Products')
            flipkart_top_deals.to_excel(writer, sheet_name='Best Deals')
            sorted_flipkart_df.to_excel(writer, sheet_name='Sorted Deals')
        writer.save()
        writer.close()

    return flipkart_df

flipkart_df = flipkart(inp_prod)
