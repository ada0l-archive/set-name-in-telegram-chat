import logging

from aiogram import Bot, Dispatcher, executor, types

from aiogram.contrib.middlewares.logging import LoggingMiddleware

from aiogram.utils.exceptions import BadRequest

import set_name_in_telegram_chat.settings as settings

logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings.TELEGRAM_BOT_API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(
    chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP],
    commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет, кожанный мешок. Я помогу поменять тебе ник в этом ламповом чатике")


@dp.message_handler(
    chat_type=[types.ChatType.PRIVATE],
    commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет, кожанный мешок. Добавь меня в какой-нибудь чатик")


@dp.message_handler(
    chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP],
    commands=['set'])
async def send_welcome(message: types.Message):

    try:
        await bot.promote_chat_member(message.chat.id,
                                      message.from_user.id,
                                      can_invite_users=True)

        await bot.set_chat_administrator_custom_title(message.chat.id,
                                                      message.from_user.id,
                                                      message.get_args())

        await message.reply(f"Теперь ты {message.get_args()}, но все равно кожанный мешок.")

    except BadRequest as e:
        error_message = str(e)
        if error_message == 'Not enough rights':
            await message.reply(f"Не достаточно прав.")
        else:
            logging.error(f"Bad Request: {error_message}")


async def on_startup(dp):
    logging.warning('Starting connection. ')
    await bot.set_webhook(settings.WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dp):
    logging.warning('Bye! Shutting down webhook connection')


def main():
    logging.basicConfig(level=logging.INFO)
    if settings.HEROKU_APP_NAME:
        logging.info("Start webhook")
        executor.start_webhook(
            dispatcher=dp,
            webhook_path=settings.WEBHOOK_PATH,
            skip_updates=True,
            on_startup=on_startup,
            host=settings.WEBAPP_HOST,
            port=settings.WEBAPP_PORT,
        )
    else:
        logging.info("Start polling")
        executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
