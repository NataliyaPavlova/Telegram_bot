#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import re
import redis
import os
import sys
import unittest
import config


def get_quotes(filename=config.filename2):
    ''' Return randomly chosen quote from 'cheers' or 'curse' file '''
    try:
        with open(filename) as f:
            sys.stdout.write('Opens the file {} for reading\n'.format(filename))
            quotes_list = list(filter(lambda string: string != '\n', f.readlines()))
            index = random.choice(range(len(quotes_list)))

        return quotes_list[index]
    except Exception as e:
        sys.stdout.write('Fails to opens the file {}\n'.format(filename))
        raise


def check_nots(string, key):
    ''' Return True if there are no negations for wise key word'''
    # split string with , or ; or : or . or !
    parts = re.split("[,;.!]", string)

    # if in part with 'wise'/'curse' words are 'not' words, then false
    for part in parts:
        if key in part:
            for not_word in config.not_words:
                if re.search(not_word, part):
                    if str.find(part, not_word) < str.find(part, key):
                        return False

    return True


def say_wise(message):
    ''' Return True if message contains smart words '''
    sys.stdout.write('Parsing {} in say_wise\n'.format(message.text))
    result1 = False
    result12 = False
    for key in config.wise_words:
        if key in re.split('\W', str(message.text).lower()):
            result1 = True
            break
    if result1:
        result12 = check_nots(str(message.text).lower(), key)

    return bool(result12)


def curse(message):
    ''' Return True if message contains angry words'''
    sys.stdout.write('Parsing {} in curse\n'.format(message.text))
    result = False
    result2 = False
    for key in config.curse_words:
        if key in (re.split('\W', str(message.text).lower())):
            result = True
            break
        # catching 'ffuuuuccckkkk' cases
        if re.search('f+u+c+k+', str(message.text).lower()):
            result = True
    if result:
        result2 = check_nots(str(message.text).lower(), key)
    return bool(result2)


def upload_toredis(filename):
    ''' NOT FINISHED: Upload data from the file to redis'''
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
    sys.stdout.write('{} values from {} file are uploaded\n'.format(len(list_values), filename))


class TestObject():
    ''' Helper: to create analogue of telegram message type for testing utils functions'''
    def __init__(self, string):
        self.text = string


class Test_utils(unittest.TestCase):
    ''' unittests for utils functions '''
    def test_get_qoutes(self):
        self.assertTrue(get_quotes('curse'))
        self.assertTrue(get_quotes('cheer'))

    def test_say_wise(self):
        string1 = 'want to hear smth intelligent please'
        string2 = "don't want smart thoughts"
        string3 = "smart, don't be jerk"

        self.assertEqual(True, say_wise(TestObject(string1)))
        self.assertEqual(False, say_wise(TestObject(string2)))
        self.assertEqual(True, say_wise(TestObject(string3)))


    def test_check_nots(self):
        string1 = 'dont say smth intelligent, please'
        string2 = 'say smth clever, dont be so rude'
        string3 = 'Nietzsche dont be so cool'

        self.assertEqual(False, check_nots(string1, 'intelligent'))
        self.assertEqual(True, check_nots(string2, 'clever'))
        self.assertEqual(True, check_nots(string3, 'Nietzsche'))

    def test_curse(self):
        string1 = 'i am soooo Angry'
        string2 = 'hello'
        string3 = "stop yelling, don't be rude"

        self.assertEqual(True, curse(TestObject(string1)))
        self.assertEqual(False, curse(TestObject(string2)))
        self.assertEqual(False, curse(TestObject(string3)))

if __name__=='__main__':
    unittest.main()

