import random
import re
import config

def get_quotes(filename='curse'):
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
    ''' Return True if message contains smart words and is addressed to @WolfLarsenbot'''
    result1 = False
    result12 = False
    for key in config.wise_words:
        if bool(re.search(key, str(message.text).lower())):
            result1 = True
            break
    if result1:
        result12 = check_nots(str(message.text).lower(), key)
    result2 = bool(re.search('@wolflarsenbot', str(message.text).lower()))
    return bool(result12 and result2)


def curse(message):
    ''' Return True if message contains angry words'''
    result = False
    result2 = False
    for key in config.curse_words:
        if bool(re.search(key, str(message.text).lower())):
            result = True
            break
        # catching 'fuuuuccckkkk' cases
        if re.search('f+u+c+k+', str(message.text).lower()):
            result = True
    if result:
        result2 = check_nots(str(message.text).lower(), key)
    return bool(result2)

