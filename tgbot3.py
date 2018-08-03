# -*- coding: utf-8 -*-
import telebot
import random
import re
import config

bot = telebot.AsyncTeleBot(config.token)


def get_quotes(filename='curse'):
    ''' Return randomly chosen quote from 'cheers' or 'curse' file '''
    with open(filename) as f:
        quotes_list = list(filter(lambda string: string != '\n', f.readlines()))
        index = random.choice(range(len(quotes_list)))

    return quotes_list[index]


def say_wise(message):
    ''' Return True if message contains smart words and is addressed to @WolfLarsenbot'''
    key_words = ['wise', 'wisdom', 'smart', 'clever', 'intelligent', 'sophisticated', 'sensible']
    result1 = False
    for key in key_words:
        if re.search(key, message.text):
            result1 = True
            break
    result2 = re.search('@WolfLarsenbot', message.text)
    return (result1 and result2)


@bot.message_handler(func=say_wise)
def answer_common(message):
    ''' Bot replies with quotes from cheer file'''
    text = get_quotes(filename='cheer')
    bot.reply_to(message, text)


@bot.message_handler(regexp='@WolfLarsenbot')
def answer_common(message):
    ''' Bot curses down with quoted from curse file'''
    text = get_quotes()
    bot.reply_to(message, text)


if __name__ == '__main__':

     random.seed()
     bot.polling(none_stop=True)