'''
This script is for nextWord prediction.
Data is taken from inputText file
next word prediction works on bigram and trigram model
This script compatible with python 2.7
@auther Jaydeep Devda 205217017
'''

# for json parsing
import json
# to remove non ascii charcs from input text
# clear texts
import re
# Counter is for count occurrences and probabilities
# OrderDict is for sorting
from collections import Counter, OrderedDict

# nltk for bigram and trigram model building
import nltk
# for retrieve text and meta data from pdf file
from PyPDF2 import PdfFileReader
# beautiful shop for extracting content from html
from bs4 import BeautifulSoup
# docx library for document file manipulation
from docx import Document

'''
This predictWordUsingBigramModel function is for predicting next word in a sentence using BigramModel
param: dictionary model of bigram and inputSentence
'''


# ====================== function predictWordUsingBigramModel start ======================
def predictWordUsingBigramModel(dictofBigram, inputSentence):
    try:
        # last word
        lastWordofSentence = inputSentence.split()[-1].lower()

        # flag is to check any matches found or not
        flag = False

        # dicofBigram list is in form of [((firstWord,nextWord),occurrences),
        #                                 ((firstWord,nextWord),occurrences) ]...
        for (firstWord, nextWord), count in dictofBigram.items():
            # comparision of last word of inputSentence and firstWord of each items of bigram Model
            if (firstWord == lastWordofSentence):
                # matches found then print whole sentence
                print 'Next Word is:', nextWord
                print 'Complete Sentence:', inputSentence, nextWord
                flag = True
                break
        if (flag != True):
            print 'matches not found!'
    except Exception, e:
        print 'Error', str(e)


# ====================== function predictWordUsingBigramModel over ======================

'''
This predictWordUsingTrigramModel function is for predicting next word in a sentence using TrigramModel
param: dictionary model of trigram and inputSentence
'''


# ====================== function predictWordUsingTrigramModel start ======================
def predictWordUsingTrigramModel(dictofTrigram, inputSentence):
    try:
        # last word
        lastWordofSentence = inputSentence.split()[-1].lower()
        # second last word
        secondLastWordofSentence = inputSentence.split()[-2].lower()

        # flag is to check any matches found or not
        flag = False

        # dicofBigram list is in form of [((firstWord,middleWord,nextWord),occurrences),
        #                                 ((firstWord,middleWord,nextWord),occurrences) ]...
        for (firstWord, middleWord, nextWord), count in dictofTrigram.items():
            # comparision of second last word of inputSentence and firstWord of each items of bigram Model
            if (firstWord == secondLastWordofSentence):
                # matches found then print whole sentence
                if (middleWord == lastWordofSentence):
                    print 'Next Word is:', nextWord
                    print 'Complete Sentence:', inputSentence, nextWord
                    flag = True
                    break

        if (flag != True):
            print 'matches not found!'

    except Exception, e:
        print 'Error:', str(e)


# ====================== function predictWordUsingTrigramModel over ======================


# ====================== main function start ======================

print 'Reading Text data from file...',

# file names are predefined
inputTextFileName = "input/inputTextFile.txt"
inputWikipediaFileName = "input/inputWikipediaFile.htm"
inputPDFFileName = "input/inputPDFFile.pdf"
inputWordFileName = "input/inputWordFile.docx"
inputTweetFileName = "input/inputTweetFile.json"

# string object that hold all text content || Training Data
inputString = ""

# code of reading text file
# assign file object from input file name in reading mode
inputFile1 = open(inputTextFileName, "r")
# extract string data from file
inputString1 = inputFile1.read()
# freeup resources
inputFile1.close()

# code of reading html file
# assign file object from input file name in reading mode
inputFile2 = open(inputWikipediaFileName, "r")
# parse html file using BeautifulSoup
soup = BeautifulSoup(inputFile2, 'html.parser')
# extract data from file
inputString2 = ''.join(soup.findAll(text=True))
# freeup resources
inputFile2.close()

# code of reading pdf file
# assign file object from input file name in reading binary mode
inputFile3 = open(inputPDFFileName, "rb")
# read pdf file using PdfFileReader class
pdfFile = PdfFileReader(inputFile3)
# total number of pages in pdf file
totalPages = pdfFile.getNumPages()
inputString3 = ""
# extract data from all the pages
for index in range(totalPages):
    inputString3 += pdfFile.getPage(index).extractText()
# freeup resources
inputFile3.close()

# code of reading doc file
# assign file object from input file name in reading binary mode
inputFile4 = open(inputWordFileName, "rb")
# parse document file using Document class
document = Document(inputFile4)
inputString4 = ""
# extract data from all the paragraphs
for para in document.paragraphs:
    inputString4 += para.text
# freeup resources
inputFile4.close()

# code of reading tweets from json file
# assign file object from input file name in reading mode
inputFile5 = open(inputTweetFileName, "r")
# parse tweets file using json class
jsonData = json.load(inputFile5)
inputString5 = ""
# json structure ref: https://dev.twitter.com/rest/reference/get/statuses/user_timeline
# extract data from each json object in an json array
for i in range(len(jsonData)):
    # where text is key value of json object in an Array
    inputString5 += jsonData[i]["text"]
# freeup resources
inputFile5.close()

# for case ignore convert whole string to lower case
# reading only wrords, non ascii and symbols are ignored
allTokens = re.sub('[^\w]', ' ', inputString1).split()
allTokens += re.sub('[^\w]', ' ', inputString2).split()
allTokens += re.sub('[^\w]', ' ', inputString3).split()
allTokens += re.sub('[^\w]', ' ', inputString4).split()
allTokens += re.sub('[^\w]', ' ', inputString5).split()

# sample text for testing || training data
# inputString = 'This is data This is sample String This is sample'
print 'done.'

print 'Model building...',

# model construction of bigrams using nltk library
# inpnut of bigrams is tokens in order
bigramModel = list(nltk.bigrams(allTokens))
# sample of bigram model is like [('this','is'), ('is','data')]...

# model construction of trigram using nltk library
# inpnut of trigram is tokens in order
trigramModel = list(nltk.trigrams(allTokens))
# sample of trigram model is like [('this','is','data'), ('is','data','this')]...

# Dictionary construction based on occurrences and in descending order
# it's like high occurrences word pairs are bubbled up
dictofBigram = OrderedDict(Counter(bigramModel).most_common())
dictofTrigram = OrderedDict(Counter(trigramModel).most_common())

print 'done.'

# print  dictofBigram
# print dictofTrigram

userInputString = '\nEnter your input for Predict word Using:\n' \
                  '1. Bigram Model\n' \
                  '2. Trigram Model\n' \
                  '3. Exit\n' \
                  'Enter Your Choice:'

while True:
    choice = raw_input(userInputString)
    if (choice.isdigit()):
        if (choice == '1'):
            # ask user to input string
            inputSentence = raw_input('Enter string:')
            predictWordUsingBigramModel(dictofBigram, inputSentence)

        elif (choice == '2'):
            # ask user to input string
            inputSentence = raw_input('Enter string:')
            predictWordUsingTrigramModel(dictofTrigram, inputSentence)

        elif (choice == '3'):
            print 'Thanks for Stopping by'
            break
        else:
            print "Seems like you are tired\nHint: Enter 3"
    else:
        # user input is other than integer
        print "This program is recognize only integer input.\ntry again with integer value."

    # continue loop logic
    wantToContinue = raw_input('\ndo Want to Continue? (Y/N)')
    if (wantToContinue.lower()) != 'y':
        break

# ====================== main function over ======================
