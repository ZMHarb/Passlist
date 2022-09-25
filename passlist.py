#!/bin/python3 

import os, time
from datetime import datetime
from threading import Timer, Thread
from argparse import ArgumentParser, RawTextHelpFormatter, SUPPRESS

from itertools import product
from collections import OrderedDict

from colorama import Fore


banner = '''

██████╗  █████╗  ██████╗ ██████╗██╗     ██╗ ██████╗████████╗
██╔══██╗██╔══██╗██╔════╝██╔════╝██║     ██║██╔════╝╚══██╔══╝
██████╔╝███████║╚█████╗ ╚█████╗ ██║     ██║╚█████╗    ██║
██╔═══╝ ██╔══██║ ╚═══██╗ ╚═══██╗██║     ██║ ╚═══██╗   ██║
██║     ██║  ██║██████╔╝██████╔╝███████╗██║██████╔╝   ██║
╚═╝     ╚═╝  ╚═╝╚═════╝ ╚═════╝ ╚══════╝╚═╝╚═════╝    ╚═╝

* Powerful wordlist Generator
* Created by ZMHarb
* Project https://github.com/ZMHarb/passlist.git
_______________________________________________________________
'''


CHARS = ["", " ", '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', 
    '>', '?', '@', '[', "\\", ']', '^', '_', '`', '{', '|', '}', '~']

DICTO = {'a':("@", "A", '4'), 'b': 'B', 'c': ('C', '('), 'd': 'D', 'e': ('E', '3'), 'f': 'F', 'g': 'G', 'h': 'H', 'i': 'I',
    'j': 'J', 'k': 'J', 'l': 'L', 'm': 'M', 'n': 'N', 'o': ("O", "0"), 'p': 'P', 'q': 'Q', 'r': 'R',
    's': ("S", "5", "$"), 't': 'T', 'u': ('U','v'), 'v': ('V','u'), 'w': ('W', 'vv'), 'x': 'X', 'y': 'Y', 'z': 'Z'}

EXAMPLES = '''
        
Examples:
---------

>> ./passlist.py -p 1 -f john -l smith
johnsm
johnsm
johnsmi
...
smithjohn
smithjoh
...

>> ./passlist.py -p 2 -f john -l smith -d 1 1 1990
...
j0hnsmith111990
1990Johnsmith
...
J0hnsmith1990
...

>> ./passlist.py -p 3 -f john -l smith
...
J0hn Smith
J0hn-Smith
Smith*john
...

'''
# Used with verbosity On
LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'

#time of the program's start
START = datetime.now()

