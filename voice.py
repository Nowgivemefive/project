import os
import simpleaudio
import argparse
from nltk.corpus import cmudict as cmt
import re
import numpy as np

### NOTE: DO NOT CHANGE ANY OF THE EXISTING ARGUMENTS
parser = argparse.ArgumentParser(
    description='A basic text-to-speech app that synthesises an input phrase using monophone unit selection.')
parser.add_argument('--monophones', default="monophones", help="Folder containing monophone wavs")
parser.add_argument('--play', '-p', action="store_true", default=False, help="Play the output audio")
parser.add_argument('--outfile', '-o', action="store", dest="outfile", type=str, help="Save the output audio to a file",
                    default=None)
parser.add_argument('phrase', nargs=1, help="The phrase to be synthesised")

# Arguments for extensions
parser.add_argument('--spell', '-s', action="store_true", default=False,
                    help="Spell the phrase instead of pronouncing it")
parser.add_argument('--volume', '-v', default=None, type=float,
                    help="A float between 0.0 and 1.0 representing the desired volume")

args = parser.parse_args()

#print(args.monophones)


class Synth(object):
    def __init__(self, wav_folder):
        self.phones = {}
        self.vol = 0.2
        self.get_wavs(wav_folder)
        self.res_voice = simpleaudio.Audio()

    def get_wavs(self, wav_folder):
        for root, dirs, files in os.walk(wav_folder, topdown=False):
            if(len(files)==0):
                print('Current path not correct!')
                exit()
            for file in files:
                self.phones[file.split('.')[0].upper()] = '{0}\\{1}'.format(root,file)
                pass  # delete this line and implement


    """Extension A – Volume Control"""

    def set_volume(self,vol):
        self.vol = vol

    def get_letters_voice(self, letter_phone_list):
        letter_voice_audio = simpleaudio.Audio()
        for letter in letter_phone_list:
            if re.match('[A-Z]{1,2}[1]',letter):
                letter = letter[:-1]
            temp = simpleaudio.Audio()
            temp.load(self.phones[letter])
            letter_voice_audio.data = np.append(letter_voice_audio.data,temp.data)
        letter_voice_audio.change_speed(0.4)
        letter_voice_audio.rescale(self.vol)
        letter_voice_audio.play()
        
    def get_words_voice(self,word_phone_list):
        upper_letters = list('QWERTYUIOPASDFGHJKLZXCVBNM')
        voice_upper =  False


        """Extension B – Punctuation
        contains a comma – insert 250ms of silence
        period, question mark or exclamation mark – insert 500ms of silence"""


        for w_index in range(0,len(word_phone_list)):
            #print(word_phone_list[w_index])
            if word_phone_list[w_index] in list(',.!?'):
                if word_phone_list[w_index] == ',':
                    temp = simpleaudio.Audio(rate=16000)
                    temp.create_tone(0, int(0.25 * temp.rate), 0)
                    #print(temp.data)
                    self.res_voice.data = np.append(self.res_voice.data,temp.data)
                    continue
                else:
                    temp = simpleaudio.Audio(rate=16000)
                    temp.create_tone(0, int(0.5 * temp.rate), 0)
                    #print(temp.data)
                    self.res_voice.data = np.append(self.res_voice.data,temp.data)
                    continue
            if  word_phone_list[w_index] in list('{}'):
                continue
            #print(word_phone_list[w_index-1])
            for index in range(0,len(word_phone_list[w_index])):
            #for phone_item in word_phone_list[w_index]:
                phone_key =  ''
                for phone_item_lower_item in word_phone_list[w_index][index]:                                            #不懂？？
                    if phone_item_lower_item in upper_letters:
                        phone_key += phone_item_lower_item


                """ Extension D – Emphasis markup  
                     emphasis the word in{} """


                temp = simpleaudio.Audio()
                temp.load(self.phones[phone_key])
                if w_index > 0 and word_phone_list[w_index-1] == '{':
                    voice_upper = True
                if index == (len(word_phone_list[w_index])-1) :
                    voice_upper = False
                if voice_upper:
                    temp.data = temp.data * 5
                    #pass#temp.rescale(1)
                else:
                    pass
                    #pass#temp.rescale(self.vol)
                self.res_voice.data = np.append(self.res_voice.data,temp.data)
           
    def play_the_voice(self):
        self.res_voice.change_speed(0.4)
        self.res_voice.rescale(self.vol)
        self.res_voice.play()
        
    def save_to_file(self,outfile):
        self.res_voice.save(outfile)
        print('Saved')


    """Extension E – Text Normalisation for Numbers
       normalise numbers from 0 up to at least 999"""


