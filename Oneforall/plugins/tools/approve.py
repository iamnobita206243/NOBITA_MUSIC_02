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

    admins = await get_admins(client, chat_id)
    admin_mentions = [f"[‎](tg://user?id={admin.id})" for admin in admins]
    text = (
        f"**New Join Request**\n"
        f"**User:** [{from_user.first_name}](tg://user?id={from_user.id})\n\n"
        f"{' '.join(admin_mentions)}\n"
        f"Do you want to approve or disapprove?"
    )

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✅ Approve", callback_data=f"approve_{chat_id}_{from_user.id}"),
                InlineKeyboardButton("❌ Disapprove", callback_data=f"disapprove_{chat_id}_{from_user.id}")
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
            await callback_query.edit_message_text("✅ User has been approved.")
        except Exception as e:
            await callback_query.edit_message_text(f"Failed to approve: {e}")
    else:
        try:
            await client.decline_chat_join_request(chat_id, user_id)
            await callback_query.edit_message_text("❌ User has been disapproved.")
        except Exception as e:
            await callback_query.edit_message_text(f"Failed to disapprove: {e}")
