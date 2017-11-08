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
import os
import base64

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

true = True
false = False

def getListAdmin():
    data = ''
    with open('./.admin', 'rb') as file:
        data = file.read()

    admins  = base64.b64decode(data)

    return admins.split(',')

def reWriteDaftarAdmin(admins):
    with open('./.admin', 'wb') as file:
        file.write(base64.b64encode(','.join(admins)))

def checkIfAdmin(username):
    
    listAdmin = getListAdmin()

    if username in listAdmin:
        return true
    else:
        return false

def tambahAdmin(bot, update, args):

    listAdmin = getListAdmin()

    if (checkIfAdmin(update.message.from_user.username) == false):
        update.message.reply_text('Anda tidak berhak')
    else:

        if len(args) <= 0 or len(args) > 1:
            update.message.reply_text('Bad Request!, parameter tidak sesuai')
            return

        username = args[0]
        if (username not in listAdmin):
            listAdmin.append(username)
            reWriteDaftarAdmin(listAdmin)
            update.message.reply_text(username + ' telah ditambah sebagai admin')
        else:
            update.message.reply_text('Gagal menambahkan '+ username + ' sebagai admin, ' + username + ' sudah menjadi admin')

def hapusAdmin(bot, update, args):

    listAdmin = getListAdmin()

    if (checkIfAdmin(update.message.from_user.username) == false):
        update.message.reply_text('Anda tidak berhak')
    else:
        
        if len(args) <= 0 or len(args) > 1:
            update.message.reply_text('Bad Request!, parameter tidak sesuai')
            return

        username = args[0]

        listAdmin.remove(username)
        reWriteDaftarAdmin(listAdmin)

        update.message.reply_text(username + ' telah dihapus dari admin')

def daftarAdmin(bot, update):
    listAdmin = getListAdmin()
    if (checkIfAdmin(update.message.from_user.username) == false):
        update.message.reply_text('Anda tidak berhak')
    else:
        message = 'Daftar admin adalah : '
        update.message.reply_text(message + ", ".join(listAdmin))

def set_timer(bot, update, args):
    if (checkIfAdmin(update.message.from_user.username) == false):
        update.message.reply_text('Anda tidak berhak')
    else:
        if len(args) <= 0 or len(args) > 1:
            update.message.reply_text('Bad Request!, parameter tidak sesuai')
            return
        try:
            time = int(args[0])
        except Exception as e:
            update.message.reply_text('Bad Request!, parameter tidak sesuai')
            return            

        with open('./.env', 'wb') as file:
            file.write('timer='+str(time))

        update.message.reply_text('Waktu buka tutup pintu berhasil diatur menjadi '+str(time)+'s')


def beriMakan(bot, update):
    if (checkIfAdmin(update.message.from_user.username) == false):
        update.message.reply_text('Anda tidak berhak')
    else:
        
        try:
            os.system('python servobuka.py')
        except Exception as e:
            update.message.reply_text('Kesalahan pada sistem, tidak bisa memberi makan peliharaan')
            return

        update.message.reply_text('Telah diberi makan')

def buka(bot, update):
    if (checkIfAdmin(update.message.from_user.username) == false):
        update.message.reply_text('Anda tidak berhak')
    else:
        update.message.reply_text('Buka')

def tutup(bot, update):
    if (checkIfAdmin(update.message.from_user.username) == false):
        update.message.reply_text('Anda tidak berhak')
    else:
        update.message.reply_text('Tutup')

#def setTimer(bot, update):
#    """Send a message when the command /start is issued."""
#    update.message.reply_text('Set Timer')

def help(bot, update):
    message = "Hai Selamat datang di Makanin Bot.\n\
    Berikut beberapa commands yang bisa dicoba.\n\
    /berimakan - Untuk memberi makan ikan secara otomatis\n\
    /tambahadmin [username] - Tambah admin\n\
    /hapusadmin [username]- Hapus admin\n\
    /daftaradmin - Melihat semua admin\n\
    /settimer [waktu dalam detik] - Untuk mengatur selisih buka tutup alat selama x detik\n\
    /help - Untuk bantuan\n\
    "
    update.message.reply_text(message)


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("470261273:AAFY_jsb32bKyCAQH0QbQfVfd1jV-ySsz0E")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("berimakan", beriMakan))
    dp.add_handler(CommandHandler("tambahadmin", tambahAdmin, pass_args=True))
    dp.add_handler(CommandHandler("hapusadmin", hapusAdmin, pass_args=True))
    dp.add_handler(CommandHandler("daftaradmin", daftarAdmin))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("settimer", set_timer,
                                  pass_args=True))

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
