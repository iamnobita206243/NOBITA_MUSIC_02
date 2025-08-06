import re
import time

from pyrogram import filters
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message

from Oneforall import app
from Oneforall.mongo.afkdb import add_afk, is_afk, remove_afk
from Oneforall.mongo.readable_time import get_readable_time


@app.on_message(filters.command(["afk", "brb"], prefixes=["/", "!"]))
async def active_afk(_, message: Message):
    if message.sender_chat:
        return
    user_id = message.from_user.id
    verifier, reasondb = await is_afk(user_id)
    if verifier:
        await remove_afk(user_id)
        timeafk = reasondb["time"]
        reasonafk = reasondb["reason"]
        seenago = get_readable_time(int(time.time() - timeafk))

        if reasonafk:
            await message.reply_text(
                f"**{message.from_user.first_name}** is back online and was away for {seenago}\n\nReason: `{reasonafk}`"
            )
        else:
            await message.reply_text(
                f"**{message.from_user.first_name}** is back online and was away for {seenago}"
            )

    if len(message.command) == 1:
        details = {
            "type": "text",
            "time": time.time(),
            "data": None,
            "reason": None,
        }
    else:
        _reason = (message.text.split(None, 1)[1].strip())[:100]
        details = {
            "type": "text_reason",
            "time": time.time(),
            "data": None,
            "reason": _reason,
        }

    await add_afk(user_id, details)
    await message.reply_text(f"{message.from_user.first_name} is now AFK.")


@app.on_message(~filters.me & ~filters.bot & ~filters.via_bot, group=1)
async def chat_watcher_func(_, message):
    if message.sender_chat:
        return

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    msg = ""

    # Remove AFK if user sends message
    verifier, reasondb = await is_afk(user_id)
    if verifier:
        await remove_afk(user_id)
        timeafk = reasondb["time"]
        reasonafk = reasondb["reason"]
        seenago = get_readable_time(int(time.time() - timeafk))

        if reasonafk:
            msg += f"**{user_name}** is back online and was away for {seenago}\n\nReason: `{reasonafk}`\n\n"
        else:
            msg += f"**{user_name}** is back online and was away for {seenago}\n\n"

    # Check if replying to AFK user
    if message.reply_to_message:
        try:
            r_user = message.reply_to_message.from_user
            r_verifier, r_reasondb = await is_afk(r_user.id)
            if r_verifier:
                r_timeafk = r_reasondb["time"]
                r_reasonafk = r_reasondb["reason"]
                r_seenago = get_readable_time(int(time.time() - r_timeafk))
                if r_reasonafk:
                    msg += f"**{r_user.first_name}** is AFK since {r_seenago}\n\nReason: `{r_reasonafk}`\n\n"
                else:
                    msg += f"**{r_user.first_name}** is AFK since {r_seenago}\n\n"
        except:
            pass

    # Check for mentions
    if message.entities:
        entity = message.entities
        for i in range(len(entity)):
            ent = entity[i]
            try:
                if ent.type == MessageEntityType.MENTION:
                    username = re.findall("@([_0-9a-zA-Z]+)", message.text)[i]
                    user = await app.get_users(username)
                elif ent.type == MessageEntityType.TEXT_MENTION:
                    user = ent.user
                else:
                    continue

                if user.id == message.reply_to_message.from_user.id:
                    continue

                v, db = await is_afk(user.id)
                if v:
                    t = db["time"]
                    r = db["reason"]
                    sa = get_readable_time(int(time.time() - t))
                    if r:
                        msg += f"**{user.first_name}** is AFK since {sa}\n\nReason: `{r}`\n\n"
                    else:
                        msg += f"**{user.first_name}** is AFK since {sa}\n\n"
            except:
                continue

    if msg:
        await message.reply_text(msg, disable_web_page_preview=True)
