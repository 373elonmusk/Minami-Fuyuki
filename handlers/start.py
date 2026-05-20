# ============================================================
#Group Manager Bot
# Author: LearningBotsOfficial (https://github.com/LearningBotsOfficial) 
# Support: https://t.me/LearningBotsCommunity
# Channel: https://t.me/learning_bots
# YouTube: https://youtube.com/@learning_bots
# License: Open-source (keep credits, no resale)
# ============================================================


from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto
)
from config import BOT_USERNAME, SUPPORT_GROUP, UPDATE_CHANNEL, START_IMAGE, OWNER_ID
import db

def register_handlers(app: Client):

# ==========================================================
# Start Message
# ==========================================================
    async def send_start_menu(message, user):
        text = (
            f"Hey there, {user}! 👋\n"
            "\n"
            "My name is <b>Minami Fuyuki</b> — I'm here to help you manage your groups like a pro! "
            "Use /help to find out how to use me to my full potential.\n"
            "\n"
            'Join my <a href="https://t.me/shinchan_bots">news channel</a> to get information on all the latest updates.\n'
            "\n"
            "Check /privacy to view the privacy policy, and interact with your data."
        )

        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("➕ Add me to your chat", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
                InlineKeyboardButton("⭐ Support", url=SUPPORT_GROUP),
            ],
            [
                InlineKeyboardButton("📢 News Channel", url="https://t.me/shinchan_bots"),
                InlineKeyboardButton("⌂ Update ⌂", url=UPDATE_CHANNEL),
            ],
            [
                InlineKeyboardButton("※ ŎŴɳēŔ ※", url=f"tg://user?id={OWNER_ID}"),
                InlineKeyboardButton("Repo", url="https://github.com/LearningBotsOfficial/Nomade"),
            ],
            [InlineKeyboardButton("📚 Help Commands 📚", callback_data="help")]
        ])

        # If /start command, send a new photo
        if message.text:
            await message.reply_photo(START_IMAGE, caption=text, reply_markup=buttons, parse_mode="html")
        else:
            # If callback, edit the same message
            media = InputMediaPhoto(media=START_IMAGE, caption=text, parse_mode="html")
            await message.edit_media(media=media, reply_markup=buttons)

# ==========================================================
# Start Command
# ==========================================================
    @app.on_message(filters.private & filters.command("start"))
    async def start_command(client, message):
        user = message.from_user
        await db.add_user(user.id, user.first_name)
        await send_start_menu(message, user.first_name)

# ==========================================================
# Help Menu Message
# ==========================================================
    async def send_help_menu(message):
        text = (
            "╔══════════════════╗\n"
            "     Help Menu\n"
            "╚══════════════════╝\n"
            "\n"
            "Choose a category below to explore commands:\n"
            "─────────────────────────────"
        )
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⌂ Greetings ⌂", callback_data="greetings"),
                InlineKeyboardButton("⌂ Locks ⌂", callback_data="locks"),
            ],
            [
                InlineKeyboardButton("⌂ Moderation ⌂", callback_data="moderation")
            ],
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_start")]
        ])

        media = InputMediaPhoto(media=START_IMAGE, caption=text)
        await message.edit_media(media=media, reply_markup=buttons)

# ==========================================================
# Help Callback_query
# ==========================================================
    @app.on_callback_query(filters.regex("help"))
    async def help_callback(client, callback_query):
        await send_help_menu(callback_query.message)
        await callback_query.answer()

# ==========================================================
# back to start Callback_query
# ==========================================================
    @app.on_callback_query(filters.regex("back_to_start"))
    async def back_to_start_callback(client, callback_query):
        user = callback_query.from_user.first_name
        await send_start_menu(callback_query.message, user)
        await callback_query.answer()

# ==========================================================
# Greetings Callback_query
# ==========================================================
    @app.on_callback_query(filters.regex("greetings"))
    async def greetings_callback(client, callback_query):
        text = (
            "╔══════════════════╗\n"
            "    ⚙ Welcome System\n"
            "╚══════════════════╝\n"
            "\n"
            "Commands to Manage Welcome Messages:\n"
            "\n"
            "- /setwelcome <text> : Set a custom welcome message for your group\n"
            "- /welcome on        : Enable the welcome messages\n"
            "- /welcome off       : Disable the welcome messages\n"
            "\n"
            "Supported Placeholders:\n"
            "- {username} : Telegram username\n"
            "- {first_name} : User's first name\n"
            "- {id} : User ID\n"
            "- {mention} : Mention user in message\n"
            "\n"
            "Example:\n"
            " /setwelcome Hello {first_name}! Welcome to {title}!"
        )
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="help")]
        ])
        media = InputMediaPhoto(media=START_IMAGE, caption=text)
        await callback_query.message.edit_media(media=media, reply_markup=buttons)
        await callback_query.answer()

