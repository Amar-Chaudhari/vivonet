import logging

from django_alexa.api import fields, intent, ResponseBuilder

logger = logging.getLogger("django_alexa.views")

INTENT_TYPES = ("least latency", "high bandwidth", "100ms latency")


class CreateIntentSlots(fields.AmazonSlots):
    intent_type = fields.AmazonCustom(label="INTENT_TYPES", choices=INTENT_TYPES)
    to_city = fields.AmazonUSCity()
    from_city = fields.AmazonUSCity()

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
    kwargs['reprompt'] = "Which intent would you like to setup? You can say least latency, bandwidth or hopcount"
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


@intent(app="intents", slots=CreateIntentSlots)
def CreateIntent(session, intent_type, from_city, to_city):
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
    print session
    kwargs['launched'] = launched = session.get('attributes').get('launched')
    kwargs['to_city'] = to_city = to_city or session.get('attributes').get('to_city')
    kwargs['from_city'] = from_city = from_city or session.get('attributes').get('from_city')
    kwargs['intent_type'] = intent_type = intent_type or session.get('attributes').get('intent_type')
    logging.info(intent_type)
    logging.info(to_city)
    logging.info(from_city)
    if intent_type is None:
        kwargs['message'] = "Which intent would you like to setup? You can say least latency, bandwidth or hopcount"
        kwargs['end_session'] = False
        return ResponseBuilder.create_response(**kwargs)
    elif from_city is None or to_city is None:
        kwargs['message'] = "From which city to what city do you want the path?"
        kwargs['reprompt'] = "You can say Denver to Los Angeles or any other US City"
        kwargs["end_session"] = False
        return ResponseBuilder.create_response(**kwargs)
    else:
        kwargs['message'] = "ViVoNet will setup a {0} path from {1} to {2}".format(intent_type, from_city, to_city)
        kwargs.pop('to_city')
        kwargs.pop('from_city')
        kwargs.pop('intent_type')
        kwargs['launched'] = False
        kwargs["end_session"] = True
        logging.info("Create Intent Finished")
    return ResponseBuilder.create_response(**kwargs)
