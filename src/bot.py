from aiogram import Dispatcher, Bot

dp: Dispatcher
bot: Bot


def setup_dp(dp_) -> None:
    global dp
    dp = dp_

def get_dp() -> Dispatcher:
    global dp

    return dp

def setup_bot(bot_) -> None:
    global bot

    bot = bot_

def get_bot() -> Bot:
    global bot

    return bot