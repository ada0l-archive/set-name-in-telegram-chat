import logging

from aiogram import Bot, Dispatcher, executor, types, utils

import set_name_in_telegram_chat.settings as settings

logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings.TELEGRAM_BOT_API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(
    chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP],
    commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет, кожанный мешок.\nЯ помогу поменять тебе ник в этом ламповом чатике")


@dp.message_handler(
    chat_type=[types.ChatType.PRIVATE],
    commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет, кожанный мешок.\n. Добавь меня в какой-нибудь чатик")


@dp.message_handler(
    chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP],
    commands=['set'])
async def send_welcome(message: types.Message):
    try:
        await bot.promote_chat_member(message.chat.id,
                                      message.from_user.id,
                                      can_pin_messages=True)
        await bot.set_chat_administrator_custom_title(message.chat.id,
                                                      message.from_user.id,
                                                      message.get_args())
        await message.reply(f"Теперь ты {message.get_args()}, но все равно кожанный мешок.")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
