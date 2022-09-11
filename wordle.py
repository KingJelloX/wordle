import requests
import json
from rich.console import Console
import os
console = Console()

#make random num gen

def get_word():
    day = 1
    req = requests.get(f"https://thatwordleapi.azurewebsites.net/daily/?day={day}").text
    data = json.loads(req)
    wordls = [*data["Response"]]
    day += 1
    return wordls

def check_word_exist():
    req = requests.get(f"https://thatwordleapi.azurewebsites.net/ask/?word={guess}").text
    data = json.loads(req)
    if data["Status"] == 200:
        if data["Response"] == True:
            return True
        else:
            print("Not a word")
            return False
    if data["Status"] == 400:
        print("Word must be five letters")
        return False

def ask_word():
    global guess
    guess = input("")
    while check_word_exist() == False:
        ask_word()
    else:
        return guess

def check_word(box, guess, wordls, guesscount):
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

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    newguess = ""
    guesscount = 0
    box = []
    word = get_word()
    while newguess != word:
        if guesscount == 5:
            break
        newguess = ask_word()
        newguessls = [*newguess]
        guesscount += 1
        check_word(box, newguessls, word, guesscount)
    if newguess == get_word():
        print("You win")
    if guesscount >= 5:
        print(f"The word was {''.join(get_word())}")
    again = input("Play again? (y/n)").lower()
    if again in ["y", "yes"]:
        clear()
        main()
    else:
        quit()

main()