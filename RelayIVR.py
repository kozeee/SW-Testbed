from signalwire.relay.consumer import Consumer
from signalwire.rest import Client as signalwire_client
import os
import pyjokes


class CustomConsumer(Consumer):
    def setup(self):
        #holds our environment variables
        self.project = os.environ['ProjectID']
        self.token = os.environ['AuthToken']
        self.url = os.environ['SpaceUrl']

        # make sure your signalwire number is pointed to this context
        self.contexts = ['office']

        # this list holds all of our no-fun numbers
        self.lists=[]

        # this dictionary is for our 'managers' to forward no-fun customers to.
        self.callthrough=[{'to_number':'+18045472366', 'timeout': 10}]

    # function listens for incoming calls
    async def on_incoming_call(self, call):
        result = await call.answer()
        if result.successful:
            print("Checking no fun database.. ")
            # checks if our caller is on the no-fun list
            if call.from_number in self.lists:
                print("Detected..")
                # prompts with text-to-speech
                result = await call.prompt_tts(prompt_type="digits",
                                               text = "Hey.. I know you, You're one of those no fun types. Press 1 if you've changed your ways. Or press 2 to speak with a manager.",
                                               digits_max=1)
                # if our caller is nice they get taken off the list.
                if result.successful and result.result=="1":
                    await call.play_tts(text="Okay fine, I'll give you another chance.")
                    for object in self.lists:
                        if call.from_number == object:
                            self.lists.remove(object)
                # if our caller is rude they get sent to our "manager"
                if result.successful and result.result=="2":
                    # tries numbers in our "callthrough" dictionary until one answers
                    result = await call.connect (device_list=self.callthrough)
                    # if any answers the consumer waits for the call to end and then hangs up
                    if result.successful:
                        print("calling successful")
                        patchthrough = result.call
                        await patchthrough.wait_for_ended()
                        print("goodbye")
                        await call.hangup()
                    # if nobody answers, we also hang up.
                    else:
                        print("Call Failed")
                        await call.hangup()
                # if our no-fun caller can't press buttons correctly we also hang up on them
                else:
                    await call.play_tts(text="What a shame. I have nothing more to say to you. Goodbye.")
                    await call.hangup()
            # if our caller is not on the list of no-fun callers we ask if they want to hear a joke.
            if call.from_number not in self.lists:
                result = await call.prompt_tts(prompt_type="digits",
                                               text="Press 1 to hear a funny joke, Press 2 to have a joke texted to you, Press 3 if you're no fun.",
                                               digits_max=1)
                # if our caller wants to hear a joke, we get one using pyjokes and play it over text-to-speech, then hang up.
                if result.successful and result.result == "1":
                    joke = pyjokes.get_joke()
                    await call.play_tts(text=joke)
                    await call.hangup()

                # if our caller wants to have the joke texted to them, we use the rest api to send a the joke via sms and hangs up
                if result.successful and result.result == "2":
                    joke = pyjokes.get_joke()
                    client = signalwire_client(self.project, self.token, signalwire_space_url=self.url)
                    client.messages.create(to=call.from_number, from_=call.to_number, body=joke)
                    await call.play_tts(text='Your joke is on the way. Goodbye.')
                    await call.hangup()

                # if our caller is no fun they get put on the no-fun list and we hang up on them.
                if result.successful and result.result == "3":
                    await call.play_tts(text="Not cool pal. You're going on the no fun list")
                    # technically this if statement shouldn't be needed, but maybe it will catch some sneaky callers that break our "advanced security"
                    if call.from_number not in self.lists:
                        self.lists.append(call.from_number)
                    print(self.lists)
                    await call.hangup()
                # if our caller can't press a useful button we hang up on them
                else:
                    await call.play_tts(text="Sorry. I'm still a new AI, and didn't understand your request. Call back and try again.")
                    await call.hangup()

# Runs the consumer
consumer = CustomConsumer()
consumer.run()
