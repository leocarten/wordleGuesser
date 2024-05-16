import datetime
import requests
import enchant
import re

class Wordle(object):
    global_guess = ""
    incorrect_letters = []
    def getSolution(self):
        date = datetime.date.today()
        url = f"https://www.nytimes.com/svc/wordle/v2/{date:%Y-%m-%d}.json"
        response = requests.get(url).json()
        solution = response['solution']
        return solution
    
    def makeGuess(self, trueSolution, guess):
        if guess == 1:
            self.seeIfCorrect(trueSolution, 'stare')
        else:
            # make a guess based on the guess
            print(f'This is current: {Wordle.global_guess}')

            # remove colors
            stringWithoutColors = re.sub(r'\033\[[0-9;]+m', '', Wordle.global_guess)

            # see if we literally have nothing right
            if stringWithoutColors == "_____":
                print(Wordle.incorrect_letters)
            else:
                # we have something right
                # LEFT OFF HERE
                print("yay")

        return Wordle.global_guess
    
    def seeIfCorrect(self, trueSolution, guess):
        guess = guess.lower()
        solutionToArray = list(trueSolution)
        guessToArray = list(guess)
        return self.evaluateGuess(solutionToArray, guessToArray)

    def evaluateGuess(self, trueSolutionAsArray, guessAsArray):
        string = ""
        for letters in range(len(trueSolutionAsArray)):
            if trueSolutionAsArray[letters] == guessAsArray[letters]:
                string += trueSolutionAsArray[letters]
            elif guessAsArray[letters] in trueSolutionAsArray:
                string += "\033[93m" + guessAsArray[letters].upper() + "\033[0m"
            else:
                string += "\033[91m" + '_' + "\033[0m"
                Wordle.incorrect_letters.append(guessAsArray[letters])
        Wordle.global_guess = string
        return string
        


# generate dictionary 
# my_word_map = {}
# f = open("text.txt", "r")
# array = f.readlines()
# for line in array:
#     for letters in line:
#         if letters.isalpha():
#             letters = letters.lower()
#             if letters not in my_word_map:
#                 my_word_map[letters] = 1
#             else:
#                 my_word_map[letters] += 1

# sorted = sorted(my_word_map.items(), key=lambda x:x[1], reverse=True)
# converted_dict = dict(sorted)

# print(converted_dict)

# maybe the best word is stare ?

game_counter = 1
wordle = Wordle()
solution = wordle.getSolution()
while game_counter <= 5:
    print(wordle.makeGuess(solution, game_counter))
    game_counter += 1

# Get the English word list
# word_list = nltk.corpus.words.words()