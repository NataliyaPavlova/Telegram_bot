#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import telebot
from flask import Flask, request
import config
import utils

token = os.environ.get('TG_TOKEN')
bot = telebot.TeleBot(token)

server = Flask(__name__)


@bot.edited_message_handler(commands=['start'])
@bot.message_handler(commands=['start'])
def answer_common(message):
    ''' Bot welcomes '''
    try:
        sys.stdout.write('Sending welcome instructions...\n')
        bot.send_message(message.chat.id, config.start_text)
    except Exception as e:
        sys.stdout.write('Failure {}, sending error message to channel\n'.format(e))
        bot.send_message(message.chat.id, config.error_text)
        raise e


@bot.edited_message_handler(commands=['help'])
@bot.message_handler(commands=['help'])
def answer_common(message):
    ''' Bot answer for /help command '''
    try:
        sys.stdout.write('Sending help instructions...\n')
        bot.send_message(message.chat.id, config.help_text)
    except Exception as e:
        sys.stdout.write('Failure {}, sending error message to channel...\n'.format(e))
        bot.send_message(message.chat.id, config.error_text)
        raise e


@bot.edited_message_handler(commands=['spell'])
@bot.message_handler(commands=['spell'])
def answer_common(message):
    ''' Bot answer for /spell command '''
    try:
        sys.stdout.write('Spelling with nautical flags...\n')
        bot.send_message(message.chat.id, utils.spell(message))
    except Exception as e:
        sys.stdout.write('Failure spelling: {}, sending error message to channel...\n'.format(e))
        bot.send_message(message.chat.id, config.error_text)
        raise e


@bot.edited_message_handler(regexp='WolfLarsen')
@bot.message_handler(regexp='WolfLarsen')
def answer_common(message):
    ''' Bot sings pirate songs '''
    try:
        sys.stdout.write('Captain is drunk and singing and it is so True\n')
        text = utils.get_quotes(setname='songs')
        bot.send_message(message.chat.id, text)
    except Exception as e:
        sys.stdout.write('Failure {}, sending error message to channel...\n'.format(e))
        bot.send_message(message.chat.id, config.error_text)
        raise e


@bot.edited_message_handler(func=utils.say_wise)
@bot.message_handler(func=utils.say_wise)
def answer_common(message):
    ''' Bot replies with quotes from cheer file'''
    try:
        sys.stdout.write('Function say_wise returns True on msg {}\n'.format(message.text))
        text = utils.get_quotes(setname='cheer')
        bot.send_message(message.chat.id, text)
    except Exception as e:
        sys.stdout.write('Failure {}, sending error message to channel...\n'.format(e))
        bot.send_message(message.chat.id, config.error_text)
        raise e


@bot.edited_message_handler(func=utils.curse)
@bot.message_handler(func=utils.curse)
def answer_common(message):
    ''' Bot curses down with quoted from curse file'''
    try:
        sys.stdout.write('Function curse returns True on msg {}\n'.format(message.text))
        text = utils.get_quotes(setname='curse')
        bot.send_message(message.chat.id, text)
    except Exception as e:
        sys.stdout.write('Failure {}, sending error message to channel...\n'.format(e))
        bot.send_message(message.chat.id, config.error_text)
        raise e


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
    utils.data_upload()
    server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))

