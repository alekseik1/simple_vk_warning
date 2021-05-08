import os
import aiohttp
from vkbottle import BotBlueprint
from vkbottle.bot import Message, rules
from loguru import logger
from src.keyboards import KEYBOARD_ENTRYPOINT
from src.settings import TECHNICAL_ADMIN_ID
from src.commands import AdminOpenLock

ADMIN_HARDCODED_LIST = [
    TECHNICAL_ADMIN_ID,
    94592201
]

STRIKA_DOOR_OPEN_URL = 'http://8ka.mipt.ru/door_control/5b/open'

bl = BotBlueprint()
bl.labeler.auto_rules = [rules.PeerRule(from_chat=False), rules.FromPeerRule(ADMIN_HARDCODED_LIST)]


@bl.labeler.message(command=AdminOpenLock.raw_message_name)
@bl.labeler.message(payload={'cmd': AdminOpenLock.key})
async def handle_open_door_request(message: Message, **kwargs):
    token = os.environ.get('SECRET_BOT_TOKEN')
    if token is None:
        logger.warning('failure in token read')
        await message.answer(
            message='Мне не удалось считать токен, поэтому я не смогу открыть замок. Возврат в меню',
            keyboard=KEYBOARD_ENTRYPOINT
        )
    else:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        STRIKA_DOOR_OPEN_URL,
                        params={'secret_token': token}
                ) as resp:
                    if resp.status != 200:
                        content = resp.content.read()
                        logger.warning(f'response is invalid | status = {resp.status} | content={content}')
                        await message.answer(
                            message=f'Запрос вернул status_code={resp.status} != 200, так не должно быть. '
                                    f'Вот контент: {content}',
                            keyboard=KEYBOARD_ENTRYPOINT
                        )
                        return
                    else:
                        await message.answer(
                            message='Дверь в 5Б должна быть открыта. '
                                    'Не забудь, пожалуйста, нажать кнопку, когда будешь уходить!',
                            keyboard=KEYBOARD_ENTRYPOINT
                        )
        except Exception as e:
            logger.error(f'Unknown error: {e}')
