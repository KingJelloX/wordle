from xml.etree.ElementTree import tostring
import requests
import json
from rich.console import Console
import random
import os
import sys
console = Console()


def get_word():
    num = random.randint(1, 2315)
    req = requests.get(
        f"https://thatwordleapi.azurewebsites.net/daily/?day={num}").text
    data = json.loads(req)
    word = data["Response"]
    return word


def check_word_exist(guess):
    req = requests.get(
        f"https://thatwordleapi.azurewebsites.net/ask/?word={guess}").text
    data = json.loads(req)
    if data["Status"] == 200:
        if data["Response"] == True:
            return True
        else:
            console.print("\n Not a word", style="bold red")
            clear_input()
            return False
    if data["Status"] == 400:
        console.print("\n Word must be five letters", style="bold red")
        clear_input()
        return False


def clear_input():
    for i in range(2):
        sys.stdout.write('\x1b[1A')
    print(" \033[A                                      \033[A")
    sys.stdout.write('\x1b[1A')


def ask_word(oldguess):
    global guess
    guess = input("\n ").lower()
    if guess in oldguess:
        console.print("\n You already guessed that word", style="bold red")
        clear_input()
        ask_word(oldguess)
    while check_word_exist(guess) == False:
        ask_word(oldguess)
    else:
        return guess


def check_word(box, guess, word, guesscount):
    clear()
    word_dict = letter_dict(word)
    emptyrow = 6 - guesscount
    guessword = " "
    index = guesscount - 1
    for i in range(5):
        if guess[i] in word and guess[i] != word[i]:
            if word_dict[guess[i]] > 0:
                guessword += '[white on yellow] [/]' + \
                    f'[white on yellow]{guess[i]}[/]' + '[white on yellow] [/]'
                word_dict[guess[i]] -= 1
            else:
                guessword += '[white on black] [/]' + \
                    f'[white on black]{guess[i]}[/]' + '[white on black] [/]'
        if guess[i] == word[i]:
            guessword += '[white on green] [/]' + \
                f'[white on green]{guess[i]}[/]' + '[white on green] [/]'
        if guess[i] not in word:
            guessword += '[white on black] [/]' + \
                f'[white on black]{guess[i]}[/]' + '[white on black] [/]'
    box.insert(index, guessword)
    box = box[0:guesscount]
    for i in range(emptyrow):
        blankrow = " "
        blankrow += '[white on black] [/]'*15
        box.append(blankrow)
    for i in range(6):
        console.print(box[i], style="bold white")


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def check_letters_left(guess, word):
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
               'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    letter_index = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                    'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    for i in range(5):
        try:
            index = letter_index.index(guess[i])
        except ValueError:
            pass
        if guess[i] in word:
            letters[index] = f'[white on yellow]{guess[i]}[/]'
            if guess[i] == word[i]:
                letters[index] = f'[white on green]{guess[i]}[/]'
        else:
            letters[index] = f'[white on red]{guess[i]}[/]'
    for i in letters:
        console.print(f" {i}", style="bold white", end=' ')


def letter_dict(word):
    dict = {}
    for letter in word:
        if dict.get(letter) != None:
            dict[letter] += 1
        else:
            dict[letter] = 1
    return dict


def main():
    clear()
    newguess = ""
    guesscount = 0
    oldguess = []
    box = []
    for i in range(6):
        blankrow = " "
        blankrow += '[white on black] [/]'*15
        box.append(blankrow)
        console.print(box[i])
    console.print("\n Enter a 5 letter word\n", style="bold white")
    word = get_word()
    print(word)
    while newguess != word:
        if guesscount == 6:
            break
        newguess = ask_word(oldguess)
        oldguess.append(newguess)
        guesscount += 1
        check_word(box, newguess, word, guesscount)
        console.print("\n Enter a 5 letter word\n", style="bold white")
        check_letters_left(newguess, word)
        print("\n")
    if newguess == word:
        console.print("\n You win", style="bold green")
    if guesscount >= 5:
        print("\n The word was", end=' ')
        console.print(f"{word}", style="bold white underline")
    console.print("\n Play again? (y/n)", style="bold white", end="")
    again = input(" ").lower()
    if again in ["y", "yes"]:
        clear()
        main()
    else:
        clear()
        quit()


main()