before_twenty_dict = {0:"zero", 1:"one", 2:"two", 3:"three", 4:"four", 5:"five", 6:"six", 7:"seven",
                8:"eight", 9:"nine", 10:"ten", 11:"eleven", 12:"twelve", 13:"thirteen",
                14:"fourteen", 15:"fifteen", 16:"sixteen", 17:"seventeen", 18:"eighteen", 19:"nineteen" }
digital_ten_dict = {2:"twenty", 3:"thirty", 4:"forty", 5:"fifty", 6:"sixty", 7:"seventy", 8:"eighty", 9:"ninety"}


def num_to_word(number):                                                                                                         #不是类里的方法了吗？
    number = str(number)
    if int(number) < 20:
        return before_twenty_dict[int(number)]
    # 20 - 99
    if len(number) == 2 and int(number) % 10 == 0:
        return digital_ten_dict[int(number[0])]
    elif len(number) == 2:
        res = digital_ten_dict[int(number[0])] + ' ' + before_twenty_dict[int(number[1])]
        return res
    # 100-999
    if len(number) == 3 and int(number) % 100 == 0:
        return before_twenty_dict[int(number[0])] + ' hundred'
    elif len(number) == 3 and int(number[1]) == 0:
        return before_twenty_dict[int(number[0])] + ' hundred and ' + before_twenty_dict[int(number[2])]
    elif len(number) == 3 and int(number[1]) == 1:
        return before_twenty_dict[int(number[0])] + ' hundred and ' + before_twenty_dict[
            int(number[2]) + 10 * int(number[1])]
    elif len(number) == 3:
        return before_twenty_dict[int(number[0])] + ' hundred and ' + digital_ten_dict[int(number[1])] + ' ' + \
               before_twenty_dict[int(number[2])]


month_dict = {'01': 'january', '02': 'february', '03': 'march', '04': 'april', '05': 'may', '06': 'june', '07': 'july',
              '08': 'august', '09': 'september', '10': 'october', '11': 'november', '12': 'december'}

day_dict = {'1':'frist','2':'second','3':'third','4':'fouth','5':'fifth','6':'sixth',
            '7':'seventh','8':'eighth','9':'ninth', '01': 'frist', '02': 'second', '03': 'third', '04': 'fouth', '05': 'fifth', '06': 'sixth',
            '07': 'seventh', '08': 'eighth', '09': 'ninth', '10': 'tenth', '11': 'eleventh', '12': 'twelfth',
            '13': 'thirteenth', '14': 'fourteenth', '15': 'fifteenth', '16': 'sixteenth', '17': 'seventeenth',
            '18': 'eighteenth', '19': 'nineteenth', '20': 'twentieth', '21': 'twenty first', '22': 'twenty scond', '23': 'twenty third',
            '24': 'twenty fouth', '25': 'twenty fifth', '26': 'twenty sixth', '27': 'twenty seventh', '28': 'twenty eighth',
            '29': 'twenty ninth', '30': 'thirty', '31': 'thirty first'}


def date_to_word(date_str):
    date_list = date_str.split('/')
    # print(date_list)
    if len(date_list) == 2:
        return 'the ' + day_dict[date_list[0]] + ' of ' + month_dict[date_list[1]]
    if len(date_list) == 3 and len(date_list[2]) == 2:
        return 'the ' + day_dict[date_list[0]] + ' of ' + month_dict[date_list[1]] + ' nineteen ' + num_to_word(
            int(date_list[2]))
    if len(date_list) == 3 and len(date_list[2]) == 4:
        return 'the ' + day_dict[date_list[0]] + ' of ' + month_dict[date_list[1]] + ' ' + num_to_word(
            int(date_list[2][:2])) + ' ' + num_to_word(int(date_list[2][2:]))


