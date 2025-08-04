from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums import ChatMembersFilter

from Oneforall import app  # <- this is important
from config import OWNER_ID

admins_cache = {}

async def get_admins(client, chat_id):
    if chat_id in admins_cache:
        return admins_cache[chat_id]
    admins = []
    async for member in client.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
        if not member.user.is_bot:
            admins.append(member.user)
    admins_cache[chat_id] = admins
    return admins


async def handle_join_request(client, message):
    chat_id = message.chat.id
    from_user = message.from_user

    # Get group (chat) title dynamically
    chat = await client.get_chat(chat_id)
    group_name = chat.title

    # Get all admins
    admins = await get_admins(client, chat_id)
    invisible_pings = ''.join([f"[‎](tg://user?id={admin.id})" for admin in admins])

    # Format message
    text = (
        f"🔹HELLO BABY ➥ [{from_user.first_name}](tg://user?id={from_user.id})\n"
        f"🔸WELCOME TO ➥ **{group_name}**\n\n"
        f"{invisible_pings}"
    )

    # Buttons
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✅ 𝐀ᴄᴄᴇᴘᴛ", callback_data=f"approve_{chat_id}_{from_user.id}"),
                InlineKeyboardButton("❌ 𝐑ᴇᴊᴇᴄᴛ", callback_data=f"disapprove_{chat_id}_{from_user.id}")
            ],
            [
                InlineKeyboardButton("⚡ 𝐀ᴜᴛᴏ 𝐀ᴄᴄᴇᴘᴛ 𝐎ɴ", callback_data="noop")
            ]
        ]
    )

    await client.send_message(chat_id, text, reply_markup=buttons)

@app.on_chat_join_request()
async def on_join_request(client, message):
    print("Join request received")  # DEBUG
    await handle_join_request(client, message)


@app.on_callback_query(filters.regex(r"^(approve|disapprove)_(\-?\d+)_(\d+)$"))
async def on_approval_action(client, callback_query: CallbackQuery):
    action, chat_id, user_id = callback_query.data.split("_")
    chat_id = int(chat_id)
    user_id = int(user_id)

    if callback_query.from_user.id not in [admin.id for admin in await get_admins(client, chat_id)]:
        return await callback_query.answer("Only admins can approve or disapprove.", show_alert=True)

    if action == "approve":
        try:
            await client.approve_chat_join_request(chat_id, user_id)
            await callback_query.edit_message_text("✅ 𝐔sᴇʀ 𝐇ᴀs 𝐁ᴇᴇɴ 𝐀ᴘᴘʀᴏᴠᴇᴅ.")
        except Exception as e:
            await callback_query.edit_message_text(f"𝐅ᴀɪʟᴇᴅ 𝐓ᴏ 𝐀ᴘᴘʀᴏᴠᴇ: {e}")
    else:
        try:
            await client.decline_chat_join_request(chat_id, user_id)
            await callback_query.edit_message_text("❌ 𝐔sᴇʀ 𝐇ᴀs 𝐁ᴇᴇɴ 𝐃ɪsᴀᴘᴘʀᴏᴠᴇᴅ.")
        except Exception as e:
            await callback_query.edit_message_text(f"𝐅ᴀɪʟᴇᴅ 𝐓ᴏ 𝐃ɪsᴀᴘᴘʀᴏᴠᴇ: {e}")
