from xml.etree.ElementTree import tostring
import requests
import json
from rich.console import Console
import random
import os
import sys
console = Console()

#Generate a random word from the api
def get_word():
    num = random.randint(1, 2315)
    req = requests.get(f"https://thatwordleapi.azurewebsites.net/daily/?day={num}").text
    data = json.loads(req)
    wordls = [*data["Response"]]
    return wordls

#Check if the word is a valid word
def check_word_exist():
    req = requests.get(f"https://thatwordleapi.azurewebsites.net/ask/?word={guess}").text
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

#Reset user input
def clear_input():
    for i in range(2):
        sys.stdout.write('\x1b[1A')
    print(" \033[A                             \033[A")
    sys.stdout.write('\x1b[1A')

#Ask user for a word
def ask_word(oldguess):
    global guess
    guess = input("\n ").lower()
    if guess in oldguess:
        console.print("\n You already guessed that word", style="bold red")
        clear_input()
        ask_word(oldguess)
    while check_word_exist() == False:
        ask_word(oldguess)
    else:
        return guess

#Check each letter in the guess against the word and print the result
def check_word(box, guess, wordls, guesscount):
    clear()
    word_dict = letter_dict(wordls)
    emptyrow = 6 - guesscount
    guessword = " "
    index = guesscount -  1
    for i in range(5):
        if guess[i] in wordls and guess[i] != wordls[i]:
            if word_dict[guess[i]] > 0:
                guessword += '[white on yellow] [/]' + f'[white on yellow]{guess[i]}[/]' + '[white on yellow] [/]'
                word_dict[guess[i]] -= 1
            else:
                guessword += '[white on black] [/]' + f'[white on black]{guess[i]}[/]' + '[white on black] [/]'
        if guess[i] == wordls[i]:
            guessword += '[white on green] [/]' + f'[white on green]{guess[i]}[/]' + '[white on green] [/]'
        if guess[i] not in wordls:
            guessword += '[white on black] [/]' + f'[white on black]{guess[i]}[/]' + '[white on black] [/]'
    box.insert(index, guessword)
    box = box[0:guesscount]
    for i in range(emptyrow):
        blankrow = " "
        blankrow += '[white on black] [/]'*15
        box.append(blankrow)
    for i in range(6):
        console.print(box[i])
    return guessword

#Clear the terminal
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

#Check which letters are left on the alphabet
def check_letters_left(letters, guess, word):
    letters_def = letters.copy()
    for i in range(5):
        if guess[i] in word:
            try:
                index = letters_def.index(guess[i])       
                letters[index] = f'[white on yellow]{guess[i]}[/]'
            except ValueError:
                pass
            if guess[i] == word[i]:
                try:
                    index = letters_def.index(guess[i])       
                    letters[index] = f'[white on green]{guess[i]}[/]'
                except ValueError:
                    pass
        else:
            try:
                index = letters_def.index(guess[i])
                letters[index] = f'[white on red]{guess[i]}[/]'
            except ValueError:
                pass
    for i in letters:
        console.print(f" {i}", style="bold white", end=' ')

#return a dictionary with the letters of the word and the number of times they appear
def letter_dict(word):
    dict = {}
    for letter in word:
        if dict.get(letter,None) != None:
                dict[letter]+=1
        else:
            dict[letter] = 1  
    return dict

def main():
    clear()
    newguess = ""
    guesscount = 0
    oldguess = []
    box = []
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    #print empty box
    for i in range(6):
        blankrow = " "
        blankrow += '[white on black] [/]'*15
        box.append(blankrow)
        console.print(box[i])
    print("\n Enter a 5 letter word\n")
    #loop until the user guesses the word
    word = "".join(get_word())
    while newguess != word:
        if guesscount == 6:
            break
        newguess = ask_word(oldguess)
        oldguess.append(newguess)
        newguessls = [*newguess]
        guesscount += 1
        check_word(box, newguessls, word, guesscount)
        print("\n Enter a 5 letter word\n")
        check_letters_left(letters, newguessls, word)
        print(" ")
    #ends game
    if newguess == word:
        console.print("\n You win", style="bold green")
    if guesscount >= 5:
        print("\n The word was", end=' ')
        console.print(f"{''.join(word)}", style="bold white")
    again = input("\n Play again? (y/n) ").lower()
    if again in ["y", "yes"]:
        clear()
        main()
    else:
        clear()
        quit()

main()