def difference():
    '''
    Returns the duration of time needed for the program to be executed.
    '''
    stop = datetime.now()
    seconds = (stop - START).total_seconds() 
    hours = round(seconds // 3600)
    minutes = round((seconds // 60) % 60)
    return "{} {} {}".format(
        str(hours) + (" hour and" if hours == 1 else " hours and") if hours else "",
        str(minutes) + (" minute and" if minutes == 1 else " minutes and") if minutes else "",
        str(round(seconds - (minutes * 60), ndigits=2)) + (' second' if seconds <= 1 else ' seconds ')
        )

def format_size(size):
    
    if size < 1000000:
        return "{} KB".format(round(size / 1000, ndigits=3))
    
    elif size >= 1000000 and size < 1000000000:
        return "{} MB".format(round(size / 1000000, ndigits=3))
    
    else:
        return "{} GB".format(round(size / 1000000000, ndigits=3))

def verbose_function(filename):
    '''
    To be more verbosity

    :param filename: the name of the output file
    '''
    try:
        size = os.stat(filename).st_size
        # print(f"Verbosity: {Fore.GREEN}ON{Fore.RESET}")
        print(f"Wordlist Size: {format_size(size)}")
        print(f"Time Taken: {difference()}")

        # To print on the same lines each time
        print(LINE_UP, end=LINE_CLEAR)
        print(LINE_UP, end=LINE_CLEAR)

        timer = Timer(3, verbose_function, args=(filename,))
        timer.daemon = True
        timer.start()

    except FileNotFoundError:
        verbose_function(filename)
        pass                
    
class Passlist:
    '''

    Passlist class used to generate the wordlist
    '''

    def __init__(self, filename, phase, first=None, last=None, date=None):
        
        #initializing the class variables
        self.phase = phase
        self.first = first
        self.last = last
        self.date = date
        self.output = filename
        self.nbr_passwords = 0
            
    def __decompose_word(self, word):
        '''
        Decomposes a given word according to the phase.
        eg. john --> ['j', 'jo', 'joh', 'john', ...]

        :param word: the word to decompose
        
        :returns: list of decomposed words
        '''
        try:        
            #If the given parameter is the 'date', its type will be a 'list'
            if type(word) == list:    
                
                list_to_return = [
                        str(word[0]), str(word[1]), str(word[2]), # separates the day, month, year 
                        str(word[0]) + str(word[1]), str(word[1]) + str(word[0]), # day & month 
                        str(word[1]) + str(word[2]), str(word[2]) + str(word[1]), # month & year
                        str(word[0]) + str(word[2]), str(word[2]) + str(word[0]), # day & year
                        "".join(map(str, word[:])),   # day month year
                        ]
                
                # If we are in phase 3, we want to add the characters after each word
                if self.phase == 3:
                    
                    list_to_return = []
                    for char in CHARS:
                    
                        liste = [
                        
                        str(word[0]) + char, # day + char (eg. 22/)
                        str(word[1]) + char, # month + char
                        str(word[2]) + char, #year + char
                        str(word[0]) + str(word[1]) + char, str(word[1]) + str(word[0]) + char, # day + month + char 
                        str(word[1]) + str(word[2]) + char, str(word[2]) + str(word[1]) + char, # month + year + char
                        str(word[0]) + str(word[2]) + char, str(word[2]) + str(word[0]) + char, # day + year + char

                        str(word[0]) + char + str(word[1]), str(word[1]) + char + str(word[0]), # day + char + month 
                        str(word[1]) + char + str(word[2]), str(word[2]) + char + str(word[1]), # month + char + year
                        str(word[0]) + char + str(word[2]), str(word[2]) + char + str(word[0]), # day + char + year
                        
                        char + str(word[0]) + str(word[1]), char + str(word[1]) + str(word[0]), # char + day + month
                        char + str(word[1]) + str(word[2]), char + str(word[2]) + str(word[1]), # char + month + year
                        char + str(word[0]) + str(word[2]), char + str(word[2]) + str(word[0]), # char + day + year
                        
                        char.join(map(str, word[:])),   # day + char + month + char + year (eg. 1/1/1992)

                        ]

                        list_to_return.extend(liste)    

                return list_to_return

            else:
                #The prefix of each letter (eg. john --> ['j', 'jo', 'joh', 'john'])
                list_to_return = [word[:i] for i in range(1, len(word)+1)]
                
                #In phase 3,the list will contains the decomposed word + char
                if self.phase == 3:
                    list_to_return = []
                    for char in CHARS:
                            list_to_return.extend(word[:i] + char for i in range(1, len(word)+1))

            return list_to_return

        #if we don't provide a category by argument, it will be None, so when parsing the word, we'll get a TypeError Exception
        except TypeError:
            return []

    def __split_word(self, word):
        '''
        Split the word letter by letter

        :param word: the string to split

        :returns: a list of word's letters
        '''
        if word:    
            return list(word)
        else:
            return []

    def __find_words(self, word):
        '''
        Substitutes each letter by its corresponding specific characters, defined in DICTO

        :param word: a string to substitute its letters

        :returns: a list containing all possible substitutions of a word
        '''
        #We will split the word by letters
        letters = self.__split_word(word)
        liste = []
        try:
            for letter in letters:
                for sub in DICTO[letter]:
                    #if a letter exists one time in a string, we will replace it directly
                    if word.count(letter) == 1:
                        word1 = word.replace(letter, sub)
                        liste.append(word1)

                    #if a letter exists multiple time in a string, we will replace each letter seperately
                    else:
                        #we will get the index of each repetition of letter
                        letter_index = [z[0] for z in list(enumerate(list(word))) if z[1] == letter]
                        for index in letter_index:
                            word2 = word
                            word_list = self.__split_word(word2)
                        
                            #We will remove each repetition of letter seperately by index the replacing it by its substitution
                            word_list.pop(index)
                            word_list.insert(index, sub)

                            liste.append("".join(word_list))
        # When using this function to find substitutions in a string already substituted, the letter could be a character substitued
        # So DICTO[letter] will not be defined
        except KeyError:
            pass


        return liste
    
    def __all_subs(self, name):
        '''
        Function that makes sure that all the words are substituted. Even if a string is already substituted
        
        :param name: word to check its letters

        :returns: list with all the name's substitutions 
        '''

        try:
            all_words = [name]
            nbr = len(name) - 1
            # The number of all possible combinations will be the possible substitution of each letter
            while nbr < len(name):
                for mot in all_words:
                    all_words.extend(self.__find_words(mot))
                nbr += 1

            return all_words

        except TypeError:
            return []

    def __combine_lists(self, *args):
        '''
        Combines received lists. This means it will give all the possible combinations between the strings of the lists
        it will use itertools.product

        :param *args: the lists to combine

        '''

        try:
            # Combine the lists, each combination is represented by a tuple
            #Then pass the product to the write function
            self.nbr_passwords += self.__write_to_file(product(*args))

        except TypeError:
            pass


    def __write_to_file(self, prod):
        '''
        Write the generated passwords to the given file.

        :param prod: a generator or a list of strings

        :returns: number of passwords written
        '''
        
        nbr_passwords = 0

        with open(self.output, "a") as f:

            for tpl in prod:
                f.write("".join(tpl) + "\n")
                nbr_passwords += 1
                if len(tpl) > 1:
                    f.write("".join(tpl[::-1]) + "\n")
                    nbr_passwords += 1
        
        return nbr_passwords

    def __remove_duplicates(self, liste):
        '''
        Remove duplicates from a list, by setting its elements as dictionary keys, where the keys shouldn't be repeated
        
        :param liste: The list to remove dupliactes from it

        :returns: a list without duplicates
        '''
        return list(OrderedDict.fromkeys(liste))


    def __sub_words(self, name):
        '''
        Function that will take a name, and substitute all the letter by its 

        :param name: The word to substitute its letters

        :returns: a list with all the name's substitutions 
        '''    
        sub_words = []

        words = self.__decompose_word(name)

        if self.phase == 1:
            
            return words
        
        sub_words.extend(words)
        
        for word in words[:-1]:
            sub_words.extend(self.__all_subs(word))
        
        sub_words.extend(self.__all_subs(name))

        return self.__remove_duplicates(sub_words)

    def run(self):
        '''
        The main function to generate all the passwords
        '''
    
        # Will slice the words by prefix
        date_words = self.__decompose_word(self.date)
        first_words = self.__sub_words(self.first)
        last_words = self.__sub_words(self.last)

        if self.phase == 1:
            self.nbr_passwords += self.__write_to_file(date_words)

        self.nbr_passwords += self.__write_to_file(first_words)
        self.nbr_passwords += self.__write_to_file(last_words)
    
        # The combinations according to the order of words. Then sleep(1) will help the CPU        
        self.__combine_lists(first_words, last_words)
        time.sleep(0.2)

        self.__combine_lists(first_words, date_words)
        time.sleep(0.2)

        self.__combine_lists(last_words, date_words)
        time.sleep(0.2)

        self.__combine_lists(first_words, last_words, date_words)
        time.sleep(0.2)
        
        self.__combine_lists(first_words, date_words, last_words)
        time.sleep(0.2)

        self.__combine_lists(last_words, first_words, date_words)
        time.sleep(0.2)



if __name__ == "__main__":  


    print(f"{Fore.GREEN}{banner}{Fore.RESET}")

    parser = ArgumentParser(formatter_class=RawTextHelpFormatter, usage=SUPPRESS)

    opt_parser = parser.add_argument_group("Arguments")
    opt_parser.add_argument('-p', '--phase', dest='phase', choices = [1,2,3], type=int, help="\nSpecify the phase of your desired passlist (1, 2, 3), \
        \n1: Simple combinations between the provided categories\
        \n2: Substitutions of the letters with special characters\
        \n3: Adding characters between words\n")


    sub_parser = parser.add_argument_group("Categories")
    sub_parser.add_argument('-f', '--first', type=str, help="First Name")
    sub_parser.add_argument('-l', '--last',  type=str, help="\nLast Name")
    sub_parser.add_argument('-d', '--date', nargs=3, type=int, help="\nDate of birth")
    
    parser.add_argument('--help-all', dest="helpall", action='store_true', help="More detailed help\n\n")
    # parser.add_argument('-v', '--verbose', action='store_true', help="Verbose Mode\n\n")
    parser.add_argument('-o', '--output', default='wordlist.txt', help="Name of The output file\n\n")
            
    parser.usage = "./passlist.py -p [1/2/3] -f [Fname] -l [Lname] -d [day] [month] [year] -o wordlist.txt"
    parser.description = "\nDescription: A tool that generates a wordlist based on given personal information"
    args = parser.parse_args()

    if args.helpall:

        parser.print_help()
        print(EXAMPLES)
        print("\nThe Letters Substitution Used in Phase 2:\n", DICTO)
        print("\nThe Characters Added Between Words Used in Phase 3:\n", CHARS)
        exit()

    if not args.phase and not args.first and not args.date and not args.last:
        parser.print_help()
        exit()

    if not args.phase:
        parser.error("Please Specify which phase you want, use --help for more informations")        

    if not (args.first or args.last or args.date):
        parser.error("You should specify at least one entry, use --help for more informations")

    password_list = args.output

    #To check if the given file name is empty or not
    try:
        size = os.stat(args.output).st_size
        if size > 0:
            choice = str(input(f"The output file provided '{args.output}' is not empty. Do you want to over-write it? [y/n]: ").lower())
            if choice == "y":
                with open(args.output, "w") as f:
                    f.truncate()
                print()
    except:
        pass

    passlist = Passlist(args.output, args.phase, args.first, args.last, args.date)

    print(f"{Fore.BLUE}[*]{Fore.RESET} Generating the wordlist ...\n")

    # if args.verbose:
    t2 = Thread(target=verbose_function, args=(args.output,))
    t2.start()

    t = Thread(target=passlist.run)
    t.start()

    t.join()
    # if args.verbose:
    t2.join()

    print("Finished\n")
    print(f"{Fore.GREEN}[+]{Fore.RESET} Total Time: ", difference())
    
    size = os.stat(password_list).st_size
    print(f"{Fore.GREEN}[+]{Fore.RESET} Wordlist Size: {format_size(size)}")

    print(f"{Fore.GREEN}[+]{Fore.RESET} Passwords Generated: {passlist.nbr_passwords} passwords\n")
    
