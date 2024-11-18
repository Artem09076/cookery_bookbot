from aiogram import Bot, Dispatcher

from src.logger import logger

dp: Dispatcher
bot: Bot


def setup_dp(dp_) -> None:
    global dp
    dp = dp_
    logger.info('Dispatcher успешно настроен.')


def get_dp() -> Dispatcher:
    global dp
    logger.debug('Dispatcher получен.')
    return dp


def setup_bot(bot_) -> None:
    global bot
    bot = bot_
    logger.info('Bot успешно настроен.')


def get_bot() -> Bot:
    global bot
    logger.debug('Bot получен.')
    return bot
