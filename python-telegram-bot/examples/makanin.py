#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple Bot to reply to Telegram messages.

This program is dedicated to the public domain under the CC0 license.

This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def readConfig():
    data = ''
    with open('./.env', 'rb') as file:
        data = file.read()

    configs = {}
    config_all = data.split('\n')
    for config in config_all:
        configs[config.split('=')[0]] = config.split('=')[1]

    return configs



def set_timer(bot, update, args, job_queue, chat_data):
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(args[0])
        if due < 0:
            update.message.reply_text('Sorry we can not go back to future!')
            return

        # Add job to queue
        job = job_queue.run_once(alarm, due, context=chat_id)
        chat_data['job'] = job

        update.message.reply_text('Timer successfully set!')

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')



# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def beriMakan(bot, update):
    config = readConfig()
    """Send a message when the command /start is issued."""
    update.message.reply_text('Beri Makan')


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def buka(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Buka')


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def tutup(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Tutup')


def setTimer(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Set Timer')


def addAdmin(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('addAdmin')


def listAdmin(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('List Admin')


def deleteAdmin(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Delete Admin')


def help(bot, update):
    message = "Hai Selamat datang di Makanin Bot.\nBerikut beberapa commands yang bisa dicoba.\n\
    /berimakan - Untuk memberi makan ikan secara otomatis\n\
    /buka - Untuk membuka tutup pakan\n\
    /tutup - Untuk memberi makan ikan secara otomatis\n\
    /settimer - Untuk konfigurasi timer buka dan tutup pakan untuk command /berimakan\n\
    /listadmin - Untuk menampilkan list admin\n\
    /addadmin - Untuk menambahkan admin\n\
    /deleteadmin - Untuk menghapus admin\n\
    /help - Untuk bantuan\n\
    "
    """Send a message when the command /help is issued."""
    update.message.reply_text(message)


def echo(bot, update):
    """Echo the user message."""
    print update.message.text
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("358705908:AAHw1KCmfabvF0O8K4kDq5mmwN2DiAg-5xo")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("berimakan", beriMakan))
    dp.add_handler(CommandHandler("buka", buka))
    dp.add_handler(CommandHandler("tutup", tutup))
    dp.add_handler(CommandHandler("settimer", setTimer))
    dp.add_handler(CommandHandler("listadmin", listAdmin))
    dp.add_handler(CommandHandler("addadmin", addAdmin))
    dp.add_handler(CommandHandler("deleteadmin", deleteAdmin))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("addjob", set_timer,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
