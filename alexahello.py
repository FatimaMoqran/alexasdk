#creating skillbuilder object helps in adding components responsible for handling input requests and generating custom responses for your skill.
from ask_sdk_core.skill_builder import SkillBuilder
sb = SkillBuilder()
#configure a handler to be invoked when the skill receives a LaunchRequest
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard
from ask_sdk_core.dispatch_components import AbstractExceptionHandler

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self,handler_input):
        #type: (HandlerInput) -> bool
        return is_request_type('LaunchRequest')(handler_input)

    def handle(self,handler_input):
        #type: (HandlerInput) -> Response
        speech_text = "Welcome to the Alexa Skills kit, you can say hello!"

        handler_input.response_buider.speak(speech_text).set_card(SimpleCard('Hello World', speech_text)).set_should_end_session(False)
        return handler_input.response_buider.response

#configure a handler to be invoked whe the skill receives an intent requests with the name HelloWorldIntent

class HelloWorldIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        #type: (HandlerInput) -> bool
        return is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Hello World"

        handler_input.response_builder.speak(speech_text).set_card(SimpleCard("Hello World",speech_text)).set_should_end_session(True)
        return handler_input.response_builder.response

#configure a handler to be invoked when the skill receives the built-in intent
class HelpIntentHandler():
    def can_handle(self,handler_input):
        #type:(HandlerInput) -> bool
        return is_intent_name('AMAZON.HelpIntent')(handler_input)

    def handle(self, handler_input):
        ##type: (HandlerInput) -> Response
        speech_text = "You can say hello to me!"

        handler_input.response_buider.speak(speech_text).ask(speech_text).set_card(SimpleCard('Hello World', speech_text))
        return handler_input.response_buider.response


class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        #type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.CancelIntent")(handler_input) or is_intent_name("AMAZON.StopIntent")(handler_input)

    def handle(self, handler_input):
        #type: (HandlerInput) -> bool
        speech_text = "Goodbye!"

        handler_input.response_builder.speak(speech_text).set_card(SimpleCard("Hello World", speech_text)).set_should_end_session(True)
        return handler_input.response_builder.response

class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        #type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        #type:(HandlerInput) -> Response
        #any cleanup logic goes here

        return handler_input.response_builder.response

class AllExceptionHandler(AbstractExceptionHandler):

    def can_handle(self, handler_input, exception):
        #type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        #type: (HandlerInput, Exception) -> response
        #log the execption in CloudWatch Logs
        print(exception)

        speech = "Sorry I didn't get it. can you please say it again!"
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response

#create a Lambda handler function 
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_exception_handler(AllExceptionHandler())

handler = sb.lambda_handler()

    




