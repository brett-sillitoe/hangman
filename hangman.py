import random

def greetUser():
	"""Greets the user and provides instructions"""
	print("Hello! Hangman is a simple game. A word will be randomly selected and your job is to guess it!")
	print("You win if you either guess all of the correct letters or guess the correct word.")
	print("You lose if you guess 10 incorrect letters or guess the incorrect word.")
	print("Have fun!")

def getNumOfLines():
	"""Gets the number of lines in a file"""
	file_name = "words.txt"
	num_of_lines = 0
	with open(file_name) as f:
		lines = f.readlines()
		for line in lines:
			num_of_lines = num_of_lines + 1
		return num_of_lines
		
def getWord(num_of_lines):
	"""Gets a random word from words.txt"""
	file_name = "words.txt"
	line_number = random.randint(0,num_of_lines - 1)
	line_counter = 0
	word = ""
	
	with open(file_name) as f:
		lines = f.readlines()
		for line in lines:
			if(line_number == line_counter):
				for c in line:
					if(c == "\n"):
						c = c
					else:
						word = word + c
				if(line_number == 0):
					word = word[3:]
				break
			else:
				line_counter = line_counter + 1
		return word

def generateHiddenWord(word):
	"""Generates the hidden word"""
	hidden_word = ""
	for c in word:
		hidden_word = hidden_word + "_"
	return list(hidden_word)
	
def promptForGuess():
	"""Gets the users guess"""
	guess = input("\nPlease either guess a letter or the word if you think you know it.\n")
	while(not guess.isalpha()):
		guess = input("Please only enter letters. Try again.\n")
	return guess.lower()
	
def checkGuess(guess, word, guessed_letters):
	"""Checks the validity of the players guess"""
	while(True):
		if(len(guess) == 1):
			if(guess in guessed_letters):
				print("You already guessed " + guess + ".")
				return 0
			elif(guess in word):
				return 1
			else:
				return 2
				
		elif(len(guess) == len(word)):
			if(guess == word):
				return 3
			else:
				return 4
				
		else:
			print("Your guess was the incorrect length. The word has " + str(len(word)) + " letters.\n")
			return 0
		
def updateHiddenWord(guess, word, hidden_word):
	"""Updates the hidden word"""
	char_index = 0
	for c in word:
		if(guess == c):
			hidden_word[char_index] = c
		char_index = char_index + 1	
		
def printHiddenWord(hidden_word):
	"""Prints the hidden_word in a legible format"""
	print_word = ""
	for c in hidden_word:
		print_word = print_word + c + " "
	print(print_word)
		
def gameover(result, word):
	"""Performs the correct action for the given result"""
	if(result == 1):
		print("Congrats you won! You guessed all of the letters! The word was " + word + ".")
		return playAgain()
		
	elif(result == 2):
		print("Oops! You guessed 10 wrong letters.")
		print("The word was " + word + ".")
		print("GAME OVER.")
		return playAgain()
		
	elif(result == 3):
		print("Congrats you won! You guessed the correct word, " + word + "!")
		return playAgain()
		
	elif(result == 4):
		print("Oops! You guessed the wrong word.")
		print("The word was " + word + ".")
		print("GAME OVER.")
		return playAgain()

def playAgain():
	"""Asks the user if they want to play again"""
	answer = input("Would you like to play again? Y/N\n").lower()
	if(answer == "y" or answer == "yes"):
		return 1
	else:
		return 0
		
def goodbye():
	"""Thanks the user for playing and tells them goodbye"""
	print("Okay, thanks for playing!")
	exit()
	
def play():
	"""Runs the game"""
	num_of_lines = getNumOfLines()
	word = getWord(num_of_lines)
	hidden_word = generateHiddenWord(word)
	guessed_letters = ""
	incorrect_guesses = 0
	play_again_status = -1
	
	greetUser()
	
	printHiddenWord("".join(hidden_word))
	
	while(True):
		#Prompts user for guess and checks it
		guess = promptForGuess()
		guess_accuracy = checkGuess(guess, word, guessed_letters)
		
		#Guessed a correct letter
		if(guess_accuracy == 1):
			guessed_letters = guessed_letters + guess
			updateHiddenWord(guess,word,hidden_word)
			printHiddenWord("".join(hidden_word))
			
			#All letters in the word have been guessed
			if("_" not in "".join(hidden_word)):
				play_again_status = gameover(1,word)
				
		#Guessed an incorrect letter		
		elif(guess_accuracy == 2):
			guessed_letters = guessed_letters + guess
			print("Sorry " + guess + " is not in the word")
			incorrect_guesses = incorrect_guesses + 1
			printHiddenWord("".join(hidden_word))
			print("\nIncorrect guesses: " + str(incorrect_guesses))
			
			#There have been 10 incorrect guesses
			if(incorrect_guesses == 10):
				play_again_status = gameover(2,word)
		
		#Guessed the correct word		
		elif(guess_accuracy == 3):
			play_again_status = gameover(3,word)
		
		#Guessed an incorrect word	
		elif(guess_accuracy == 4):
			play_again_status = gameover(4,word)
		
		#Replied that they want to play again
		if(play_again_status == 1):
			print("Awesome!")
			word = getWord(num_of_lines)
			hidden_word = generateHiddenWord(word)
			printHiddenWord("".join(hidden_word))
			incorrect_guesses = 0
			guessed_letters = ""
			play_again_status = -1
		
		#Replied that they didn't want to play again
		elif(play_again_status == 0):
			goodbye()
			
play()
