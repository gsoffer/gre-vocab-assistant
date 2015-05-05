# gre-vocab-assistant
# GRE Vocab Prep App written in Python
# Written by Gil Soffer (Originally 05-04-2015)
# Feel free to modify and repurpose as you wish!



# IMPORT NECESSARY MODULES
import random # Import the random module to choose the next word at random
from datetime import datetime # Import the datetime module to measure seconds between button presses
import Tkinter as gui # Import the Tkinter gui development module



# IMPORT VOCABULARY FILE
vocab_lookup= [] # Array to store vocabulary file (as array of arrays, each inner array containing details for one vocab word)
fin = open('GRE Words.txt', "r") # Read in the vocabulary file

for line in fin.readlines()[1:]: # For each line, skipping the header row...
	word_data = line.split('\t') # Store the contents of each line as an array of column values
	word_data[2] = word_data[2].rstrip('\n') # Remove the new line character from last (3rd) column
	vocab_lookup.append(word_data) # Add the word's details to the vocabulary lookup array

fin.close() # Close the file once our array has been assigned



# INITIALIZE THE LISTS OF MASTERED, CURRENTLY LEARNING, AND REMAINING WORDS
mastered_list = [] # The list of indeces (in vocab_lookup array) corresponding to words that have been mastered

learning_list = [] # The list of indeces (in vocab_lookup array) corresponding to words that are currently being learned

remaining_list = [] # The list of indeces (in vocab_lookup array) corresponding to words that have not been given yet

# Begin by appending all indeces to the "remaining" list, as none have been learned yet
for x in range(len(vocab_lookup)):
	remaining_list.append(x)



# DEFINE "VOCAB WORD" CLASS FOR WORDS CURRENTLY BEING LEARNED
class Vocab_Word(object):
	
	def __init__(self, index):
		self.new_word(index)
	
	def new_word(self, new_index):
		learning_list.append(new_index)
		remaining_list.remove(new_index)
		self.index = new_index
		self.word = vocab_lookup[new_index][0]
		self.definition = vocab_lookup[new_index][1]
		self.example = vocab_lookup[new_index][2]
	
	def mastered(self):
		mastered_list.append(self.index)
		learning_list.remove(self.index)



# INSTANTIATE THE VOCAB WORDS TO BEGIN LEARNING
learning_vocab_words = {} # Dictionary mapping index (in vocab_lookup array) to a Vocab Word object

max_words_learning = 15 # The max number of words that can be learned simultaneously at any given time

if len(vocab_lookup) < max_words_learning: # If there are less words than the max...
	num_learning = len(vocab_lookup) # The max becomes the total number of words
else:
	num_learning = max_words_learning # Otherwise instantiate the max number of vocab words to learn at once

# Instantiate the appropriate number of vocab word objects, 
# and add them as dictionary values mapped by index values from the vocab_lookup array
for x in range(num_learning):
	rand_idx = random.choice(remaining_list)
	learning_vocab_words[rand_idx] = Vocab_Word(rand_idx)



# DESIGN THE GUI (NO INTERACTIVITY DEFINED YET)
max_width = 550 # Max width in pixels
max_height = 355 # Max height in pixels
wrap_length = max_width - 50 # Max width of text before continuing on next line
bg_color = "#B2DFEE" # Header and footer background color

window = gui.Tk() # Create a new window
window.title("GRE Vocabulary Assistant") # Set the window title
window.geometry(str(max_width) + "x" + str(max_height)) # Set the window size in pixels

title_label = gui.Label(window, text="Vocabulary Preparation", font=("Helvetica", 16), pady=8, width=max_width, bg=bg_color) # Create a label widget for the vocab word
title_label.pack() # Add the title label widget into the window

word_label = gui.Label(window, font=("Helvetica", 20, "bold"), padx=20, pady=20, anchor="w", justify="left", width=max_width) # Create a label widget for the vocab word
word_label.pack() # Add the word label widget into the window

def_label = gui.Label(window, font=("Helvetica", 16), wraplength=wrap_length, padx=20, anchor="w", justify="left", width=max_width, height=2) # Create a label widget for the word definition
def_label.pack() # Add the definition label widget into the window

invisible_label_1 = gui.Label(window, width=550, pady=1) # Create an invisible label widget to take space
invisible_label_1.pack() # Add the invisible label widget into the window

example_label = gui.Label(window, font=("Helvetica", 16, "italic"), wraplength=wrap_length, padx=20, anchor="nw", justify="left", width=max_width, height=5) # Create a label widget for the example sentence
example_label.pack() # Add the example label widget into the window

next_label = gui.Label(window, text="Next Word", font=("Helvetica", 16), pady=10, bg="#38B0DE", width=max_width) # Create a pseudo button widget for moving onto the next word (button colors don't work in OS X, so using label)
next_label.pack() # Add the next label widget into the window

