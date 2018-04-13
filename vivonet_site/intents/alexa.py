import logging

import duo_client
from django_alexa.api import fields, intent, ResponseBuilder

from intents.intent_engine import *

logger = logging.getLogger("django_alexa.views")

INTENT_TYPES = ("least latency", "high bandwidth", "100ms latency", "least hopcount")


LOGGED_IN_USER = ""
class CreateIntentSlots(fields.AmazonSlots):
    intent_type = fields.AmazonCustom(label="INTENT_TYPES", choices=INTENT_TYPES)
    to_city = fields.AmazonUSCity()
    from_city = fields.AmazonUSCity()
    confirmation = fields.AmazonCustom(label="CONFIRMATION", choices=("yes", "no"))


@intent(app="intents")
def LaunchRequest(session):
    """
    Default launch Intent
    ---
    launch
    start
    """
    logging.info("Launching Intent Invoked")
    kwargs = {}
    kwargs['message'] = "Welcome to ViVoNet."
    kwargs[
        'reprompt'] = "Which intent would you like to setup? You can say least latency, least hopcount or high bandwidth"
    kwargs["end_session"] = False
    kwargs["launched"] = True
    return ResponseBuilder.create_response(**kwargs)


@intent(app="intents")
def HelpIntent(session):
    """
    Default help intent
    ---
    help
    info
    information
    """
    message = "Using our skill you can simplify network management."
    return ResponseBuilder.create_response(message=message)


@intent(app="intents")
def StopIntent(session):
    """
    Default help intent
    ---
    help
    info
    information
    """
    message = "Good Bye!"
    return ResponseBuilder.create_response(message=message)


