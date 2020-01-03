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
    """Check if a favorite color has already been recorded in session attributes. 
    If yes, provide the color to the user. If not, ask for favorite color."""
    #type : (HandlerInput) -> Response
    if color_slot_key in handler_input.attributes_manager.session_attributes:
        fav_color = handler_input.attributes_manager.session_attributes[color_slot_key]
        speech = "votre couleur préférée est le {}. Au revoir!".format(fav_color)
        handler_input.response_builder.set_should_end_session(True)
    else:
        speech = "je ne connais pas votre couleur préférée" + help_text
        handler_input.response_builder.ask(help_text)

    handler_input.response_builder.speak(speech)
    return handler_input.response_builder.response

@sb.request_handler(can_handle_func=is_intent_name("MyColorIsIntent"))
    def my_color_handler(handler_input):
         """Check if color is provided in slot values. If provided, then set
         your favorite color fromp slot value into session attributes.
         If not, then it asks user to provide the color"""

        #type : (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots

        if color_slot in slots:
            fav_color = slots[color_slot].value
            handler_input.attribues_manager.session_attributes[color_slot_key] = fav_color
            speech = ("Maintenant je sais que votre couleur préférée est le {}"
            "vous pouvez me demander quelle est votre couleur préférée en disant "
            "quelle est ma couleur préférée".format(fav_color))
            reprompt = ("vous pouvez me demander quelle est votre couleur préférée en disant "
            "quelle est ma couleur préférée")
        else:
            speech = "Je ne suis pas sure quelle est votre couleur préférée, essayez encore"
            #reprompt after 8 seconds if the user doesn't respond
            reprompt = ("Je ne suis pas sure quelle est votre couleur préférée, essayez encore"
                        "vous pouvez me dire quelle est votre couleur préférée en disant "
                        "ma couleur préférée est rouge")

        handler_input.response_builder.speak(speech).ask(reprompt)
        return handler_input.response_builder.response

#an handler that helps you handle unexpected utterances or when a customer says something that doesn't map to any intent 
@sb.request_handler(can_handle_func = is_intent_name("AMAZON.FallbackIntent"))
def fallback_handler(handler_input):
    """AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    #type: (HandlerInput) -> Response
    speech = (
        "le {} ne peut pas vous aider avec ça"
        "vous pouvez me dire quelle est votre couleur préférée en disant "
        "ma couleur préférée est rouge".format(skill_name)
    reprompt = ("vous pouvez me dire quelle est votre couleur préférée en disant"
                        "ma couleur préférée est rouge")

def convert_speech_to_text(ssml_speech):
    #type : (str) -> str
    s = SSMLStripper()
    s.feed(ssml_speech)
    return s.get_data()


@sb.global_response_interceptor()
def add_card(handler_input, response):
    """Add a card by translating ssml text to card content"""
    #type: (HandlerInput, response)-> None
    response.card = SimpleCard(
        tittle=skill_name,
        content= convert_speech_to_text(response.output_speech.ssml))

@sb.global_response_interceptor()




