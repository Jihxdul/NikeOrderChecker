from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import json
import time
import datetime

products = {}
name = ""
sizes = []
totalorders = 0

def retrieve_webhook(channelid): 
    headers = { #fill with your own authorization token below
        'authorization': 'REPLACE HERE' 
    }
    r = requests.get(f'https://discord.com/api/v9/channels/{channelid}/messages', headers=headers)
    jsonn = json.loads(r.text)
    sku = input("Enter your SKU: ")
    print('\n')
    for webhook in jsonn:
        for embed in webhook['embeds']:
            for fields in embed['fields']:
                if sku in fields['value']:
                    for fields in embed['fields']:
                        if fields['name'] == "**Email**":
                            temp = fields['value']
                            temp2 = temp.replace('|',"")
                            products[temp2] = None
                        if fields['name'] == "**OrderId**":
                            temp3 = fields['value']
                            temp4 = temp3.replace('|',"")
                            products[temp2] = temp4  
                        if fields['name'] == "**Product Name**":
                            global name
                            name = fields['value']
                        if fields['name'] == "**Size**":
                            sizes.append(fields['value'])
     
retrieve_webhook(1234567890)#Place ChannelID here

def checkstat(dict,name):
    headers = { #fill with your own authorization token below
        'authorization': 'REPLACE HERE' 
    }
    tracking_channelID = 1234567890 #Place tracking ChannelID here

    date = datetime.datetime.now()
    now = date.strftime("%m-%d-%y %H:%M:%S")
    

    PATH = "chromedriver.exe"
    driver = webdriver.Chrome(PATH)
 
    totalorders = len(dict)
    line = "-------------------START CHECK-------------------"
    
    payload = {
                 'content': "```{}\n{}\n{} \nTotal Orders: {}```".format(line,now,name,totalorders)
            }
    r = requests.post(f'https://discord.com/api/v9/channels/{tracking_channelID}/messages',data=payload, headers=headers)
    i = 0
    for key in dict:
        driver.get('https://www.nike.com/orders/details/')
        orderNumber = driver.find_element(By.ID,'orderNumber')
        email = driver.find_element(By.ID,'email')
        on = dict[key]
        if on == "NULL":
            continue
        mail = key
        orderNumber.send_keys(on)
        time.sleep(2)
        email.send_keys(mail)
        time.sleep(2)
        email.submit()
        time.sleep(2)
       
        ONholder = driver.find_element(By.CSS_SELECTOR, "#order-detail-wrapper > div > div > div.mb0-sm.mb9-xl.ncss-col-sm-12.ncss-col-xl-8.va-sm-t > div.m-md-12 > div > div > div.shipment-status-messaging.mb3-sm.u-full-width > div")
        status = ONholder.text
        addyholder = driver.find_element(By.CSS_SELECTOR, "#order-detail-wrapper > div > div > div.ncss-col-sm-12.ncss-col-xl-3.ncss-col-xl-offset-1.va-sm-t.mb9-sm > div > div.order-overview > div.css-0.order-detail-panel-overview-shipping-addresses.pb6-sm.prl0-sm.pt4-md.pt6-sm > div > div > div.flx-gro-sm-1.ta-sm-r > div > p:nth-child(1)")
        addy = addyholder.text
        
        if status == "Shipped":
            trackingbutton = driver.find_element(by=By.LINK_TEXT, value = "Track Shipment")
            number = trackingbutton.get_attribute('href')
            payload = {
                 'content': "```Order Number: {} \nEMAIL: {} \nSIZE: {} \nADDRESS: {} \nSTATUS: {} \nTRACKING:{}\nLINK BELOW:``` {}".format(on, mail, sizes[i], addy, status,number,number)
            }
            r = requests.post(f'https://discord.com/api/v9/channels/{tracking_channelID}/messages',data=payload, headers=headers)   
        else:
            payload = {
                 'content': "```Order Number: {} \nEMAIL: {} \nSIZE: {} \nADDRESS: {} \nSTATUS: {}\n```".format(on, mail, sizes[i], addy, status)
            }

            r = requests.post(f'https://discord.com/api/v9/channels/{tracking_channelID}/messages',data=payload, headers=headers)
        i=i+1
   
checkstat(products,name)



