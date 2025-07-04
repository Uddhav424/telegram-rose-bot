import os
from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from utils.moderation import warn_user, mute_user, ban_user, kick_user, is_admin

load_dotenv()

BOT_TOKEN = os.getenv("7760135917:AAFBV1o8stZ_EpAL3T1tXUzMsQNQ0t2c0-s")
WELCOME_MESSAGE = "Welcome, {name}! Please follow the group rules."

# Welcome new users
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await update.message.reply_text(WELCOME_MESSAGE.format(name=member.full_name))

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I'm alive! Use /help for commands.")

# Help command
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/warn @user reason\n/mute @user mins\n/ban @user\n/kick @user"
    )

# Anti-link handler
async def delete_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "http" in update.message.text.lower():
        await update.message.delete()

# Main app
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("warn", warn_user))
    app.add_handler(CommandHandler("mute", mute_user))
    app.add_handler(CommandHandler("ban", ban_user))
    app.add_handler(CommandHandler("kick", kick_user))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("http"), delete_links))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
                
