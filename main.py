# @author Hinux

from os import times, write
import re
import requests
from bs4 import BeautifulSoup
import json
import datetime
import time,random
from email.mime.text import MIMEText
import smtplib

def sendEmail(toAddress:str,content:str,ifSendFlag:bool):

    if not ifSendFlag:
        return

    with open('./authcode.txt','r+') as f:
        authInfo=json.load(f)                    #Authentication Info
    
    for fromAddress in authInfo:
        passwd = authInfo[fromAddress]          #The authentication code and the Email Address of the sender

    subject="Hinux's JNU Utility Reminder"                         #Subject          　　                                          
    msg = MIMEText(content)                                        #Use the MIMEText to convert the content into correct form
    msg['Subject'] = subject
    msg['From'] = fromAddress
    msg['To'] = toAddress
    s = smtplib.SMTP_SSL("smtp.qq.com",465)
    s.login(fromAddress, passwd)
    s.sendmail(fromAddress, toAddress, msg.as_string())
    #log("Mail has been sent",False)
    s.quit()

def getTbMeter(ssn:requests.Session,dorm:str):

    loginUrl="http://202.116.25.12/login.aspx"

    loginPage=requests.get(loginUrl).content.decode('utf-8')
    bs4LoginPage=BeautifulSoup(loginPage,"lxml")
    __VIEWSTATE=bs4LoginPage.find(attrs={"name":"__VIEWSTATE"})['value']
    __VIEWSTATEGENERATOR=bs4LoginPage.find(attrs={"name":"__VIEWSTATEGENERATOR"})['value']

    loginFormData={
        "__LASTFOCUS": "",
        "__VIEWSTATE": __VIEWSTATE,
        "__VIEWSTATEGENERATOR": __VIEWSTATEGENERATOR,
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "hidtime": "",       #"2021-05-31+15:47:01"
        "txtname": dorm,
        "txtpwd": "",
        "ctl01": ""
    }
    
    ssn=requests.Session()
    ssn.post(url=loginUrl,data=loginFormData)
    defaultPage=ssn.get(url="http://202.116.25.12/default.aspx").content.decode('utf-8')
    tbMeter=re.findall(">0000[0-9]*<",defaultPage)
    return tbMeter[0][1:-1]

