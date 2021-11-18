import requests
import json
import base64

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

#headers for all requests
headers = {
    "Accept": "application/json",
    "Authorization": "Basic "+str(authcode.decode())
}

#url to GET list of messages
url = space+"/api/laml/2010-04-01/Accounts/"+accountsid+"/Messages"

#initialize some variables
msidlist = []
resloop = 1

#our application loop
while resloop == 1:

    #create GET response for list of messages
    response = requests.request("GET", url, headers=headers)

    #converts the response.text to a string
    responsestr = response.text

    #converts the string to a dictionary via json
    jsdata = json.loads(responsestr)

    #searches each message in the jsdata dictionary for the sid item
    for message in jsdata['messages']:

        #appends each sid to a separate list
        msidlist.append(message['sid'])

    #loops through the list of sid(s) and posts DELETE requests to the appropriate url
    for sid in msidlist:
        furl = space + "/api/laml/2010-04-01/Accounts/" + accountsid + "/Messages/" + sid
        response = requests.request("DELETE", furl, headers=headers)
        print(response)
    #checks response for 204 (no content), if not breaks our program loop
    if response != "<Response [204]>":
        resloop = 0
        print(response)
        print("all done")

