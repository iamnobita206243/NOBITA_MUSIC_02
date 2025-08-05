from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import MUSIC_BOT_NAME
from Oneforall import app


@app.on_message(filters.command(["alive"]))
async def start(client: Client, message: Message):
    bot = await app.get_me()
    mention = f"[{bot.first_name}](https://t.me/{bot.username})"

    await message.reply_video(
        video="https://files.catbox.moe/l8duqz.jpg",
        caption=f"""❤️ HEY {message.from_user.mention}\n\n🤖 I AM {mention}\n\n✨ I AM FAST AND POWERFUL MUSIC PLAYER BOT WITH SOME AWESOME FEATURES.\n\n💫 IF YOU HAVE ANY QUESTIONS THEN JOIN OUR SUPPORT GROUP🤍 ...
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="☆ OWNER ☆", url="https://t.me/ll_NOBITA_DEFAULTERS_ll"
                    ),
                    InlineKeyboardButton(
                        text="☆ SUPPORT ☆", url="https://t.me/+WLTHgUavkYVmNtg9"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="☆ UPDATE ☆", url="https://t.me/NOBITA_SUPPORT"
                    ),
                    InlineKeyboardButton(
                        text="★ CLOSE ★", callback_data="close"
                    ),
                ]
            ]
        ),
        parse_mode="markdown"
    )
