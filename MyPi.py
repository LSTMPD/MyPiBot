from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from subprocess import PIPE, Popen
import socket
import os
import logging

def getCPUtemperature(bot, update):
    res = os.popen('vcgencmd measure_temp').readline()
    bot.send_message(chat_id=update.message.chat_id, text=(res.replace("temp=","").replace("'C\n","")))


def get_private_ip(bot, update):
    """
    Gets private IP address of this machine.

    Returns:
        private IP address
    """
    ip = socket.gethostbyname(socket.gethostname())
    bot.send_message(chat_id=update.message.chat_id, text="Your Pi's local IP is:" + "\n" + ip)

"""
def ping(bot, update):
    _,target = update.message.text.split(" ")
    update.message.reply_text((subprocess.check_output(["ping", target]).decode("UTF-8")).replace("\r\n", ""))
"""
def running_services(bot,update):
    update.message.reply_text(os.system('service --status-all | grep " + "'))


def updatelist(bot, update):
    os.system("sudo apt update -y")
    bot.send_message(chat_id=update.message.chat_id, text="List update requested!")

def upgrading(bot, update):
    os.system("sudo apt upgrade -y")
    bot.send_message(chat_id=update.message.chat_id, text="Upgrade requested!")

def distupgrade(bot, update):
    os.system("sudo apt dist-upgrade -y")
    bot.send_message(chat_id=update.message.chat_id, text="Dist-upgrade requested!")

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    updater = Updater("TOKEN")

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("ip", get_private_ip))
    dp.add_handler(CommandHandler("temp", getCPUtemperature))
    #dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ping", ping))
    dp.add_handler(CommandHandler("distupgrade", distupgrade))
    dp.add_handler(CommandHandler("updatelist", updatelist))
    dp.add_handler(CommandHandler("services", running_services))
    #dp.add_handler(CommandHandler("reboot", reboot))
    #dp.add_handler(CommandHandler("shutdown", shutdown))
    #dp.add_handler(CommandHandler("pproc", pproc))
    dp.add_error_handler(error)
    dp.add_handler(CommandHandler("upgrade", upgrading))
    #dp.add_handler(CommandHandler("rename", rename))
    updater.start_polling()

    updater.idle()




if __name__ == '__main__':
    main()
