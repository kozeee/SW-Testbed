import pandas as pd
import time
import requests

#this script grabs Phone numbers, Names, and Messages from an Excel file
#uses this data to format and send HTML requests

#Your project ID
projectID = ""

#Your Space Name (not full url)
spaceName = ""

#Your SignalWire phone number used to send messages
#country code, no +, hypen, or ()
SWnumber = ""

# using pandas to read an excel file and create a dictionary
#change 'example.xlsx' to your desired path/file name
df = pd.read_excel('example.xlsx')
xldict = df.to_dict(orient='list')

#lists for seperating data
mlist = []
plist = []
#ilist = []
clist = []

#importing data from dictionary to their lists
def dataimport():
    for values in xldict['Phone Number']:
        plist.append(values)

    for message in xldict['Message']:
        mlist.append(message)

    #iteration is a debugging list
    #for iterations in xldict['Iteration']:
        #ilist.append(iterations)

    for names in xldict['Client Name']:
        clist.append(names)


def signalwire():
    #imports data from function above
    dataimport()

    #this formats our payload for each html request
    for number, message, name in zip(plist, mlist, clist):
        plprep = ("To=%2b" + str(number) + "&From=%2B"+SWnumber+"&Body=" + "Hello " + str(name) + ", " + str(
            message))

        #creates url with proper spacename and project ID
        url = "https://"+spaceName+".signalwire.com/api/laml/2010-04-01/Accounts/"+projectID+"/Messages"
        payload = plprep
        headers = {
            "Accept": "application/json",
         "Content-Type": "application/x-www-form-urlencoded",
            # <Your Auth Code> is a 64 bit encoded version of projectID+":"+accountToken
            #You can generate this using Auth_Helper.py in my repository!
            "Authorization": "Basic <Your Auth Code>"
        }

        #Sends each request with a sleep of 5 seconds (Change "GET" to "POST")
        response = requests.request("GET", url, data=payload, headers=headers)
        time.sleep(5)

        print(response.text)


signalwire()