def process_pounc(phrase):
    """normalise the text (convert to lower/upper case, remove all punctuation, expect ,.?!{},which are used in task2)
    """
    letters = list('qwertyuiopasdfghjklzxcvbnm0123456789 ')
    phrase = phrase.lower()
    after_phrase = ''
    for phrase_item in phrase:
        if phrase_item in letters:
            after_phrase += phrase_item
        elif phrase_item in list(',!.}'):
            temp = ' ' + phrase_item
            after_phrase += temp
        elif phrase_item == '{':
            temp = phrase_item + ' '
            after_phrase += temp
        elif phrase_item == '/':
            after_phrase += phrase_item
        else:
            after_phrase += ' '
    after_phrase = after_phrase.replace('  ', ' ')
    return after_phrase

'''convert number and date to words'''
def process_num(phrase):
    before_str = phrase
    before_str_list = before_str.split(' ')
    for index in range(0, len(before_str_list)):
        if re.match('[0-9]{1,3}$', before_str_list[index]):
            before_str_list[index] = num_to_word(int(before_str_list[index]))
        if re.match('\.[0-9]+$', before_str_list[index]):
            temp = before_str_list[index].strip('.')
            after_point = ''
            for temp_item in temp:
                after_point += ' ' + num_to_word(temp_item)
            before_str_list[index] = 'point' + after_point                                                                     #不懂???
        if re.match('([0-9]{1,2}/[0-9]{1,2})|([0-9]{1,2}/[0-9]{1,2}/[0-9]{1,2})|([0-9]{1,2}/[0-9]{1,2}/[0-9]{1,4})',
                    before_str_list[index]):
            before_str_list[index] = date_to_word(before_str_list[index])
    before_str = ''
    for before_str_list_item in before_str_list:
        before_str += ' ' + before_str_list_item
    return before_str

"""Extension C – Spelling
       pronounce for each letter in its alphabetic form"""
def get_phone_list(phrase):
     # get a word phone seq
    after_phrase = phrase
    entries = cmt.entries()
    word_phone_list = []
    for word in after_phrase.strip(' ').split(' '):                                                                             #strip把空格去掉，怎么根据空格split?  这里是实现的spelling吗？
        if word == ' ':
            continue
        throw_error = True
        if word in list(',.!?{}'):
            word_phone_list.append(word)
            throw_error = False
            continue
        for entries_item in entries:
            if word == entries_item[0]:
                word_phone_list.append(entries_item[1])
                throw_error = False
                break
        if throw_error:
            print('this: error {0}'.format(word))
            exit()
    return word_phone_list

def processPhrase(phrase):
    before_str = process_pounc(phrase)
    
    after_phrase = process_num(before_str)
    return after_phrase
def get_phone_seq(phrase):
    after_phrase = processPhrase(phrase)
    print(after_phrase.strip(' '))
    # return after_phrase
    return get_phone_list(after_phrase)

def getLetterPoun(phrase):
    letter_list =[]
    after_phrase = processPhrase(phrase)
    for letter in after_phrase:
        if re.match('[a-z]',letter):
            letter_list.append(letter)
    entries = cmt.entries()
    letter_phone_list =[]
    #print(letter_list)
    for letter in letter_list:
        for entries_item in entries:
            if letter == entries_item[0]:
                letter_phone_list.append(entries_item[1][0])
                break
    return letter_phone_list
    
if __name__ == "__main__":
    S = Synth(wav_folder=args.monophones)
    phone_seq = get_phone_seq(args.phrase[0])    #args.phrase[0]?   phone_seq是放的音标？
    if args.volume != None:
        S.set_volume(args.volume)
    if args.spell:
        letter_phone_list = getLetterPoun(args.phrase[0])
        print(letter_phone_list)
        S.get_letters_voice(letter_phone_list)
    else:
        S.get_words_voice(phone_seq)                                                                                             #实现声音大小？？？

        S.play_the_voice()
        if args.outfile != None:
            S.save_to_file(args.outfile)

    #'''
    
    
    # out is the Audio object which will become your output
    # you need to modify out.data to produce the correct synthesis
    #out = simpleaudio.Audio(rate=16000)
    #print(out.data, type(out.data))


