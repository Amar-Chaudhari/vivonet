from django_alexa.api import fields, intent, ResponseBuilder
from django.views.decorators.csrf import csrf_exempt
import logging


logger = logging.getLogger("django_alexa.views")

@intent(app='intents')
def LaunchRequest(session):

    return ResponseBuilder.create_response(message="Welcome to ViVonet skill. Using our skill you can simplify network management.",
                                           end_session=True)

@intent(app='intents')
def CreateIntent(session,intent_type,from_city,to_city):
    print(session)
    if to_city:
        speech_text = 'Vivonet will setup a {0} path from {1} to {2}'.format(intent_type,from_city,to_city)
    else:
        speech_text = "Vivonet needs the destination location to setup the path"
        reprompt_text = 'What path do you want to setup? You can say from Denver to SF'
        return ResponseBuilder.create_response(speech_text=speech_text,message_is_ssml=True,end_session=True,reprompt_text=reprompt_text)
    return ResponseBuilder.create_response(message=speech_text,message_is_ssml=True,end_session=True)
