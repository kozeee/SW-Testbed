# imports Consumer from the relay
from signalwire.relay.consumer import Consumer
# imports Client from the rest api to handle outbound sms
from signalwire.rest import Client as signalwire_client
# os is used to manage environment variables
import os
# pyjokes handles our jokes
import pyjokes

class CustomConsumer(Consumer):
    def setup(self):
        # holds our environment variables
        self.project = os.environ['ProjectID']
        self.token = os.environ['AuthToken']
        self.url = os.environ['SpaceUrl']

        # make sure your signalwire number is pointed to this context
        self.contexts = ['office']

        # this list holds all of our no-fun numbers
        self.lists=['']

        # this dictionary is for our 'managers' to forward no-fun customers to.
        self.callthrough=[{'to_number':'+18045472366', 'timeout': 10}]

        # catches bad inputs
        self.mapper="0"

        # decides if we return to the main menu or ends the call
        self.menuloop = "0"

    # function listens for incoming calls
    async def on_incoming_call(self, call):
        result = await call.answer()
        # checks if call connected
        if result.successful:
            # resets map and menu loop with each call
            self.mapper="0"
            self.menuloop= "0"
          # starts our IVR only if the call is successful
            while self.menuloop == "0":
                # resets our bad input catcher at beginning of the loop
                self.mapper="0"

                # checks if our caller is on the no-fun list
                if call.from_number in self.lists:
                    # debugging print("Detected..")

                    # prompts with text-to-speech
                    result = await call.prompt_tts(prompt_type="digits",
                                                   text = "Hey.. I know you, You're one of those no fun types. Press 1 if you've changed your ways. Or press 2 to speak with a manager.",
                                                   digits_max=1)
                    # if our caller is nice they get taken off the list.
                    if result.successful and result.result=="1":
                        self.mapper = "1"
                        await call.play_tts(text="Okay fine, I'll give you another chance.")
                        # sets mapper to one so we can proceed to our joke menu
                        for object in self.lists:
                            if call.from_number == object:
                                self.lists.remove(object)
                    # if our caller is rude they get sent to our "manager"
                    if result.successful and result.result=="2":
                        self.mapper = "1"
                        # tries numbers in our "callthrough" dictionary until one answers
                        result = await call.connect (device_list=self.callthrough)
                        # if any answers the consumer waits for the call to end and then hangs up
                        if result.successful:
                            # debugging print("calling successful")
                            patchthrough = result.call
                            await patchthrough.wait_for_ended()
                            #debugging print("goodbye")
                            self.menuloop = "1"
                            await call.hangup()
                        # if nobody answers, we also hang up.
                        else:
                            #debugging print("Call Failed")
                            self.menuloop = "1"
                            await call.hangup()
                    if self.mapper != "1":
                        await call.play_tts(text="Sorry. I'm still a new AI, and didn't understand your request. Try again.")
                        self.menuloop = "0"

                # if our caller is not on the list of no-fun callers we ask if they want to hear a joke.
                if call.from_number not in self.lists:
                    self.mapper="0"
                    result = await call.prompt_tts(prompt_type="digits",
                                                   text="Press 1 to hear a funny joke, Press 2 to have a joke texted to you, Press 3 if you're no fun.",
                                                   digits_max=1)
                    # if our caller wants to hear a joke, we get one using pyjokes and play it over text-to-speech, then hang up.
                    if result.successful and result.result == "1":
                        joke = pyjokes.get_joke()
                        await call.play_tts(text=joke)
                        await call.play_tts(text='Hope you enjoyed your joke. Taking you back to the main menu.')
                        self.menuloop= "0"
                        self.mapper = "1"

                    # if our caller wants to have the joke texted to them, we use the rest api to send a the joke via sms and hangs up
                    if result.successful and result.result == "2":
                        joke = pyjokes.get_joke()
                        client = signalwire_client(self.project, self.token, signalwire_space_url=self.url)
                        client.messages.create(to=call.from_number, from_=call.to_number, body=joke)
                        await call.play_tts(text='Your joke is on the way. Going back to menu.')
                        self.menuloop= "0"
                        self.mapper = "1"

                    # if our caller is no fun they get put on the no-fun list and we hang up on them.
                    if result.successful and result.result == "3":
                        await call.play_tts(text="Not cool pal. You're going on the no fun list")
                        # technically this if statement shouldn't be needed, but maybe it will catch some sneaky callers that break our "advanced security"
                        if call.from_number not in self.lists:
                            self.lists.append(call.from_number)
                        # debugging print(self.lists)
                        self.menuloop = "1"
                        self.mapper = "1"
                        await call.hangup()

                    if self.mapper != "1":
                        await call.play_tts(text="Sorry. I'm still a new AI, and didn't understand your request. Try again.")
                        self.menuloop = "0"

# Runs the consumer
consumer = CustomConsumer()
consumer.run()
