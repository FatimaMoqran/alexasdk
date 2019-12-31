#creating a skill builder object
from ask_sdk_core.skill_builder import SkillBuilder

sb = SkillBuilder()

from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard

#decorator retun True if the incoming request is a Launch request.

@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    #type: (HandlerInput) -> Response
    speech_text = "Welcome to the Alexa Skills, you can say hello!"

    handler_input.response_builder.speak(speech_text).set_card(SimpleCard("Hello World", speech_text)).set_should_end_session(False)
    return handler_input.response_builder.response

@sb.request_handler(can_handle_func=is_intent_name("HelloWorldIntent"))
def hello_world_intent_handler(handler_input):
    #type: (HandlerInput) -> Response
    speech_text = "Hello World!"

    handler_input.response_builder.speak(speech_text).set_card(SimpleCard("Hello World", speech_text)).set_should_end_session(True)
    return handler_input.response_builder.response

#help intent handler
@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    #type: (HandlerInput) -> Response
    speech_text = "you can say hello to me!"

    handler_input.response_builder.speak(speech_text).ask(speech_text).set_card(SimpleCard("Hello world", speech_text))
    return handler_input.response_builder.response

#CancelandStop Intent handler
@sb.request_handler(
    can_handle_func= lambda handler_input:
    is_intent_name("AMAZON.CancelIntent")(handler_input) or
    is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input):
    #type: (HandlerInput) -> Response
    speech_text = "Goodbye!"

    handler_input.response_builder.speak(speech_text).set_card(SimpleCard("Hello World", speech_text)).set_should_end_session(True)
    return handler_input.response_builder.response

@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    #type : (HandlerInput) -> Response
    #any cleanup logic goes here

    return handler_input.response_builder.response