#Query related info
def query(
    ssn:requests.Session,   #An existing session.
    itemIndex:int,          #The remaining value queryed. 0:当前剩余数量(Currently remaining power) 1:当前剩余金额(Currently remaining amount)
    tbMeter:str,            #The number of your electricity meter.
    dorm:str                #The number of your dorm.
):
    queryUrl="http://202.116.25.12/default.aspx"
    items=["当前剩余数量","当前剩余金额"]
    now=datetime.datetime.now().strftime("%Y-%m-%d")
    splitNow=now.rsplit("-")
    old=f"{splitNow[0]}-{str(int(splitNow[1])-1).zfill(2)}-{str(int(splitNow[1])-1).zfill(2)}"

    formData={
        "__EVENTTARGET": "RegionPanel1$Region2$GroupPanel1$ContentPanel1$DDL_监控项目",
        "__EVENTARGUMENT": "",
        "__LASTFOCUS": "",
        "__VIEWSTATE": "/wEPDwUKMTEzMzUzMDQ1OQ9kFgICAw9kFgICCQ9kFgICAQ9kFgJmD2QWAmYPZBYCAiwPEGQQFQMP5b2T5YmN6KGo6K+75pWwEuW9k+WJjeWJqeS9memHkeminRLlvZPliY3liankvZnmlbDph48VAw/lvZPliY3ooajor7vmlbAS5b2T5YmN5Ymp5L2Z6YeR6aKdEuW9k+WJjeWJqeS9meaVsOmHjxQrAwNnZ2cWAWZkGAQFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYaBRRSZWdpb25QYW5lbDEkUmVnaW9uMwUiUmVnaW9uUGFuZWwxJFJlZ2lvbjMkQ29udGVudFBhbmVsMwUtUmVnaW9uUGFuZWwxJFJlZ2lvbjMkQ29udGVudFBhbmVsMyR0eHRzdGFyT2xkBSpSZWdpb25QYW5lbDEkUmVnaW9uMyRDb250ZW50UGFuZWwzJHR4dHN0YXIFKlJlZ2lvblBhbmVsMSRSZWdpb24zJENvbnRlbnRQYW5lbDMkRERMU09SVAUsUmVnaW9uUGFuZWwxJFJlZ2lvbjMkQ29udGVudFBhbmVsMyRidG5TZWFyY2gFKlJlZ2lvblBhbmVsMSRSZWdpb24zJENvbnRlbnRQYW5lbDMkQnV0dG9uMwUqUmVnaW9uUGFuZWwxJFJlZ2lvbjMkQ29udGVudFBhbmVsMyRidG5FeGl0BSpSZWdpb25QYW5lbDEkUmVnaW9uMyRDb250ZW50UGFuZWwzJHRiTWV0ZXIFKVJlZ2lvblBhbmVsMSRSZWdpb24zJENvbnRlbnRQYW5lbDMkdGJSb29tBRRSZWdpb25QYW5lbDEkUmVnaW9uMgUgUmVnaW9uUGFuZWwxJFJlZ2lvbjIkR3JvdXBQYW5lbDEFLlJlZ2lvblBhbmVsMSRSZWdpb24yJEdyb3VwUGFuZWwxJENvbnRlbnRQYW5lbDEFLlJlZ2lvblBhbmVsMSRSZWdpb24yJEdyb3VwUGFuZWwxJENvbnRlbnRQYW5lbDIFLlJlZ2lvblBhbmVsMSRSZWdpb24yJEdyb3VwUGFuZWwxJENvbnRlbnRQYW5lbDQFFFJlZ2lvblBhbmVsMSRSZWdpb24xBSBSZWdpb25QYW5lbDEkUmVnaW9uMSRHcm91cFBhbmVsMgUqUmVnaW9uUGFuZWwxJFJlZ2lvbjEkR3JvdXBQYW5lbDIkVGFiU3RyaXAzBTBSZWdpb25QYW5lbDEkUmVnaW9uMSRHcm91cFBhbmVsMiRUYWJTdHJpcDMkVGFiMTMFNlJlZ2lvblBhbmVsMSRSZWdpb24xJEdyb3VwUGFuZWwyJFRhYlN0cmlwMyRUYWIxMyRHcmlkMwUwUmVnaW9uUGFuZWwxJFJlZ2lvbjEkR3JvdXBQYW5lbDIkVGFiU3RyaXAzJFRhYjE0BTZSZWdpb25QYW5lbDEkUmVnaW9uMSRHcm91cFBhbmVsMiRUYWJTdHJpcDMkVGFiMTQkR3JpZDIFMFJlZ2lvblBhbmVsMSRSZWdpb24xJEdyb3VwUGFuZWwyJFRhYlN0cmlwMyRUYWIxNQU2UmVnaW9uUGFuZWwxJFJlZ2lvbjEkR3JvdXBQYW5lbDIkVGFiU3RyaXAzJFRhYjE1JEdyaWQxBQd0eHRTb3J0BQd0eHRSS0VZBTZSZWdpb25QYW5lbDEkUmVnaW9uMSRHcm91cFBhbmVsMiRUYWJTdHJpcDMkVGFiMTUkR3JpZDEPD2RlZAU2UmVnaW9uUGFuZWwxJFJlZ2lvbjEkR3JvdXBQYW5lbDIkVGFiU3RyaXAzJFRhYjE0JEdyaWQyDw9kZWQFNlJlZ2lvblBhbmVsMSRSZWdpb24xJEdyb3VwUGFuZWwyJFRhYlN0cmlwMyRUYWIxMyRHcmlkMw8PZGVkCzzc9Vc4t4ceeZUdzrmGxbi9DwE=",
        "__VIEWSTATEGENERATOR": "CA0B0334",
        "RegionPanel1$Region3$ContentPanel3$txtstarOld": old,
        "RegionPanel1$Region3$ContentPanel3$txtstar": now,
        "RegionPanel1$Region3$ContentPanel3$DDLSORT$Value": "电",
        "RegionPanel1$Region3$ContentPanel3$DDLSORT": "电",
        "RegionPanel1$Region3$ContentPanel3$tbMeter": tbMeter,
        "RegionPanel1$Region3$ContentPanel3$tbRoom": dorm,
        "RegionPanel1$Region2$GroupPanel1$ContentPanel1$DDL_监控项目": items[itemIndex],
        "inputItem": [
            "1",
            "1",
            "1"
        ],
        "txtHeight": "337",
        "tbNewDayMeter": "0",
        "tqid": "",
        "tqsort": "",
        "PandValue": "10",
        "txtSort": "电表",
        "txtRKEY": "",
        "F_CHANGED": "false",
        "RegionPanel1_Region3_ContentPanel3_Collapsed": "false",
        "RegionPanel1_Region3_Collapsed": "false",
        "RegionPanel1_Region2_GroupPanel1_ContentPanel1_Collapsed": "false",
        "RegionPanel1_Region2_GroupPanel1_ContentPanel2_Collapsed": "false",
        "RegionPanel1_Region2_GroupPanel1_ContentPanel4_Collapsed": "false",
        "RegionPanel1_Region2_GroupPanel1_Collapsed": "false",
        "RegionPanel1_Region2_Collapsed": "false",
        "RegionPanel1_Region1_GroupPanel2_TabStrip3_Tab13_Grid3_Collapsed": "false",
        "RegionPanel1_Region1_GroupPanel2_TabStrip3_Tab13_Grid3_PageIndex": "0",
        "RegionPanel1_Region1_GroupPanel2_TabStrip3_Tab13_Collapsed": "false",
        "RegionPanel1_Region1_GroupPanel2_TabStrip3_Tab13_Hidden": "false",
        "RegionPanel1_Region1_GroupPanel2_TabStrip3_Tab14_Grid2_Collapsed": "false",
        "RegionPanel1_Region1_GroupPanel2_TabStrip3_Tab14_Grid2_PageIndex": "0",
        "RegionPanel1_Region1_GroupPanel2_TabStrip3_Tab14_Collapsed": "false",
        "RegionPanel1_Region1_GroupPanel2_TabStrip3_Tab14_Hidden": "false",
        "RegionPanel1_Region1_GroupPanel2_TabStrip3_Tab15_Grid1_Collapsed": "false",
        "RegionPanel1_Region1_GroupPanel2_TabStrip3_Tab15_Grid1_PageIndex": "0",
        "RegionPanel1_Region1_GroupPanel2_TabStrip3_Tab15_Collapsed": "false",
        "RegionPanel1_Region1_GroupPanel2_TabStrip3_Tab15_Hidden": "false",
        "RegionPanel1_Region1_GroupPanel2_TabStrip3_Collapsed": "false",
        "RegionPanel1_Region1_GroupPanel2_TabStrip3_ActiveTabIndex": "0",
        "RegionPanel1_Region1_GroupPanel2_Collapsed": "false",
        "RegionPanel1_Region1_Collapsed": "false",
        "RegionPanel1_Collapsed": "false",
        "F_STATE": "",
        "F_AJAX": "true"
    }
    
    resultPage = ssn.post(queryUrl,formData).content.decode('utf-8')
    res=re.findall(r"\"[0-9\.]*\"",resultPage)[2]
    return float(str(res).replace("\"",""))

