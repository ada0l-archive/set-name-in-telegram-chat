""" Run a function by ado <func_name> """


def set_hook():
    import asyncio
    from set_name_in_telegram_chat.settings import HEROKU_APP_NAME, WEBHOOK_URL, TELEGRAM_BOT_API_TOKEN
    from aiogram import Bot
    bot = Bot(token=TELEGRAM_BOT_API_TOKEN)

    async def hook_set():
        if not HEROKU_APP_NAME:
            print('You have forgot to set HEROKU_APP_NAME')
            quit()
        await bot.set_webhook(WEBHOOK_URL)
        print(await bot.get_webhook_info())

    asyncio.run(hook_set())
    bot.close()


def start():
    from set_name_in_telegram_chat.main import main
    main()
