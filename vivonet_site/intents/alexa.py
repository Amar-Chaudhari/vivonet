from django_alexa.api import fields, intent, ResponseBuilder
from django.views.decorators.csrf import csrf_exempt
import logging


logger = logging.getLogger("django_alexa.views")

@intent(app='intents')
def LaunchRequest(session):
    """
    Hogwarts is a go
    ---
    launch
    start
    run
    begin
    open
    """
    return ResponseBuilder.create_response(message="Welcome to ViVonet skill. Using our skill you can simplify network management.",
                                           end_session=True)

@intent(app='intents')
def CreateNetwork(session,from_city,to_city):
    speech_text = '<speak>Vivonet will setup a 100 milli second path from {0} to {1}</speak>'.format(from_city,to_city)
    reprompt_text = '<speak>What path do you want to setupt? You can say from Denver to SF</speak>'
    print from_city, to_city
    return ResponseBuilder.create_response(message=speech_text,message_is_ssml=True)
