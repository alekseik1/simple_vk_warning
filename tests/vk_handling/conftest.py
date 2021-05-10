import datetime

import pytest
import json
from vkbottle import API
from vkbottle.tools.test_utils import MockedClient


EXAMPLE_MESSAGE_EVENT = {
    "ts": 1,
    "updates": [
        {
            "type": "message_new",
            "object": {
                "message": {
                    "date": 1620678005,
                    "from_id": 92540660,
                    "id": 1771,
                    "out": 0,
                    "peer_id": 92540660,
                    "text": "hey hey do the zombies stomp?",
                    "conversation_message_id": 1302,
                    "fwd_messages": [

                    ],
                    "important": False,
                    "random_id": 0,
                    "attachments": [

                    ],
                    "is_hidden": False
                },
                "client_info": {
                    "button_actions": [
                        "text",
                        "intent_subscribe",
                        "intent_unsubscribe"
                    ],
                    "keyboard": True,
                    "inline_keyboard": False,
                    "carousel": False,
                    "lang_id": 3
                }
            },
            "group_id": 204187299,
            "event_id": "15cd5841e6fa2ba10c4b4d114a8dc04f78fc47b4"
        },
    ],
}


@pytest.fixture()
def raw_message_builder():
    def build_message(
            text: str,
            from_id: int = 92540660,
            on_datetime: datetime.datetime = datetime.datetime.fromtimestamp(1620678005),
    ):
        rv = EXAMPLE_MESSAGE_EVENT
        rv['updates'][0]['object']['message']['date'] = on_datetime.timestamp()
        rv['updates'][0]['object']['message']['from_id'] = from_id
        rv['updates'][0]['object']['message']['peer_id'] = from_id
        rv['updates'][0]['object']['message']['text'] = text
        return rv
    return build_message


@pytest.fixture()
def fake_vk_api_message_builder(
        raw_message_builder
):
    def api_builder(
        text: str,
        from_id: int = 92540660,
        on_datetime: datetime.datetime = datetime.datetime.fromtimestamp(1620678005),
    ):
        def callback(data: dict):
            if "groups.getById" in data["url"]:
                return {"response": [{"id": 1}]}
            elif "groups.getLongPollServer" in data["url"]:
                return {"response": {"ts": 1, "server": "!SERVER!", "key": ""}}
            elif "!SERVER!" in data["url"]:
                return raw_message_builder(text=text, from_id=from_id, on_datetime=on_datetime)
            elif "messages.send" in data["url"]:
                target_data = data['data']
                if 'keyboard' in target_data:
                    try:
                        json.dumps(target_data['keyboard'])
                    except TypeError:
                        target_data['keyboard'] = target_data['keyboard'].get_json()
                return json.dumps({"response": {**data['data'], **{"r": 1}}})
        api = API("token")
        api.http._session = MockedClient(None, callback=callback)
        return api
    return api_builder
