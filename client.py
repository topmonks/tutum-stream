import os
import websocket
import json
import logging

from integrations.hipchat import generic_hipchat, post_hipchat
from integrations.utilities import get_resource

STACK_NAME = os.environ.get('STACK_NAME', '')

def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"

def on_message(ws, message):
    msg_as_JSON = json.loads(message)
    type = msg_as_JSON.get("type")
    if type:
        if type == "auth":
            print("Auth completed")
        elif type == "container":
            generic_hipchat(message)
        elif type == "service":
            parents = msg_as_JSON.get("parents")
            service = get_resource(msg_as_JSON.get("resource_uri"))
            service_as_JSON = json.loads(service)

            if parents:
                stack = get_resource(parents[0])
                stack_as_JSON = json.loads(stack)
                stack_name = stack_as_JSON.get('name')
                if STACK_NAME and stack_name != STACK_NAME:
                    # do nothing
                    print("Doing nothing, STACK_NAME({}) set and notification is related to different stack({})".format(STACK_NAME,stack_namegit ))
                else:
                    text = ("A Service {} was {}d. The current state is {}. \nIt belonged to the "
                        "{} Stack.\nThe Stack state is: {}".format(service_as_JSON.get('name'),
                                                                   msg_as_JSON.get('action'),
                                                                   service_as_JSON.get('state'),
                                                                   stack_name,
                                                                   stack_as_JSON.get('state')))
                    post_hipchat(text=text)
        elif type != "user-notifications":
            print("{}:{}:{}:{}:{}".format(type, msg_as_JSON.get("action"), msg_as_JSON.get("state"), msg_as_JSON.get("resource_uri"), msg_as_JSON.get("parents")))

def on_open(ws):
    print "Connected"

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    websocket.enableTrace(False)
    token = os.environ.get('TUTUM_TOKEN')
    username = os.environ.get('TUTUM_USERNAME')
    TUTUM_AUTH = os.environ.get('TUTUM_AUTH')

    if TUTUM_AUTH:
        TUTUM_AUTH = TUTUM_AUTH.replace(' ', '%20')
        url = 'wss://stream.tutum.co/v1/events?auth={}'.format(TUTUM_AUTH)
    elif token and username:
        url = 'wss://stream.tutum.co/v1/events?token={}&user={}'.format(token, username)
    else:
        raise Exception("Please provide authentication credentials")

    ws = websocket.WebSocketApp(url,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close,
                                on_open = on_open)

    try:
        ws.run_forever()
    except KeyboardInterrupt:
        pass
