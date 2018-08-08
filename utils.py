#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import re
import redis
import os
import config

def get_quotes(filename=config.filename2):
    ''' Return randomly chosen quote from 'cheers' or 'curse' file '''
    with open(filename) as f:
        quotes_list = list(filter(lambda string: string != '\n', f.readlines()))
        index = random.choice(range(len(quotes_list)))

    return quotes_list[index]


def check_nots(string, key):
    ''' Return True if there are no negations for wise key word'''
    # split string with , or ; or : or . or !
    parts = re.split("\W ", string)

    # if in part with 'wise' words are 'not' words, then false
    for part in parts:
        if key in part:
            for not_word in config.not_words:
                if re.search(not_word, part):
                    return False

    return True


def say_wise(message):
    ''' Return True if message contains smart words '''
    result1 = False
    result12 = False
    for key in config.wise_words:
        if bool(re.search(key, str(message.text).lower())):
            result1 = True
            break
    if result1:
        result12 = check_nots(str(message.text).lower(), key)

    return bool(result12)


def curse(message):
    ''' Return True if message contains angry words'''
    result = False
    result2 = False
    for key in config.curse_words:
        if bool(re.search(key, str(message.text).lower())):
            result = True
            break
        # catching 'ffuuuuccckkkk' cases
        if re.search('f+u+c+k+', str(message.text).lower()):
            result = True
    if result:
        result2 = check_nots(str(message.text).lower(), key)
    return bool(result2)

def upload_toredis(filename):
    ''' Upload data from the file to redis'''
    # redis stores key-value: id-text
    if not os.path.isfile(filename):
        list_values=[]
        filename=''
    else:
        setname = filename

        # Read values from the file into the list
        with open(filename) as f:
            list_values = list(filter(lambda string: string != '\n', f.readlines()))

    # Delete old set
    redis.delete(setname)

    # Upload new set
    i = 0
    for val in list_values:
        key = '{}.{}:'.format(setname, i)   # curse.0:, curse.1:, ... or cheer.0:, cheer.1:, ...
        i+=1
        redis.sadd(setname, key)
        redis.set(key, val)


