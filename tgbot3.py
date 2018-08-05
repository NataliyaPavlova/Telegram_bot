#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import telebot
import random
import re
import os
import config
import logging
from flask import Flask, request

bot = telebot.TeleBot(config.token)
server = Flask(__name__)


def get_quotes(filename='curse'):
    ''' Return randomly chosen quote from 'cheers' or 'curse' file '''
    with open(filename) as f:
        quotes_list = list(filter(lambda string: string != '\n', f.readlines()))
        index = random.choice(range(len(quotes_list)))

    return quotes_list[index]


def check_nots(string, key):
    ''' Return True if there are no negations for wise key word'''
    # split string with , or ; or : or . or !
    not_words = ['not', 'n\'t', 'stop', 'cease', 'wind down', 'off', 'halt', 'shut down', 'dont']
    parts = re.split("\W ", string)
    print(parts)
    # if in part with 'wise' words are 'not' words, then false
    for part in parts:
        if key in part:
            for not_word in not_words:
                if re.search(not_word, part):
                    print(part, not_word)
                    return False
            break
    return True


def say_wise(message):
    ''' Return True if message contains smart words and is addressed to @WolfLarsenbot'''
    key_words = ['wise', 'wisdom', 'smart', 'clever', 'intelligent', 'sophisticated', 'sensible']
    result1 = False
    result12 = False
    for key in key_words:
        if bool(re.search(key, str(message.text).lower())):
            result1 = True
            break
    if result1:
        result12 = check_nots(str(message.text).lower())
    result2 = bool(re.search('@WolfLarsenbot', str(message.text)))
    return bool(result12 and result2)


def curse(message):
    ''' Return True if message contains angry words'''
    key_words = ['angry', 'fuck', 'wtf', 'furious', 'evil', 'grumpy', 'yelling', 'kill']
    result = False
    for key in key_words:
        if bool(re.search(key, str(message.text).lower())):
            result = True
            break
    return bool(result)


@bot.message_handler(func=say_wise)
def answer_common(message):
    ''' Bot replies with quotes from cheer file'''
    text = get_quotes(filename='cheer')
    bot.send_message(message.chat.id, text)


@bot.message_handler(func=curse)
def answer_common(message):
    ''' Bot curses down with quoted from curse file'''
    text = get_quotes()
    bot.send_message(message.chat.id, text)


@bot.message_handler(regexp='@WolfLarsen')
def answer_common(message):
    ''' Bot curses down with quoted from curse file'''
    text = 'Who knows - does not say. Who says - does not know'
    bot.send_message(message.chat.id, text)


@server.route('/' + config.token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://nameless-beyond-17722.herokuapp.com/"+config.token) 
    return "?", 200

if __name__ == '__main__':
    random.seed()
    server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))

