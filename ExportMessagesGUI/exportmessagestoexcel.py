# importing needed modules
# pytz is recommended for handling timezones.
# signalwire datetime data is typically handled in UTC

from datetime import datetime
from signalwire.rest import Client as signalwire_client
import pandas as pd
import pytz

# setting authentication variables
accountsid = "your project id"
token = "your token"
space = "https://<your space url>.signalwire.com"
client = signalwire_client(accountsid, token, signalwire_space_url=space)

def getnums():
    numlist = []
    numuniq = []
    msglist = client.messages.list()
    for record in msglist:
        numlist.append((record.from_))
    for uniq in numlist:
        if uniq not in numuniq:
            numuniq.append(uniq)
    return numuniq


def exportmessagestoxl(csvorxlsx, filename, phonenum):
    # setting up additional variables
    cleanedmessages = []
    messageloop = 1

    # gets our list of calls with desired specifications
    # more info in CallList.List api
    messages = client.messages.list(from_=phonenum, date_sent_after=datetime(2021, 11, 9, 3, 0, 0, 0, tzinfo=pytz.UTC))

    # grabbing the desired data from each call and storing it in a list
    # more info in the CallInstance api
    for record in messages:
        cleanedmessages.append((record.from_, record.to, record.date_sent, record.status, record.sid))

    # creates a dataframe of our data appropriate for csv or xlsx formats
    messagesdataframe = pd.DataFrame(cleanedmessages, columns=('From', 'To', 'Date_Sent', 'Status', 'Sid'))

    # exports data to a csv or xlsx in the desired path. this path by default is in the same folder as your python script
    while messageloop == 1:
        if csvorxlsx == "csv":
            # add "\desired path\"+ to alter the path of saved file
            messagesdataframe.to_csv(filename+".csv", index=False, encoding='utf-8')
            messageloop = 0
            print("file saved as", filename+".csv")
        elif csvorxlsx == "xlsx":
            messagesdataframe['Date_Sent'] = messagesdataframe['Date_Sent'].dt.tz_localize(None)
            messagesdataframe.to_excel(filename+".xlsx", index=0)
            messageloop = 0
            print("file saved as", filename + ".xlsx")
        else:
            break
