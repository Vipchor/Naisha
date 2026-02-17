import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from DAXXMUSIC import LOGGER, app, userbot
from DAXXMUSIC.misc import sudo
from DAXXMUSIC.plugins import ALL_MODULES
from DAXXMUSIC.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

# ✅ SAFE IMPORT (crash nahi hoga)
try:
    from DAXXMUSIC.core.call import DAXX
except ImportError:
    class DAXX:
        @staticmethod
        async def start():
            LOGGER("DAXXMUSIC").warning("DAXX.start() dummy mode")

        @staticmethod
        async def stream_call(_):
            LOGGER("DAXXMUSIC").warning("DAXX.stream_call() dummy mode")

        @staticmethod
        async def decorators():
            pass


async def init():
    if not any([
        config.STRING1,
        config.STRING2,
        config.STRING3,
        config.STRING4,
        config.STRING5,
    ]):
        LOGGER(__name__).error(
            "String Session nahi dali gayi, bot band ho raha hai"
        )
        return

    await sudo()

    try:
        for user_id in await get_gbanned():
            BANNED_USERS.add(user_id)
        for user_id in await get_banned_users():
            BANNED_USERS.add(user_id)
    except Exception as e:
        LOGGER("DAXXMUSIC").warning(f"Ban load error: {e}")

    await app.start()

    for module in ALL_MODULES:
        importlib.import_module("DAXXMUSIC.plugins" + module)

    LOGGER("DAXXMUSIC.plugins").info("All plugins loaded")

    await userbot.start()
    await DAXX.start()

    try:
        await DAXX.stream_call(
            "https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4"
        )
    except NoActiveGroupCall:
        LOGGER("DAXXMUSIC").error(
            "Log group me voice chat start nahi hai"
        )
    except Exception:
        pass

    await DAXX.decorators()

    LOGGER("DAXXMUSIC").info("Bot successfully started")

    await idle()

    await app.stop()
    await userbot.stop()
    LOGGER("DAXXMUSIC").info("Bot stopped")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
