import random
from pyrogram import enums, filters
from Oneforall import app

INFO_TEXT = """
**❅─────✧❅✦❅✧─────❅**
**✦ ᴜsᴇʀ ɪɴғᴏ ✦**

➻ ᴜsᴇʀ ɪᴅ ‣ **{}**
➻ ғɪʀsᴛ ɴᴀᴍᴇ ‣ **{}**
➻ ʟᴀsᴛ ɴᴀᴍᴇ ‣ **{}**
➻ ᴜsᴇʀɴᴀᴍᴇ ‣ **{}**
➻ ᴍᴇɴᴛɪᴏɴ ‣ **{}**
➻ ʟᴀsᴛ sᴇᴇɴ ‣ **{}**
➻ ᴅᴄ ɪᴅ ‣ **{}**
➻ ʙɪᴏ ‣ **{}**

**❅─────✧❅✦❅✧─────❅**
"""

async def userstatus(user_id):
    try:
        user = await app.get_users(user_id)
        x = user.status
        if x == enums.UserStatus.RECENTLY:
            return "Recently."
        elif x == enums.UserStatus.LAST_WEEK:
            return "Last week."
        elif x == enums.UserStatus.LONG_AGO:
            return "Long time ago."
        elif x == enums.UserStatus.OFFLINE:
            return "Offline."
        elif x == enums.UserStatus.ONLINE:
            return "Online."
    except:
        return "sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ʜᴀᴘᴘᴇɴᴇᴅ !"

@app.on_message(
    filters.command(["info", "userinfo"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"])
)
async def userinfo(_, message):
    user_id = message.from_user.id
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) == 2:
        user_id = message.text.split(None, 1)[1]

    try:
        user_info = await app.get_chat(user_id)
        user = await app.get_users(user_id)
        status = await userstatus(user.id)

        id = user_info.id
        dc_id = user.dc_id
        first_name = user_info.first_name
        last_name = user_info.last_name if user_info.last_name else "No last name"
        username = user_info.username if user_info.username else "No Username"
        mention = user.mention
        bio = user_info.bio if user_info.bio else "No bio set"

        text = INFO_TEXT.format(id, first_name, last_name, username, mention, status, dc_id, bio)
        await message.reply(text, parse_mode=None)  # No HTML or Markdown

    except Exception as e:
        await message.reply(str(e))
        

