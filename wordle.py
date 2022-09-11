import requests
import json
from termcolor import colored
from rich.console import Console
console = Console()

#make random num gen

def get_word():
    day = 1
    req = requests.get(f"https://thatwordleapi.azurewebsites.net/daily/?day={day}").text
    data = json.loads(req)
    wordls = [*data["Response"]]
    day += 1
    return wordls

def check_word_exist(word):
    req = requests.get(f"https://thatwordleapi.azurewebsites.net/ask/?word={word}").text
    data = json.loads(req)
    print(data)
    if data["Status"] == 200:
        if data["Response"] == True:
            return True
        else:
            print("Not a word")
            ask_word()
    if data["Status"] == 400:
        print("Word must be five letters")
        ask_word()

def ask_word():
    guess = input("")
    if check_word_exist(guess) == True:
        return guess

def check_word(guess, wordls, guesscount):
    box = []
    emptyrow = 5 - guesscount
    guessword = " "
    index = guesscount -  1
    for i in range(5):
        if guess[i] == wordls[i]:
            guessword += '[white on green] [/]' + f'[white on green]{guess[i]}[/]' + '[white on green] [/]'
        elif guess[i] in wordls:
            guessword += '[white on yellow] [/]' + f'[white on yellow]{guess[i]}[/]' + '[white on yellow] [/]'
        else:
            guessword += '[white on black] [/]' + f'[white on black]{guess[i]}[/]' + '[white on black] [/]'
    box.insert(index, guessword)
    box = box[0:guesscount]
    for i in range(emptyrow):
        blankrow = " "
        blankrow += '[white on black] [/]'*15
        box.append(blankrow)
    for i in range(5):
        console.print(box[i])
    return guessword

def main():
    newguess = ""
    guesscount = 0
    while newguess != get_word() or guesscount < 5:
        wordls = get_word()
        newguess = ask_word()
        newguessls = [*newguess]
        guesscount += 1
        check_word(newguessls, wordls, guesscount)


main()