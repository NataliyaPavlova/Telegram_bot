#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import telebot
from flask import Flask, request
import config
from utils import get_quotes, say_wise, curse, upload_toredis, upload_songs_toredis

token = os.environ.get('TG_TOKEN')
bot = telebot.TeleBot(token)

server = Flask(__name__)


def data_upload():
    ''' Upload data from files to redis'''
    sys.stdout.write('Start working!\n')
    sys.stdout.write('Start uploading to redis...\n')
    file_list = [config.filename1, config.filename2]
    songs_file = config.filename3
    try:
        if not (upload_toredis(file_list)):
            sys.stdout.write('Fail upload to redis: file not found!\n')
            return False
        if not (upload_songs_toredis(songs_file)):
            sys.stdout.write('Fail upload to redis: file with songs not found!\n')
            return False

    except Exception as err:   #todo handle tg bot exception
        sys.stdout.write('Fail upload to redis: {}'.format(err))
        return False

    return True


@bot.edited_message_handler(regexp='@WolfLarsen')
@bot.message_handler(regexp='@WolfLarsen')
def answer_common(message):
    ''' Bot sings pirate songs '''
    sys.stdout.write('Captain is drunk and singing and it is so True\n')
    text = get_quotes(setname='songs')
    bot.send_message(message.chat.id, text)


@bot.edited_message_handler(func=say_wise)
@bot.message_handler(func=say_wise)
def answer_common(message):
    ''' Bot replies with quotes from cheer file'''
    sys.stdout.write('Function say_wise returns True on msg {}\n'.format(message.text))
    text = get_quotes(setname='cheer')
    bot.send_message(message.chat.id, text)


@bot.edited_message_handler(func=curse)
@bot.message_handler(func=curse)
def answer_common(message):
    ''' Bot curses down with quoted from curse file'''
    sys.stdout.write('Function curse returns True on msg {}\n'.format(message.text))
    text = get_quotes(setname='curse')
    bot.send_message(message.chat.id, text)


@bot.message_handler(func=not(data_upload))
def answer_common(message):
    ''' Bot curses down with quoted from curse file'''
    sys.stdout.write('Fail upload, sending error message to channel\n')
    text = "Go away, Hump, I am shot away and two sheets to the wind."
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
    data_upload()
    server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))

