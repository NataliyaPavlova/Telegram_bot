#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import re
import os
import sys
import unittest
import redis
import config

r = redis.from_url(os.environ.get("REDIS_URL"), decode_responses=True)


def get_quotes(setname):
    ''' Return randomly chosen quote from 'cheers' or 'curse' file '''
    try:
       sys.stdout.write('Looking for a random expression from {} set\n'.format(setname))
       key = r.srandmember(setname)
       result = r.get(key)
       sys.stdout.write('Found an expression from {} set: {}\n'.format(setname, result))
       return result
    except Exception as e:
        sys.stdout.write('Fail to get an expression from {} set\n'.format(setname))
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


def upload_songs_toredis(filename):
    ''' Upload data from file with songs to redis'''

    # redis stores key-value: id-text

    if not os.path.isfile(filename):
        sys.stdout.write('Fail upload to {}\n'.format(filename))
        return 0
    else:
        setname = filename
        song = ''
        key_index = 0
        # Read values from the file into the list
        with open(filename) as f:
            for line in f:
                if line=='*\n':
                    # it means the song is over and we save song to redis
                    key = '{}.{}:'.format(setname, key_index)  # curse.0:, curse.1:, ... or cheer.0:, cheer.1:, ...
                    r.sadd(setname, key)
                    r.set(key, song)
                    song = ''
                    key_index += 1
                else:
                    song = song + line

    sys.stdout.write('{} values from {} file are successfully uploaded\n'.format(r.scard(setname), filename))
    return 1


def upload_toredis(file_list):
    ''' Upload data from files with curse and cheer expressions to redis'''
    # redis stores key-value: id-text

    # Delete old sets
    r.flushall()

    # for each file do upload to redis
    for filename in file_list:

        if not os.path.isfile(filename):
            sys.stdout.write('Fail upload to {}\n'.format(filename))
            return 0
        else:
            setname = filename

            # Read values from the file into the list
            with open(filename) as f:
                list_values = list(filter(lambda string: string != '\n', f.readlines()))
                # Upload new set
                i = 0
                for val in list_values:
                    key = '{}.{}:'.format(setname, i)  # curse.0:, curse.1:, ... or cheer.0:, cheer.1:, ...
                    i += 1
                    r.sadd(setname, key)
                    r.set(key, val)
                sys.stdout.write('{} values from {} file are successfully uploaded\n'.format(r.scard(setname), filename))
    return 1


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
        elif not (upload_songs_toredis(songs_file)):
            sys.stdout.write('Fail upload to redis: file with songs not found!\n')
            return False

    except Exception as err:
        sys.stdout.write('Fail upload to redis: {}'.format(err))
        return False

    return True


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

