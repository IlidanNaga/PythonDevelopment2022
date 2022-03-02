import sys
import urllib.request as request
from typing import List

from bullscows import gameplay

if __name__ == '__main__':

    def ask(prompt: str, valid: List[str] = None):
        
        if valid is None:
            
            word = input(prompt)
            
        else:
            
            while True:
                
                word = input(prompt)
                if word in valid:
                    break
                    
        return word


    def inform(format_string: str, bulls: int, cows:int):

        print(format_string.format(bulls, cows))


    try:
        f = open(sys.argv[1], "r", encoding='utf8')
        words = f.read().split()
    except IOError:
        f = request.urlopen(sys.argv[1])
        words = f.read().decode('utf-8').split()

    word_len = 5
    if sys.argv.__len__() > 2:
        word_len = int(sys.argv[2])

    words = [x for x in words if x.__len__() == word_len]

    print(gameplay(ask, inform, words))

    