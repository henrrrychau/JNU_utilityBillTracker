# JNU_utilityBillTracker
Getting stuck in the uncertainty of outage? Here is a tracker for your utility bill at the Zhuhai Campus of Jinan University as the solution.  
  
# Prerequisites
The version of Python should be equal to or newer than 3.0 .  
The ```main.py``` should run on the campus network of JNU to make sure that the queried server is accessible.
  
# How to run
Run the command below on your terminal  
```bash
$ Python3.x main.py  
```  
# Configuration files  
The file ```authcode.txt``` stores your sender email address and the corresponding POP3/SMTP service code.  
If you can not contrive to generate the code please refer to [here!](https://support.microsoft.com/en-us/office/add-a-qqmail-account-to-outlook-34ef1254-0d07-405a-856f-0409c7c905eb).  
  
The file ```dorms.txt``` stores the key-value pairs of dorm numbers and their email addresses to which the reminders are sent.  
