import requests
import json
import base64

#uses HTML post/get requests to grab messages with media files
#deletes media first, and then deletes the message
#Use-Case HIPAA compliance(?)

#sets up credentials
accountsid = ""
token = ""
space = ""

#converts credentials to base64
accountsidbyte = accountsid.encode('utf-8')
tokenbyte = token.encode('utf-8')
helper = ":"
helperbyte = helper.encode('utf-8')
authcode = accountsidbyte+helperbyte+tokenbyte
authcode = base64.b64encode(authcode)

#setting url for first request, and headers used through all requests
#this may be the best place to drill down with To/From/DateSent info
#as message sid(s) marked here will be the only ones passed to future functions

url = space+"/api/laml/2010-04-01/Accounts/"+accountsid+"/Messages"

headers = {
    "Accept": "application/json",
    "Authorization": "Basic "+str(authcode.decode())
}

#Grabs all messages
response = requests.request("GET", url, headers=headers)

#moving response.text into a variable, loading data into json
responsestr = response.text
jsdata = json.loads(responsestr)

#setting up lists
msidlist = []
msglist = []
mdalist = []

#getting the sid of all messages pulled from json data and appending it to a list
for message in jsdata['messages']:
    msidlist.append(message['sid'])

#taking each sid from the msid list and creating a request for the corresponding media data
for sid in msidlist:
    furl = space+"/api/laml/2010-04-01/Accounts/"+accountsid+"/Messages/"+sid+"/Media"
    response = requests.request("GET", furl, headers=headers)

    #parsing media data to a list
    medlist = response.text
    jsmed = json.loads(medlist)
    mdalist.append(jsmed['media_list'])

#media_list is only present in messages with media files, so this will ONLY send requests to messages with media files.
for mda in mdalist:
    try:
        msgholster = mda[0]['parent_sid']
        mdaholster = mda[0]['sid']

        #comment this response out to only delete media
        msgurl = space+"/api/laml/2010-04-01/Accounts/"+accountsid+"/Messages/"+msgholster

        #sends the delete request to each medial url grabbed
        mdaurl = space+"/api/laml/2010-04-01/Accounts/"+accountsid+"/Messages/"+msgholster+"/Media/"+mdaholster
        response = requests.request("DELETE", mdaurl, headers=headers)
        print(response)

        #comment this response out to only delete media
        response = requests.request("DELETE", msgurl, headers=headers)

        print(msgholster)
        print(response)
    #When we find the last message with media it will give an IndexError "list index out of range"
    except IndexError:
        pass