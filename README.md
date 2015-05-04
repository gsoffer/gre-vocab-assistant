# gre-vocab-assistant
GRE Vocab Prep App written in Python

To run, first make sure that the words list, "GRE Words.txt", is in the same folder as the python script, "GRE_Vocab_Assistant.py".
Then simply navigate to the folder containing both files, and run:
python GRE_Vocab_Assistant.py

Usage: To move on to the next word, you can either click the "Next Word" button, or press the "d" key on your keyboard. The app cycles through up to 15 words that can be learned at any given time. A word is considered "mastered" if you move on to the next word in under 1.5 seconds. As words are mastered, new words are added to the 15 word cycle. The order of words given within the 15 word cycle is random, so you may see one word three times as often as another. 

This process was tested with Python 2.7 on OS X, but all of the required modules should come straight out of the box on most distributions, and all of the functionalities used should be cross-platform compatible. 

Feel free to adjust the words list as you wish - to remove unnecessary words, add new words, or replace with a completely new list of vocab words that suits your purpose!

