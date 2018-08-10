#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import telebot
import random
import os
import sys
import config
import redis
#import logging
import datetime
from flask import Flask, request
from utils import get_quotes, say_wise, curse, upload_toredis

token = os.environ.get('TG_TOKEN')
bot = telebot.TeleBot(token)

server = Flask(__name__)

@bot.message_handler(regexp='@WolfLarsen')
def answer_common(message):
    ''' Bot sings pirate songs '''
    sys.stdout.write('Captain is drunk and singing\n')
    text = get_quotes(setname='songs')
    bot.send_message(message.chat.id, text)


@bot.message_handler(func=say_wise)
def answer_common(message):
    ''' Bot replies with quotes from cheer file'''
    sys.stdout.write('Function say_wise returns True on msg {}\n'.format(message.text))
    text = get_quotes(setname='cheer')
    bot.send_message(message.chat.id, text)


@bot.message_handler(func=curse)
def answer_common(message):
    ''' Bot curses down with quoted from curse file'''
    sys.stdout.write('Function curse returns True on msg {}\n'.format(message.text))
    text = get_quotes(setname='curse')
    bot.send_message(message.chat.id, text)


@server.route('/' + token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://nameless-beyond-17722.herokuapp.com/"+token)
    return "?", 200


if __name__ == '__main__':
    random.seed()
    sys.stdout.write('Start working!\n')
    sys.stdout.write('Start uploading to redis...\n')
    file_list = [config.filename1, config.filename2, config.filename3]
    try:
        upload_toredis(file_list)
        sys.stdout.write('Files are successfully uploaded')
    #    upload_toredis(config.filename2)
    #    logging.info('{} is successfully uploaded'.format(config.filename1))

    except Exception as err:
        sys.stdout.write('Fail upload to redis: {}'.format(err))
        raise

    server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))

