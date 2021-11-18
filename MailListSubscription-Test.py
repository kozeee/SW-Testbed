import os
from pyngrok import ngrok
from flask import Flask, request
from signalwire.messaging_response import MessagingResponse
from signalwire.rest import Client as signalwire_client
import csv

#modified from https://developer.signalwire.com/apis/docs/creating-a-publically-exposed-webhook-and-configure-it-to-your-incoming-number

#this script listens for incoming messages and adds/deletes them from a csv in real time
#could be used for managing mailing list subscription

# Input User Authentication into Client
ProjectID = "Your Project ID"
AuthToken = "Your Account Token"
SpaceURL = 'https://YourSpace.signalwire.com'
sw_phone_number = 'SignalWire Number to Recieve SMS'
client = signalwire_client(ProjectID, AuthToken, signalwire_space_url=SpaceURL)

# Initialize the Flask object
app = Flask(__name__)

# Define what we would like our application to do
@app.route("/sms_app", methods=['GET', 'POST'])
def sms_app():

    # Find the body of the incoming message and the phone number it was sent from
    body = request.values.get('Body', None)
    fname = request.values.get('From', None)

    #our list of dictionaries used to hold data in memory
    friendlist = []

    #opens our testing file and begins populating friendlist (currently requires one populated entry, {'phone number': init} by default
    with open('testing.csv', 'r') as readFile:
        reader = csv.DictReader(readFile)
        for line in reader:
            friendlist.append({'phone number': line['phone number']})

    # Start our message response
    resp = MessagingResponse()

    # Tests the body for a specific string. Currently set to the "Trial Account" message

    #if a 1-character message is sent:
    if body == "You've received a 1-character message. Upgrade your Trial account to view this message.":
        # message response commented out for testing
        # resp.message("Great! Added your number to my list of friends!")

        #check if the incoming number is already in the dictionary
        if fname not in line['phone number']:
            #adds phone number to dictionary with the key 'phone number'
            friendlist.append({'phone number': fname})
        #print(friendlist)

    # if a 2-character message is sent:
    elif body == "You've received a 2-character message. Upgrade your Trial account to view this message.":
        # message response commented out for testing
        #resp.message("No problem, I'll make new friends.")

        #loop through each dictionary in the friendlist
        for objects in friendlist:

            #search each 'phone number' value and remove it if found
            if fname in objects['phone number']:
                friendlist.remove(objects)
        #print(friendlist)

    #determines what to do in-case of unexpected message bodies
    #commented out since it only returns a response
    #else:
        # message response commented out for testing
    #resp.message(
        #f'Would you like to be friends?(y/n)')
    #print(friendlist)

    #setup for writing to our new csv, changing the name will create a new csv in your current directory
    with open('testing.csv', 'w', newline='') as writeFile:

        #if your dictionary has more keys they would be listed here
        fieldname = ['phone number']

        writer = csv.DictWriter(writeFile, fieldnames=fieldname)
        writer.writeheader()

        #for each entry in friendlist, write a new row to the csv
        for lines in friendlist:
            writer.writerow(lines)
    return str(resp)


# Set the ngrok URL as the webhook for our SW phone

def start_ngrok():

    # Set up a tunnel on port 5000 for our Flask object to interact locally
    url = ngrok.connect(5000).public_url
    print(' * Tunnel URL:', url)

    # Now that we have our URL, Use the SignalWire's Update an Incoming Phone Number API
    client.incoming_phone_numbers.list(
        phone_number=sw_phone_number)[0].update(
        sms_url=url + '/sms_app')  # Notice we update the parameter sms_url


# In the previous step, we declared where the tunnel will be opened, however we must start ngrok before a tunnel will be available to open
# This checks your os to see if ngrok is already running and if it is not, ngrok will start
if __name__ == '__main__':
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        start_ngrok()
    app.run(debug=True)
