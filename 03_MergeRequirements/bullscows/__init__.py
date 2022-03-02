import numpy as np
import textdistance

from typing import List

def bullscows(guess: str, secret: str):
  
    return textdistance.hamming.similarity(guess, secret), textdistance.bag.similarity(guess, secret) - textdistance.hamming.similarity(guess, secret)

def gameplay(ask: callable, inform: callable, words: List[str]):
    
    secret = np.random.choice(words, 1)[0]
    counter = 0
    secret_len = secret.__len__()
    #print(secret)
    
    while True:
        attempt = ask("Введите слово: ", words)
        counter += 1
        b, c = bullscows(attempt, secret)

        inform("Быки: {}, Коровы: {}", b, c)

        if b == secret_len:
            return counter
