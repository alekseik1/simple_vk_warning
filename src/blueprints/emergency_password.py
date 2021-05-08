import aioredis
from vkbottle import BotBlueprint
from vkbottle.bot import Message, rules
from src.redis_.crud import get_password_from_redis

bl = BotBlueprint()
bl.labeler.auto_rules = [rules.PeerRule(from_chat=False)]


@bl.labeler.message(command='пароль')
@bl.labeler.message(payload={'cmd': 'get_password'})
async def send_emergency_password(message: Message, redis: aioredis.Redis):
    user_id = message.from_id
    answer = f"Логин: {user_id}\nПароль: {await get_password_from_redis(redis, user_id=user_id)}"
    return answer