stats_label = gui.Label(window, font=("Helvetica", 13), pady=10, width=max_width, height=10, bg=bg_color, anchor="n") # Create a label widget for progress stats
stats_label.pack() # Add the stats label widget into the window



# DEFINE SCREEN UPDATE FUNCTION
# Update the values on the screen for the newly chosen vocab word
def update_screen(index):
	if len(learning_list) == 0: # If the user has mastered all of the words then game ends, congratulate them
		word_label.configure(text="Congratulations!")
		def_label.configure(text="You mastered every single word!")
		example_label.configure(text="")
	else:
		word_label.configure(text=learning_vocab_words[index].word) # Update vocab word label value
		def_label.configure(text=learning_vocab_words[index].definition) # Update definition label value
		example_label.configure(text=learning_vocab_words[index].example) # Update example sentence label value
	stats = "Words Mastered: " + str(len(mastered_list)) + "  " + u"\u00B7" + "  Words Remaining: " + str(len(remaining_list) + len(learning_list)) # Calculate stat text string
	stats_label.configure(text=stats) # Update stats label value



# REFRESH WORD FUNCTION
# This function measures how much time passed between button presses, 
# moves words among the mastered, learning, and remaining word lists, 
# determines the next appropriate word to display on the screen,
# and modifies the vocab word objects as necessary.
current_idx = learning_list[0] # Determine the starting word (chosen at random)
update_screen(current_idx) # Display details for the starting word
current_datetime = datetime.now() # Note the start time
mastered_threshold = 1.5 # Number of seconds under which the word is considered mastered
def refresh_word():
	global current_idx
	global current_datetime
	seconds_elapsed = (datetime.now() - current_datetime).total_seconds() # Calculate the number of seconds between button presses
	current_datetime = datetime.now() # Overwrite the last button pressed time
	if seconds_elapsed < mastered_threshold: # If button pressed before threshold...
		learning_vocab_words[current_idx].mastered() # The word has been mastered
		if len(remaining_list) == 0: # If there are no more words to add to the learning list...
			learning_vocab_words.pop(current_idx) # Drop the vocab word completely
			if len(learning_list) == 0: # If all words have been mastered...
				chosen_idx = current_idx # Don't change the vocab word
			else: # Otherwise, if not all words have been mastered...
				choice_list = list(set(learning_list) - set([current_idx])) # Calculate the list of choices for the next word
				chosen_idx = random.choice(choice_list) # Randomly choose the next word
		else: # Otherwise, if there are still words that haven't been shown yet...
			chosen_idx = random.choice(remaining_list) # Choose a word at random from the remaining list
			learning_vocab_words[chosen_idx] = learning_vocab_words.pop(current_idx) # Change the key to the new index
			learning_vocab_words[chosen_idx].new_word(chosen_idx) # Refresh the vocab word object attributes
	else: # Otherwise, if it took too long for the user to press the "next" button...
		if len(learning_list) == 1: # If there is only one word left...
				chosen_idx = current_idx # Don't change the vocab word
		else: # Otherwise, if there are multiple words still being learned...
			choice_list = list(set(learning_list) - set([current_idx])) # Calculate the list of choices for the next word
			chosen_idx = random.choice(choice_list) # Randomly choose the next word
	current_idx = chosen_idx # Update the current word index variable to the newly chosen word's index
	update_screen(chosen_idx) # Update the actual visual text displayed for the newly chosen word



# CALLBACK FUNCTION FOR "NEXT" BUTTON
def next_word(event):
	if len(learning_list) == 0: # If all words have been mastered
		pass # No longer do anything
	else:
		refresh_word() # Otherwise, refresh the word as appropriate



# DEFINE "NEXT" BUTTON MOUSEOVER COLOR CHANGE FUNCTIONS
def next_color_enter(event): # On mouse over
	next_label.configure(bg="#4682B4", cursor="hand2") # Change background color and cursor to pointing hand

def next_color_leave(event): # On mouse remove
	next_label.configure(bg="#38B0DE") # Change background color back to original color



# BIND APPROPRIATE FUNCTIONS TO "NEXT" BUTTON SO THAT GUI IS INTERACTIVE
next_label.bind("<Button-1>", next_word) #bind to the callback function
next_label.focus_set() # Allow key binding to work
next_label.bind("d", next_word) # Bind to keyboard press (specific key)
next_label.bind("<Enter>", next_color_enter) # Bind to mouse over function
next_label.bind("<Leave>", next_color_leave) # Bind to mouse remove function



# DRAW THE GUI AND BEGIN!
window.mainloop() # Draw the window and start the application


