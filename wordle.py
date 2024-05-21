import datetime
import requests
import enchant
import re
from itertools import product

class Wordle(object):
    global_guess = ""

    official_word_dictionary = enchant.Dict("en_US")

    iteration_counter = 0

    not_in_location = {}

    is_in_location = {}

    my_word_map = {}

    possible_words = []

    not_in_word = []

    # ADD A CASE TO REMOVE WORDS THAT SHOULD CONTAIN A LETTER BUT DONT



    f = open("text.txt", "r")
    array = f.readlines()
    for line in array:
        for letters in line:
            if letters.isalpha():
                letters = letters.lower()
                if letters not in my_word_map:
                    my_word_map[letters] = 1
                else:
                    my_word_map[letters] += 1

    sorted = sorted(my_word_map.items(), key=lambda x:x[1], reverse=True)
    converted_dict = dict(sorted)


    def getSolution(self):
        date = datetime.date.today()
        # url = f"https://www.nytimes.com/svc/wordle/v2/{date:%Y-%m-%d}.json"
        url = "https://www.nytimes.com/svc/wordle/v2/2024-05-24.json"
        response = requests.get(url).json()
        solution = response['solution']
        return solution
    
    def makeGuess(self, trueSolution, counter):

        if counter == 1:
            # print(f'Current game state: _____')
            first_guess = 'stare'
            print(f'The bot\'s first guess was: {first_guess}')
            self.seeIfCorrect(trueSolution, first_guess, counter)
            perms = self.generate_permutations(Wordle.converted_dict)
            # print(f'perms: {perms}')
            Wordle.possible_words = perms
            # okay, so Wordle.possible_words will always contain the possible words based on the first guess
            # from here, we can choose the BEST word from Wordle.possible_words, updating the not_in_location dictionary, and then remove



        else:
            # if word has not been guessed:
            if Wordle.global_guess != trueSolution:

                copied_array = Wordle.possible_words

                # iterate over copy 
                print(f'not in location: {Wordle.not_in_location}')
                # print('\n')
                print(f'In location: {Wordle.is_in_location}')
                # print('\n')
                # print(f'possible letters: {Wordle.converted_dict}')
                # print('\n')
                print(f'Possible words: {Wordle.possible_words}')
                print(f'We know for sure it doesnt contain: {Wordle.not_in_word}')
                for word in copied_array:
                    remove_word = False
                    
                   
                    for index, letter in enumerate(word):
                        # print(f'letter: {letter}')
                        # print(index)
                        # if letter in Wordle.not_in_location and word.index(word[index]) in Wordle.not_in_location[letter]:
                        if letter in Wordle.not_in_location and index in Wordle.not_in_location[letter]:
                            remove_word = True
                            print(f'I just removed {word} because it violated {Wordle.not_in_location}')
                        elif letter in Wordle.not_in_word:
                            remove_word = True
                             
                    if not remove_word:
                        for letter in word:
                            # FIX THIS LOGIC
                            # ALSO, ADD A CASE FOR WHEN LETTERS ARE 100% NOT IN THE LETTER
                            if letter in Wordle.is_in_location and word.index(letter) not in Wordle.is_in_location[letter]:
                            # if letter in Wordle.is_in_location and index not in Wordle.is_in_location[letter]:

                                remove_word = True
                                print(f'(Other case) I just removed {word} because it violated {Wordle.is_in_location}')
                                 

                    if remove_word:
                        Wordle.possible_words.remove(word)

                
                # print(f'New word list: {Wordle.possible_words}')

                # make next best choice
                high_score = 0
                best_choice = ""
                for word_ in Wordle.possible_words:
                    # ADD A LOGIC CASE SO THAT BEST CHOICE DOESNT CONTAIN DUPLICATE LETTERS
                    sum = 0
                    for letter_ in word_:
                        if letter_ in Wordle.converted_dict:
                            # print(f'letter: {letter_}, score: {Wordle.converted_dict[letter_]}')
                            sum += Wordle.converted_dict[letter_]
                        else:
                            sum += -1000
                    if sum > high_score:
                        high_score = sum
                        best_choice = word_
                
                if best_choice == trueSolution:
                    print(f'GUESS: {trueSolution}')
                    return "Done."
                
                else:
                    self.seeIfCorrect(trueSolution, best_choice, counter)
            
            else:
                print("Answer has been guessed")
                return "Done."






    def match_with_wildcards(self, pattern, word):
        regex_pattern = re.sub(r'[_A-Z]', '[a-z]', pattern)
        regex = re.compile(regex_pattern)
        # print(f'Does "{pattern}" match "{word}"?')
        result = bool(regex.fullmatch(word))
        # if result:
        #     print(f'YES, {pattern} matches {word}')
        return result

    def generate_permutations(self, letter_freq):
        letters = ''.join(letter_freq.keys())
        real_words = []

        # print(f'guess: {Wordle.global_guess}')
        
        for combination in product(letters, repeat=5):
            word = ''.join(combination)
            if Wordle.official_word_dictionary.check(word):
                if Wordle.official_word_dictionary != "_____" and not re.search(r'[A-Z]', Wordle.global_guess):
                    # print('here')
                    if self.match_with_wildcards(Wordle.global_guess, word):
                        if word not in real_words:
                            real_words.append(word) 
                elif re.search(r'[A-Z]', Wordle.global_guess): 
                    if self.match_with_wildcards(Wordle.global_guess, word):
                        for letter in word:
                            if letter in Wordle.not_in_location:
                                # print('yes')
                                if (word.index(letter) + 1) not in Wordle.not_in_location[letter]:
                                    if word not in real_words:
                                        real_words.append(word)

                else:
                    if word not in real_words:
                        real_words.append(word)
        return real_words

    def seeIfCorrect(self, trueSolution, firstGuess, counter):
        # Wordle.global_guess = ""

        print(f'GUESS: {firstGuess}')

        solution_map = {}
        for letter in trueSolution:
            if letter not in solution_map:
                solution_map[letter] = 1
            else:
                solution_map[letter] += 1

        for index in range(len(trueSolution)):
            solution_letter = trueSolution[index]
            # print(f'first guess: {firstGuess}')
            # print(f'index of guess: {firstGuess[index]}')
            # print(f'index of current reveal: {Wordle.global_guess}')
            if solution_letter == firstGuess[index]:
                if solution_map[solution_letter] > 0:
                    solution_map[solution_letter] -= 1
                    Wordle.global_guess += solution_letter.lower()
                    if solution_letter.lower() not in Wordle.is_in_location:
                        if index not in Wordle.is_in_location:
                            Wordle.is_in_location[solution_letter.lower()] = [index]
                        else:
                            Wordle.is_in_location[solution_letter.lower()].append(index)
            elif trueSolution.__contains__(firstGuess[index]):
                if solution_map[firstGuess[index]] > 0:
                    solution_map[firstGuess[index]] -= 1
                    Wordle.global_guess += firstGuess[index].upper()
                    if firstGuess[index] not in Wordle.not_in_location:
                        Wordle.not_in_location[firstGuess[index]] = [index]
                    else:
                        Wordle.not_in_location[firstGuess[index]].append(index)
                else:
                    Wordle.global_guess += "_"
                    if firstGuess[index] not in Wordle.not_in_location:
                        Wordle.not_in_location[firstGuess[index]] = [index]
                    else:
                        Wordle.not_in_location[firstGuess[index]].append(index)

            else:
                Wordle.not_in_word.append(firstGuess[index])
                Wordle.global_guess += "_"
                if firstGuess[index] in Wordle.converted_dict:
                    del Wordle.converted_dict[firstGuess[index]]

                if firstGuess[index] not in Wordle.not_in_location:
                    Wordle.not_in_location[firstGuess[index]] = [index]
                else:
                    Wordle.not_in_location[firstGuess[index]].append(index)

        
        if counter == 1:
            return Wordle.global_guess
        else:
            slicer = ((counter - 1) * 5)
            Wordle.global_guess = wordle.global_guess[slicer:]
            return Wordle.global_guess

game_counter = 1
wordle = Wordle()
solution = wordle.getSolution()
while game_counter <= 6:
    res = wordle.makeGuess(solution, game_counter)
    # print(f'Respinse in while: {res}')
    if res == "Done.":
        print(f"Won in {game_counter} moves.")
        break
    elif game_counter == 6:
        print("The game was lost in 6 guesses.")
    game_counter += 1