@intent(app="intents", slots=CreateIntentSlots)
def CreateIntent(session, intent_type, from_city, to_city, confirmation):
    """
    Accept Create Intent
    ---
    {intent_type}
    {to_city}
    {from_city}
    {to_city} {from_city}
    create a {intent_type} path from {from_city} to {to_city}
    setup a {intent_type} path from {from_city} to {to_city}
    vivonet setup a {intent_type} path from {from_city} to {to_city}
    """
    kwargs = {}
    kwargs['launched'] = launched = session.get('attributes').get('launched')
    kwargs['to_city'] = to_city = to_city or session.get('attributes').get('to_city')
    kwargs['from_city'] = from_city = from_city or session.get('attributes').get('from_city')
    kwargs['intent_type'] = intent_type = intent_type or session.get('attributes').get('intent_type')
    kwargs['confirmation'] = confirmation = confirmation or session.get('attributes').get('confirmation')
    logging.info(session)
    if intent_type:
        types = ["least latency", "high bandwidth", "100ms latency", "least hopcount"]
        if intent_type not in types:
            kwargs['message'] = "Unsupported intent given."
            kwargs['reprompt'] = "You can say least latency, least hop-count or high bandwidth."
            kwargs['end_session'] = False
            return ResponseBuilder.create_response(**kwargs)
    elif intent_type is None:
        kwargs['message'] = "Which intent would you like to setup?"
        kwargs['reprompt'] = "You can say least latency, least hop-count or high bandwidth."
        kwargs['end_session'] = False
        return ResponseBuilder.create_response(**kwargs)
    if from_city and to_city:
        supported_locations = Customer.objects.values_list('location', flat=True)
        supported_locations_lower = map(lambda x: x.lower(), supported_locations)

        if from_city.lower() == to_city.lower():
            kwargs['message'] = "Please give different source and destination cities!"
            kwargs['reprompt'] = "You can say {0} to {1} or any other supported US City.".format(supported_locations[0],
                                                                                                 supported_locations[1])
            kwargs["end_session"] = False
            return ResponseBuilder.create_response(**kwargs)

        if from_city.lower() not in supported_locations_lower or to_city.lower() not in supported_locations_lower:
            kwargs['message'] = "Requested cities not supported!"
            kwargs['reprompt'] = "You can say {0} to {1} or any other supported US City.".format(supported_locations[0],
                                                                                                 supported_locations[1])
            kwargs["end_session"] = False
            return ResponseBuilder.create_response(**kwargs)

    elif from_city is None or to_city is None:
        supported_locations = Customer.objects.values_list('location', flat=True)
        kwargs['message'] = "Between which two cities do you want the path?."
        if len(supported_locations) >= 2:
            kwargs['reprompt'] = "You can say {0} to {1} or any other supported US City.".format(supported_locations[0],
                                                                                                 supported_locations[1])
        else:
            kwargs['reprompt'] = "You can say Denver to Los Angeles or any other US City."
        kwargs["end_session"] = False
        return ResponseBuilder.create_response(**kwargs)

    if not confirmation:
        kwargs['message'] = "ViVoNet will setup a {0} path from {1} to {2}.".format(intent_type, from_city, to_city)
        kwargs['reprompt'] = "Please confirm by saying Yes or No. Please approve the 2 factor request as well!"
        kwargs["end_session"] = False
        return ResponseBuilder.create_response(**kwargs)

    elif "yes" in confirmation:
        check = authenticate_intent("amar")
        if check == "allow":
            intent_type = generate_intent_type(intent_type)
            check_duplicate_intent = check_exsiting_intent(from_city.upper(), to_city.upper())
            if check_duplicate_intent:
                kwargs['message'] = "An intent already exists between requested cities. Please restart for a different intent!"
            else:
                check_intent_status = create_intent(from_city.upper(), to_city.upper(), intent_type)
                if check_intent_status == True:
                    kwargs['message'] = "The requested intent has been setup."
                elif check_intent_status == False:
                    kwargs['message'] = "Some error occurred in the back end."
        elif check == "deny":
            kwargs['message'] = "Requested intent has been denied."

        kwargs.pop('from_city')
        kwargs.pop('intent_type')
        kwargs['launched'] = False
        kwargs["end_session"] = True
        logging.info("Create Intent Finished")
        return ResponseBuilder.create_response(**kwargs)

    elif "no" in confirmation:
        kwargs['message'] = "The requested intent has been cancelled."
        kwargs.pop('from_city')
        kwargs.pop('intent_type')
        kwargs['launched'] = False
        kwargs["end_session"] = True
        logging.info("Create Intent Finished")
        return ResponseBuilder.create_response(**kwargs)

    kwargs['message'] = "Unfortunately, something went wrong!"
    kwargs['reprompt'] = "Please restart by saying launch ViVoNet."
    kwargs["end_session"] = True
    return ResponseBuilder.create_response(**kwargs)


def check_exsiting_intent(from_city, to_city):
    try:

        check_forward_path = Intent_Data.objects.filter(From_Location=from_city, To_Location=to_city)
        check_reverse_path = Intent_Data.objects.filter(To_Location=from_city, From_Location=to_city)
        if check_forward_path and check_reverse_path:
            return True
        else:
            return False
    except:
        return False


def generate_intent_type(intent_type):
    if "least latency" in intent_type.lower():
        intent_type = "least_latency"
    elif "high bandwidth" in intent_type.lower():
        intent_type = "high_bandwidth"
    elif "least hopcount" in intent_type.lower():
        intent_type = "least_hop_count"
    return intent_type


def create_intent(from_city, to_city, intent_type):
    try:
        c = ComputeAndPush('10.0.1.200', from_city, to_city, intent_type)
        status = c.intentEngine()

        c2 = ComputeAndPush('10.0.1.200', to_city, from_city, intent_type)
        status2 = c2.intentEngine()

        if status is not False and status2 is not False:
            return True
        else:
            return False
    except:
        return False


def authenticate_intent(username):
    try:
        auth_client = duo_client.Auth(
            ikey='DI2915C2QQOW6T1TAOBU',
            skey='QsufyeqbDYdI5Sh4EMkroCorfcANCMMoF3E5F10l',
            host="api-53df2292.duosecurity.com",
        )
        if username:
            status = auth_client.auth(device="auto", factor="push", username=username)
            return status['status']
        else:
            return "deny"
    except:
        return "deny"
