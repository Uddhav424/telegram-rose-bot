from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes
import datetime

# Admin check
async def is_admin(update: Update):
    user_id = update.effective_user.id
    chat_admins = await update.effective_chat.get_administrators()
    return user_id in [admin.user.id for admin in chat_admins]

async def warn_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        return await update.message.reply_text("Only admins can use this.")

    target = update.message.reply_to_message
    reason = " ".join(context.args) or "No reason"
    await update.message.reply_text(f"{target.from_user.full_name} has been warned.\nReason: {reason}")

async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        return await update.message.reply_text("Only admins can use this.")
    target = update.message.reply_to_message
    mins = int(context.args[0]) if context.args else 5
    until = datetime.datetime.now() + datetime.timedelta(minutes=mins)
    await context.bot.restrict_chat_member(update.effective_chat.id, target.from_user.id,
                                           ChatPermissions(can_send_messages=False), until)
    await update.message.reply_text(f"{target.from_user.full_name} has been muted for {mins} minutes.")

async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        return await update.message.reply_text("Only admins can use this.")
    target = update.message.reply_to_message
    await context.bot.ban_chat_member(update.effective_chat.id, target.from_user.id)
    await update.message.reply_text(f"{target.from_user.full_name} has been banned.")

async def kick_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        return await update.message.reply_text("Only admins can use this.")
    target = update.message.reply_to_message
    await context.bot.ban_chat_member(update.effective_chat.id, target.from_user.id)
    await context.bot.unban_chat_member(update.effective_chat.id, target.from_user.id)
    await update.message.reply_text(f"{target.from_user.full_name} has been kicked.")
