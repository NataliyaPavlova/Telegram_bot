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
redis = redis.from_url(os.environ.get("REDIS_URL"))

server = Flask(__name__)

@bot.message_handler(regexp='@WolfLarsen')
def answer_common(message):
    ''' Bot sings pirate songs '''
    bot.send_message(message.chat.id, random.choice(config.silence_words))


@bot.message_handler(func=say_wise)
def answer_common(message):
    ''' Bot replies with quotes from cheer file'''
    text = get_quotes(filename=config.filename1)
    bot.send_message(message.chat.id, text)


@bot.message_handler(func=curse)
def answer_common(message):
    ''' Bot curses down with quoted from curse file'''
    text = get_quotes()
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
    sys.stdout.write('Start working!')
    sys.stdout.write('Uploading to redis...')
    #try:
    #    upload_toredis(config.filename1)
    #    logging.info('{} is successfully uploaded'.format(config.filename1))
    #    upload_toredis(config.filename2)
    #    logging.info('{} is successfully uploaded'.format(config.filename1))

    #except BaseException as err:
    #    logging.error('Fail upload to redis: {}'.format(err))

    server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))

