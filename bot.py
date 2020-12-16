import logging
import os
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from MSRIT import MSRIT_RES

# Your Telegram Bot Token
TOKEN = "<YOUR BOT TOKEN>"
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


start_msg = '''
<b>HELLO THERE </b>👋👋
<i>Welcome TO RIT Result Grabber Bot</i>
<i>Type in your USN to get started or hit /help for more help</i>
'''

help_msg = '''
<i> To get Your reusults just type in your usn </i>
<b>To Get PDF file of your Provisional Grade Card use /download command followed by your USN</b>
ex : /download 1ms.....
'''

# Function to Get The data and return it


def result(usn):
    try:
        usn = usn
        data = MSRIT_RES(usn)
        name = data.Name()
        sem = data.sem()
        cr = data.credits_reg()
        ce = data.credits_earned()
        sgpa = data.sgpa()
        cgpa = data.cgpa()
        res_table = data.result_table()

        msg = f'''<b>Name</b> : {name}
        <b>USN</b> : {usn}
        <b>SEMISTER</b> : {sem}
        <b>CREDITS REGISTERD</b> : {cr}
        <b>CREDITS EARNED</b> : {ce}
        <b>SGPA</b> : {sgpa}
        <b>CGPA</b> : {cgpa}
        '''+"<pre>" + res_table + "</pre>"+'''
        <b>C N</b> :<i> Course Name</i>
        <b>C E</b> :<i> Credits Earned</i>
        <b> G </b> :<i> Grades </i> '''
        return msg
    except Exception:
        return "INVALID USN"

# Funtion to get provisional grade card Url


def gradecard(usn) -> str:
    if(usn.startswith("1ms") and len(usn) == 10):
        usn = usn
        gc = MSRIT_RES(usn)
        url = gc.markscardpdf()
        return url
    else:
        return "INVALID USN"


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_html(start_msg)


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_html(help_msg)


def download_gradecard(update: Update, context: CallbackContext) -> None:
    """Send the provisional grade card when /download command is follwed by valid USN"""
    text = update.message.text
    try:
        usn = text.split(" ")[1]
        url = gradecard(usn)
        if (not(url == "INVALID USN")):
            msg = update.message.reply_text("Downloading.......")
            file = requests.get(url).content
            with open(f"{usn}.pdf", "wb") as f:
                f.write(file)
            update.message.reply_document(document=open(f"{usn}.pdf", "rb"))
            msg.edit_text("Finished...")
            os.remove(f"{usn}.pdf")
        else:
            update.message.reply_text("INVALID USN")
    except Exception:
        update.message.reply_text("No USN detected")


def showresult(update: Update, context: CallbackContext) -> None:
    """Send The Result with Table when Valid USN is sent"""
    usn = update.message.text
    res_data = result(usn)
    update.message.reply_html(res_data)


def contact(update, context):
    """Gives the Maker Contact info"""
    keyboard = [[InlineKeyboardButton(
        "Contact", url="telegram.me/phantom2152")], ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Contact The Maker:', reply_markup=reply_markup)


def main():
    updater = Updater(TOKEN, use_context=True)
    PORT = int(os.environ.get('PORT', '8443'))
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("download", download_gradecard))
    dp.add_handler(CommandHandler("contact", contact))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, showresult))

    # Start The bot
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    updater.bot.set_webhook(
        "https://<YOUR APP NAME>.herokuapp.com/" + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()
