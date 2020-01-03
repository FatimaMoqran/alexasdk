import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard

skill_name = "My Color Session"
help_text = ('Quelle est votre couleur préférée? Vous pouvez dire ma couleur préférée est le rouge')

color_slot_key = "color"
color_slot = "color"

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#handler when the skill is invoke

@sb.request_handler(can_handle_func= is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    """Handler for Skill Launch"""
    #type: (HandlerInput) -> Response
    speech = "Bienvenue chez color picker "

    handler_input.response_builder.speak(speech+ " "+ help_text).ask(help_text)
    return handler_input.response_builder.response

@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    """Handler for help Intent"""
    #type (HandlerInput) -> Response
    handler_input.response_builder.speak(help_text).ask(help_text)
    return handler_input.response_builder.response

@sb.request_handler(
    can_handle_func=lambda handler_input:
        is_intent_name("AMAZON.CancelIntent")(handler_input) or
        is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input):
    ""Single handler for Cancel and Stop Intent.""
    #type: (HandlerInput)-> Response
    speech_text = "Goodbye!"

    return handler_input.response_builder.speak(speech_text).response

@sb.request_handler(can_handle_func= is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    """Handler for Session end"""
    #type : (HandlerInput) -> Response
    return handler_input.response_builder.response

@sb.request_handler(can_handle_func= is_intent_name("WhatsMyColorIntent"))
def session_ended_request_handler(handler_input):
    """Check if a favorite color has already been recorded in session attributes. If yes, provide the color to the user. If not, ask for favorite color."""
    #type : (HandlerInput) -> Response
    if color_slot_key in handler_input.attributes_manager.session_attributes:
        fav_color = handler_input.attributes_manager.session_attributes[color_slot_key]
        speech = "votre couleur préférée est le {}. Au revoir!".format(fav_color)
        handler_input.response_builder.set_should_end_session(True)
    else:
        speech = "je ne connais pas votre couleur préférée" + help_text
        




