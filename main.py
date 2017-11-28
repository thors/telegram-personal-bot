# -*- coding: utf-8 -*-
from telegram.ext import Updater
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ParseMode
import codecs
import logging, re, os


config={}
updater=None

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hi, I'm " + config['bot_name'] + ". Just ignore me for now...")

def get_random_file_content(category='fortune', language='en', args):
    print "todo"
    
def kfz(bot, update, args):
    kfz1Re=re.compile("^([^,]+),([^,]+)$")
    kfz2Re=re.compile("^([^,]+),([^,]+),(.*)$")
    with codecs.open("data/kennzeichen/de/all.csv","r","utf8") as kfzfile:
        for l in kfzfile:
            l = l.strip("\n")
            m=kfz1Re.match(l)
            if m != None:
                if ''.join(args).upper() == m.group(1):
                    bot.send_message(chat_id=update.message.chat_id, text=m.group(1) + ": " + m.group(2))
                    break
                continue
            m=kfz2Re.match(l)
            if m != None:
                if ''.join(args).upper() == m.group(1):
                    bot.send_message(chat_id=update.message.chat_id, text=m.group(1) + ": " + m.group(2) + ", " + m.group(3))
                    break
                continue
            print l
    
def my_help(bot, update, args):
	try:
	    filename = os.path.join("data/help/", config.get('languagede','en'), "help_" + ''.join(args) + ".html")
	    if not os.path.exists(filename):
	        filename = os.path.join("data/help/", config.get('languagede','en'), "help.html")
	    
	    if os.path.exists(filename):
	        with codecs.open(os.path.join("data/help/", config.get('languagede','en'), "help.html"),"r","utf8") as helpfile:
	            bot.send_message(chat_id=update.message.chat_id, text= ''.join(helpfile.read()), parse_mode=ParseMode.HTML)
	    else:
	        bot.send_message(chat_id=update.message.chat_id, text='No help availabe for ' + config.get('languagede','en') + " language")
	except Exception as e:
		print e

def fortune(bot, update, args):
    bot.send_message(chat_id=update.message.chat_id, text='Fortune... Not yet available, ToDo')
	
def language(bot, update, args):
    bot.send_message(chat_id=update.message.chat_id, text='Todo')

def my_exit(bot, update, args):
    bot.send_message(chat_id=update.message.chat_id, text='Todo')
    print "Exit not working..."
    #updater.stop()
    #exit(1)

def main():
    global updater
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

    propertyRe=re.compile("^([^=]+)=(.*)$")
    with open("/etc/telegram/botconfig","r") as botconfig:
        for l in botconfig:
            l = l.strip("\n")
            m = propertyRe.match(l)
            if m != None:
                config[m.group(1)]=m.group(2)

    updater = Updater(token=config['bot_token'])
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    kfz_handler = CommandHandler('kfz', kfz, pass_args=True)
    language_handler = CommandHandler('language', kfz, pass_args=True)
    help_handler = CommandHandler('help', my_help, pass_args=True)
    exit_handler = CommandHandler('exit', my_exit, pass_args=True)
    fortune_handler = CommandHandler('fortune', fortune, pass_args=True)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(kfz_handler)   
    dispatcher.add_handler(exit_handler)
    dispatcher.add_handler(help_handler)
    updater.start_polling()
    updater.idle() 
    
main()
