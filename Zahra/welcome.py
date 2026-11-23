
from pyrogram import filters
from pyrogram.types import Message


async def welcome_new_member(client, message: Message):
    for member in message.new_chat_members:
        if member.is_bot:
            continue

        name = member.first_name

        await message.reply_text(
            f"💜 Welcome to the group, {name}!\n\n"
            "✨ Welcome to ZAHRA FEDERATION protected group!\n"
            "Please follow the group rules."
        )


def register_welcome(app):
    app.on_message(
        filters.new_chat_members
    )(welcome_new_member)