# ==========================================================
# Locks callback_query
# ==========================================================
    @app.on_callback_query(filters.regex("locks"))
    async def locks_callback(client, callback_query):
        text = (
            "╔══════════════════╗\n"
            "     ⚙ Locks System\n"
            "╚══════════════════╝\n"
            "\n"
            "Commands to Manage Locks:\n"
            "\n"
            "- /lock <type>    : Enable a lock for the group\n"
            "- /unlock <type>  : Disable a lock for the group\n"
            "- /locks          : Show currently active locks\n"
            "\n"
            "Available Lock Types:\n"
            "- url       : Block links\n"
            "- sticker   : Block stickers\n"
            "- media     : Block photos/videos/gifs\n"
            "- username  : Block messages with @username mentions\n"
            "- language  : Block non-English messages\n"
            "\n"
            "Example:\n"
            " /lock url       : Blocks any messages containing links\n"
            " /unlock sticker : Allows stickers again"
        )
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="help")]
        ])
        media = InputMediaPhoto(media=START_IMAGE, caption=text)
        await callback_query.message.edit_media(media=media, reply_markup=buttons)
        await callback_query.answer()

# ==========================================================
# Moderation Callback_query
# ==========================================================
    @app.on_callback_query(filters.regex("moderation"))
    async def info_callback(client, callback_query):
        try:
            text = (
                "╔══════════════════╗\n"
                "      ⚙️ Moderation System\n"
                "╚══════════════════╝\n"
                "\n"
                "Manage your group easily with these tools:\n"
                "\n"
                "¤ /kick <user> — Remove a user\n"
                "¤ /ban <user> — Ban permanently\n"
                "¤ /unban <user> — Lift ban\n"
                "¤ /mute <user> — Disable messages\n"
                "¤ /unmute <user> — Allow messages again\n"
                "¤ /warn <user> — Add warning (3 = mute)\n"
                "¤ /warns <user> — View warnings\n"
                "¤ /resetwarns <user> — Clear all warnings\n"
                "¤ /promote <user> — make admin\n"
                "¤ /demote <user> — remove from admin\n"
                "\n"
                "💡 Example:\n"
                "Reply to a user or type\n"
                "<code>/ban @username</code>"
            )
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="help")]
            ])

            media = InputMediaPhoto(media=START_IMAGE, caption=text, parse_mode="html")
            await callback_query.message.edit_media(media=media, reply_markup=buttons)
            await callback_query.answer()

        except Exception as e:
            print(f"Error in info_callback: {e}")
            await callback_query.answer("❌ Something went wrong.", show_alert=True)


# ==========================================================
# Broadcast Command
# ==========================================================
    @app.on_message(filters.private & filters.command("broadcast"))
    async def broadcast_message(client, message):
        if not message.reply_to_message:
            await message.reply_text("⚠️ Please reply to a message to broadcast it.")
            return

        if message.from_user.id != OWNER_ID:
            await message.reply_text("❌ Only the bot owner can use this command.")
            return

        text_to_send = message.reply_to_message.text or message.reply_to_message.caption
        if not text_to_send:
            await message.reply_text("⚠️ The replied message has no text to send.")
            return

        users = await db.get_all_users()
        sent, failed = 0, 0

        await message.reply_text(f"Broadcasting to {len(users)} users..")

        for user_id in users:
            try:
                await client.send_message(user_id, text_to_send)
                sent += 1
            except Exception:
                failed += 1

        await message.reply_text(f"✅ Broadcast finished!\n\n Sent: {sent}\nFailed: {failed}")

# ==========================================================
# stats Command
# ==========================================================
    @app.on_message(filters.private & filters.command("stats"))
    async def stats_command(client, message):
        if message.from_user.id != OWNER_ID:
            return await message.reply_text("❌ Only the bot owner can use this command")

        users = await db.get_all_users()
        return await message.reply_text(f"💡 Total users: {len(users)}")
