import json
import os
import requests

HIPCHAT_URL = os.environ.get('HIPCHAT_URL', '')
HIPCHAT_ROOM = os.environ.get('HIPCHAT_ROOM', '')
HIPCHAT_TOKEN = os.environ.get('HIPCHAT_TOKEN', '')

def post_hipchat(text=None, hipchat_url=HIPCHAT_URL, hipchat_room=HIPCHAT_ROOM, hipchat_token=HIPCHAT_TOKEN):
    if not hipchat_url:
        raise Exception('Please provide a Hipchat URL')
    if not hipchat_token:
            raise Exception('Please provide a Hipchat Notification token')
    if not hipchat_room:
            raise Exception('Please provide a Hipchat ROOM')

    if not text:
        text = "You received a message from Tutum Stream!"
    data = {'color': 'purple', 'message': text}

    headers = {'Content-type' : 'application/json',
               'Authorization' : "Bearer {}".format(hipchat_token)}

    r = requests.post("{}/v2/room/{}/notification".format(hipchat_url,hipchat_room), data=json.dumps(data), headers=headers)
    return r

def generic_hipchat(message):
    msg_as_JSON = json.loads(message)
    text = ("Your {} was {}d on Tutum!\n"
            "Check {} to see more details.".format(msg_as_JSON.get('type'),
                                                   msg_as_JSON.get('action'),
                                                   msg_as_JSON.get('resource_uri')))
    post_hipchat(text=text)
