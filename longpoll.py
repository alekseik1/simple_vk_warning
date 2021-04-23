import os
from time import sleep

import vk_api
import redis
from dotenv import load_dotenv
from loguru import logger
from requests.exceptions import ReadTimeout
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from vk_api.utils import get_random_id


load_dotenv()

vk_session = vk_api.VkApi(token=os.environ.get("ACCESS_TOKEN"))
longpoll = VkBotLongPoll(vk_session, os.environ.get("GROUP_ID"))
vk = vk_session.get_api()

ADMIN_ID = "92540660"


def send_message(to_id, message: str) -> None:
    vk.messages.send(peer_id=to_id, random_id=get_random_id(), message=message)


def get_redis():
    return redis.from_url(os.environ.get('REDISTOGO_URL'))


def get_password_from_redis(user_id: int) -> str:
    r = get_redis()
    return r.get(user_id)


def set_password_for_user(user_id: int, password: str) -> bool:
    r = get_redis()
    return r.set(user_id, password)


def handle_message(event):
    logger.info("new message")
    message_text, message_id = event.obj.text, event.obj.id
    user_id = int(event.obj.message['from_id'])
    send_message(user_id, get_password_from_redis(user_id))


def main():
    for event in longpoll.listen():
        # Пока только проверяем входящие сообщения
        if event.type == VkBotEventType.MESSAGE_NEW:
            handle_message(event)


if __name__ == "__main__":
    while True:
        try:
            main()
        except ReadTimeout as e:
            logger.error(
                f"lost connection with vk. Retrying in 10 seconds... Error: {e}"
            )
            sleep(10)
