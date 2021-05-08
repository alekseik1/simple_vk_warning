from aioredis import Redis
from vkbottle import BaseMiddleware
from loguru import logger

from src.redis_.crud import get_redis


class RedisMiddleware(BaseMiddleware):
    __redis: Redis = None

    async def pre(self) -> None:
        if self.__redis is None:
            logger.info('creating redis pool')
            self.__redis = await get_redis()
        self.send({'redis': self.__redis})