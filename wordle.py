import requests  # to get data from api
import json  # to convert to json
from rich.console import Console  # to highlight, underline, bold, and color text
import os  # to clear console
import sys  # to clear console

console = Console()


def get_word():  # get random word from api
    req = requests.get(
        f"https://random-word-api.herokuapp.com/word?length=5").text  # api is not made by me
    res = json.loads(req)  # convert to json
    data = res[0]  # get the word
    return data


def clear_input():  # clear input from console
    for i in range(2):
        sys.stdout.write('\x1b[1A')
    print("\033[A                                   \033[A")
    sys.stdout.write('\x1b[1A')


def check_word_exist(guess):
    if len(guess) != 5:  # if the word is not 5 letters
        console.print("\n Word must be five letters", style="bold red")
        clear_input()
        return False
    else:
        req = requests.get(
            f"https://api.dictionaryapi.dev/api/v2/entries/en/{guess}").text  # api is not made by me
        data = json.loads(req)
        if type(data) == list:  # if the word has a definition
            return True
        else:
            console.print(
                "\n Not a word                      \033", style="bold red")
            clear_input()
            return False


def ask_word(oldguess):
    global guess
    guess = input("\n ").lower()
    if guess in oldguess:  # if the word has already been guessed
        console.print("\n You already guessed that word", style="bold red")
        clear_input()
        ask_word(oldguess)
    while check_word_exist(guess) == False:  # if the word is not a word
        ask_word(oldguess)
    else:
        return guess


def check_word(box, guess, word, guesscount):
    clear()
    word_dict = letter_dict(word)
    emptyrow = 6 - guesscount  # number of empty rows
    guessword = " "
    index = guesscount - 1
    for i in range(5):  # check letter conditions and add to guessword
        if guess[i] in word and guess[i] != word[i]:
            if word_dict[guess[i]] > 0:  # if there are more than 1 of the letter in the word
                guessword += '[white on yellow] [/]' + \
                    f'[white on yellow]{guess[i]}[/]' + '[white on yellow] [/]'
            else:
                guessword += '[white on black] [/]' + \
                    f'[white on black]{guess[i]}[/]' + '[white on black] [/]'
        if guess[i] == word[i]:
            if word_dict[guess[i]] > 0:
                guessword += '[white on green] [/]' + \
                    f'[white on green]{guess[i]}[/]' + '[white on green] [/]'
                word_dict[guess[i]] -= 1
        if guess[i] not in word:
            guessword += '[white on black] [/]' + \
                f'[white on black]{guess[i]}[/]' + '[white on black] [/]'
    box.insert(index, guessword)  # insert the guessword into the box
    box = box[0:guesscount]
    for i in range(emptyrow):  # add empty rows
        blankrow = " "
        blankrow += '[white on black] [/]'*15
        box.append(blankrow)
    for i in range(6):  # print out the box
        console.print(box[i], style="bold white")


def clear():  # clear the whole console
    os.system('cls' if os.name == 'nt' else 'clear')  # not made by me


# prints out all the letters in the alphabet
def check_letters_left(lettersArr, guess, word):
    letter_index = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                    'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    duplicate = []
    for i in range(5):
        index = letter_index.index(guess[i])
        if guess[i] in word:
            if guess[i] not in duplicate:
                lettersArr[index] = f'[white on yellow]{guess[i]}[/]'
            if guess[i] == word[i]:
                lettersArr[index] = f'[white on green]{guess[i]}[/]'
                duplicate.append(guess[i])
        else:
            lettersArr[index] = f'[white on red]{guess[i]}[/]'
    for i in lettersArr:  # print out the letters of the alphabet
        console.print(f" {i}", style="bold white", end=' ')


def letter_dict(word):  # to keep count on the number of uniqe letters in word
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
    box = []  # the game board
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
               'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    for i in range(6):
        blankrow = " "
        blankrow += '[white on black] [/]'*15
        box.append(blankrow)
        console.print(box[i])
    console.print("\n Enter a 5 letter word\n", style="bold white")
    word = get_word()
    while newguess != word:  # while the player has not won
        if guesscount == 6:
            break
        newguess = ask_word(oldguess)
        oldguess.append(newguess)
        guesscount += 1
        check_word(box, newguess, word, guesscount)
        console.print("\n Enter a 5 letter word\n", style="bold white")
        check_letters_left(letters, newguess, word)
        print("\n")
    if newguess == word:  # if the player wins
        console.print("\n You win", style="bold green")
    if guesscount >= 5:  # if the player loses
        print("\n The word was", end=' ')
        console.print(f"{word}", style="bold white underline")
    console.print("\n Play again? (y/n)", style="bold white", end="")
    again = input(" ").lower()  # ask if the player wants to play again
    if again in ["y", "yes"]:
        clear()
        main()
    else:
        clear()
        quit()


main()