def mainFunction(ifLog:bool,ifSendEmail:bool):
    ssn=requests.Session()
    #dorm=input("Please input your dorm:")
    #itemIndex=int(input("Please input the Index (0:Remaining volt 1:Remaining amount): "))

    with open("./dorms.txt","r") as f:
        dorms=json.load(f)
    
    for dorm in dorms:
        dorm=dorm.replace('\n','').replace(' ','')
        mailAddress=dorms[dorm]
        itemIndex=1                         #当前剩余金额
        tbMeter=getTbMeter(ssn,dorm)
        res:float=query(ssn,itemIndex,tbMeter,dorm)
        print(f"**********\nDorm: {dorm}\nResult: {res}\nEmail: {dorms[dorm]}")

        now:str=datetime.datetime.now().strftime("%H:%M:%S")
        
        if ifLog:
            with open("./record.txt","a+") as f:
                f.write(f"{now} ¥{res}\n")

        if(res<=10):
            print("Low Power!")
            sendEmail(mailAddress,f"Insufficient amount (¥{res} remaining)!\n Recharge in order to avoid outage",ifSendEmail)


if __name__=="__main__":
    
    ifSendEmail=True
    oldHour=datetime.datetime.now().hour

    while True:
        newHour=datetime.datetime.now().hour
        if newHour > oldHour:
            ifSendEmail=True
            oldHour=newHour

        mainFunction(False,ifSendEmail)         #Tell the program do not record and send an email per hour.
        ifSendEmail=False
        random.seed(datetime.datetime.now())
        s:float=round(random.random()*1000,2)
        print(f"Next scan would arrive after {s}s")
        time.sleep(s)                           #Sleep in order to simulate a real querying user