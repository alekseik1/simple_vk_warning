import os
import sys
from loguru import logger

from vkbottle import load_blueprints_from_package
from vkbottle.bot import Bot
from dotenv import load_dotenv

load_dotenv('../.env')
TOKEN = os.environ.get('ACCESS_TOKEN')

bot = Bot(TOKEN)

logger.remove()
logger.add(sys.stderr, level="DEBUG")


for bp in load_blueprints_from_package('blueprints'):
    bp.load(bot)

bot.run_forever()
