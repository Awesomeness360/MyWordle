import random
import sys


def debug():
    return False

def randomID(a):
    return random.randint(1, a)    

def selectWord(ID, listOfWords):
    i = listOfWords[ID - 1]
    return i

def wordArray(word):
    lst = []
    i = 0
    while (i < len(word)):
        lst.append(word[i])
        i += 1
    return lst

def contains(ch, st):
    i = 0
    while (i < len(st)):
        if (st[i] == ch):
            return True
        i += 1
    return False

def filterWords(checkString, lastGuess, badLetters, words):
    validWords = []
    i = 0
    while (i < len(words)):
        if (filterWord(checkString, lastGuess, badLetters, words[i])):
            validWords.append(words[i])
        i += 1
    return validWords

def filterWord(checkString, lastGuess, badLetters, word):
    i = 0
    while (i < len(lastGuess)):
        if (checkString[i] == 'G'):
            if (lastGuess[i] != word[i]):
                return False
        i += 1
    i = 0
    while (i < len(badLetters)):
        if (contains(badLetters[i], word)):
            return False
        i += 1
    i = 0
    while (i < len(checkString)):
        if (checkString[i] == 'Y'):
            if (not contains(lastGuess[i], word)):
                return False
        i += 1
    return True

def guessCheck(guessString, answerString):
    checkString = []
    i = 0    
    while (i < len(guessString)):
        if (answerString[i] == guessString[i]):
            checkString += 'G'
        elif (contains(guessString[i], answerString)):
            checkString += 'Y'
        else:
            checkString += 'X'
        i += 1
    return checkString

def enterGuess():
    guessString = wordArray(str(input("Enter Guess Here:")))
    return guessString

def pickAnswer(lst):
    word = selectWord(randomID(len(lst)), lst)
    return word

def importFile(fileName):
    file = open(fileName, "rt")
    data = file.read()
    words = data.split()
    return words


def isLowercase(ch):
    nch = ord(ch)
    if (nch > 96 and nch < 123):
        return True
    else:
        return False

def isUppercase(ch):
    nch = ord(ch)
    if (nch > 64 and nch < 91):
        return True
    else:
        return False

def isLetter(ch):
    return isLowercase(ch) or isUppercase(ch)

def makeCharacterCap(ch):
    if (isLetter(ch)):
        if (isUppercase(ch)):
            return ch
        else:
            return chr(ord(ch) - 32)
    else:
        return ch

def makeWordAllCaps(word):
    i = 0
    wordCap = ""
    while (i < len(word)):
        wordCap += makeCharacterCap(word[i])
        i += 1
    return wordCap

def makeRandomGuess(listOfWords):
    if (len(listOfWords) >= 1):
        return selectWord(randomID(len(listOfWords)), listOfWords)
    else:
        return False

def printArray(listOfNumbers):
    stringOfNumbers = ""
    i = 0
    lengthOfList = len(listOfNumbers)
    while (i < lengthOfList):
        stringOfNumbers += str(listOfNumbers[i])
        if (i + 1 != lengthOfList):
            stringOfNumbers += ', '
        i += 1
    return stringOfNumbers

def heuristicOne(word, letterArray):
    wordScore = 0
    i = 0
    while (i < len(word)):
        wordScore += letterArray[ord(word[i]) - 97]
        i += 1
    return wordScore

def heuristicTwo(word, letterArray):
    wordScore = 0    
    if (debug()):
        print ("heuristicTwo: word is", word)
        print ("heuristicTwo: letterArray is", letterArray)
    i = 0
    while (i < len(letterArray)):
        if (contains(chr(i + 97), word)):
            wordScore += letterArray[i]
        i += 1
    return wordScore

def heuristicThree(word, lettersInOrder):
    wordScore = 0    
    if (debug()):
        print ("heuristicThree: word is", word)
        print ("heuristicThree: lettersInOrder are", lettersInOrder)
    i = 0
    while (i < 26):
        if (contains(lettersInOrder[i], word)):
            wordScore += 26 - i
        i += 1
    if (debug()):
        print ("wordScore for", word, "is", wordScore)
    return wordScore

def heuristicFour(word, lettersInOrder):
    wordScore = 0    
    if (debug()):
        print ("heuristicFour: word is", word)
        print ("heuristicFour: lettersInOrder are", lettersInOrder)
    i = 0
    while (i < 26):
        if (contains(lettersInOrder[i], word)):
            wordScore += 2**(26 - i)
        i += 1
    if (debug()):
        print ("wordScore for", word, "is", wordScore)
    return wordScore

def maxIndex(listOfNumbers):
    maximum = max(listOfNumbers)
    return listOfNumbers.index(maximum)

def wordScoresInOrder(listOfWords, listOfScores):
    finalListOfWords = []
    lengthOfList = len(listOfWords)
    i = 0    
    while (i < lengthOfList):
        index = maxIndex(listOfScores)
        bestWord = listOfWords[index]
        finalListOfWords.append(bestWord)
        listOfWords = removeItem(listOfWords, index)
        listOfScores = removeItem(listOfScores, index)
        i += 1
    return finalListOfWords

def letterScoresInOrder(listOfLetters, listOfScores):
    if (debug()):
        print ("listOfLetters is", listOfLetters)
        print ("listOfScores is", listOfScores)
    finalListOfWords = []
    lengthOfList = len(listOfLetters)
    i = 0    
    while (i < lengthOfList):
        index = maxIndex(listOfScores)
        if (debug()):
            print ("index is", index)
        bestWord = listOfLetters[index]
        if (debug()):
            print ("letterScoresInOrder: bestWord is", bestWord)
        finalListOfWords.append(bestWord)
        listOfLetters = removeItem(listOfLetters, index)
        listOfScores = removeItem(listOfScores, index)
        i += 1
    return finalListOfWords


def numberScoresInOrder(fileName):
    finalListOfScores = []
    listOfWords = importFile(fileName)
    listOfScores = letterScoreCurve(fileName)
    lengthOfList = len(listOfScores)
    i = 0    
    while (i < lengthOfList):
        index = maxIndex(listOfScores)
        bestLetter = chr(index + 97)
        if (debug()):
            print ("Choice #",i+1, "is", bestLetter)
        finalListOfScores.append(bestLetter)
        newLenghtOfList = len(listOfScores)
        if (newLenghtOfList == 1):
            break
        else:
            listOfScores = removeItem(listOfScores, index)
            listOfWords = removeItem(listOfWords, index)
            i += 1
    return finalListOfScores

def letterScoreCurve(fileName):
    listOfWords = importFile(fileName)
    scoreArray = []
    i = 0
    while (i < 26):
        scoreArray.append(0)
        i += 1
    j = 97
    while (j < 123):
        i = 0
        while (i < len(listOfWords)):
            if (contains(chr(j), listOfWords[i])):
                scoreArray[j - 97] += 1 
            i += 1
        j += 1
    return scoreArray

def copyList(lst):
    newList = []
    i = 0
    while (i < len(lst)):
        newList.append(lst[i])
        i += 1
    return newList

def removeItem(lst, index):
    newLst = copyList(lst)
    del newLst[index]
    return newLst

def playGameRandom(fileName):
    listOfWords = importFile(fileName)
    i = 0
    while (i < len(listOfWords)):
        answer = listOfWords[i]
        k = 0
        listOfAmountOfGuesses = []
        while (k < 10):
            if (debug()):
                print ("Answer is", makeWordAllCaps(answer))
                print ("Length of listOfWords is", len(listOfWords))
            guess = makeRandomGuess(listOfWords)
            if (debug()):
                print ("Guess 1 is", makeWordAllCaps(guess))
            checkString = guessCheck(guess, answer)
            if (debug()):
                print (checkString)
            badLetters = []
            amountOfGuesses = 1
            while (guess != answer):
                j = 0
                while (j < len(checkString)):
                    if (checkString[j] == 'X'):
                        badLetters += guess[j]
                    j += 1
                validWords = filterWords(checkString, guess, badLetters, listOfWords)
                if (len(validWords) > 1):
                    if (debug()):
                        print ("validWords size is:", len(validWords), "and the first two words are", makeWordAllCaps(validWords[0]), "and", makeWordAllCaps(validWords[1]))
                else:
                    if (debug()):
                        print ("validWords size is:", len(validWords))
                if (debug()):
                    print ("badLetters are:", badLetters)
                guess = makeRandomGuess(validWords)
                amountOfGuesses += 1
                if (debug()):
                    print ("Guess", amountOfGuesses, "is", makeWordAllCaps(guess))
                checkString = guessCheck(makeWordAllCaps(guess), makeWordAllCaps(answer))
                if (debug()):
                    print (checkString)
            listOfAmountOfGuesses.append(amountOfGuesses)
            k += 1
        print (makeWordAllCaps(answer),',', printArray(listOfAmountOfGuesses))   
        i += 1

def playGameHeuristicOne(fileName):
    listOfWords = importFile(fileName)
    listOfScores = []
    i = 0
    letterScores = letterScoreCurve(fileName)    
    if (debug()):
        print ("letterScores are", letterScores)
    while (i < len(listOfWords)):
        heuristic = heuristicOne(listOfWords[i], letterScores)
        if (debug()):
            print (heuristic)
        listOfScores.append(heuristic)
        i += 1
        if (debug()): 
            print ("listofScores is:", listOfScores)
    i = 0
    listOfWordsInOrder = wordScoresInOrder(listOfWords, listOfScores)
    if (debug()):
        print (listOfWordsInOrder)
    if (debug()):
        print ("Before While Loop: listOfScores is", listOfScores)
        print ("Before While Loop: listOfWordsInOrder is", listOfWordsInOrder)
    while (i < len(listOfWords)):
        answer = listOfWords[i]
        if (debug()):
            print ("In While Loop: answer is", makeWordAllCaps(answer))
            print ("In While Loop: length of listOfWords is", len(listOfWords))
        guess = listOfWordsInOrder[0]
        if (debug()):
            print ("Guess 1 is", guess)
        checkString = guessCheck(guess, answer)
        if (debug()):
            print (checkString)
        badLetters = []
        validWords = listOfWordsInOrder
        amountOfGuesses = 1
        while (guess != answer):
            j = 0
            while (j < len(checkString)):
                if (checkString[j] == 'X'):
                    badLetters += guess[j]
                j += 1
            k = 0
            l = 0
            while (k < len(checkString)):
                if (checkString[k] != 'X'):
                    if (l + 1 == len(checkString)):
                        validWords = removeItem(validWords, 0)
                    else:
                        l += 1
                k += 1
            else:
                validWords = filterWords(checkString, guess, badLetters, validWords)
            if (debug()):
                print ("In While Loop: validWords are:", validWords)
            guess = validWords[0]
            if (debug()):
                print ("badLetters are:", badLetters)
            amountOfGuesses += 1
            checkString = guessCheck(makeWordAllCaps(guess), makeWordAllCaps(answer))
            if (checkString != ['G', 'G', 'G', 'G']):
                if (debug()):
                    print ("Guess", amountOfGuesses, "is", makeWordAllCaps(guess))
            if (debug()):
                print (checkString)
        if (debug()):
            print (makeWordAllCaps(answer),",", amountOfGuesses)
        i += 1
    return listOfWordsInOrder


def playGameHeuristicTwo(fileName):
    listOfWords = importFile(fileName)
    listOfScores = []
    i = 0
    letterScores = letterScoreCurve(fileName)    
    if (debug()):
        print ("letterScores are", letterScores)
    while (i < len(listOfWords)):
        heuristic = heuristicTwo(listOfWords[i], letterScores)
        if (debug()):
            print (heuristic)
        listOfScores.append(heuristic)
        i += 1
        if (debug()):
            print ("listofScores is:", listOfScores)
    i = 0
    listOfWordsInOrder = wordScoresInOrder(listOfWords, listOfScores)
    if (debug()):
        print (listOfWordsInOrder)
    if (debug()):
        print ("Before While Loop: listOfScores is", listOfScores)
        print ("Before While Loop: listOfWordsInOrder is", listOfWordsInOrder)
    while (i < len(listOfWords)):
        answer = listOfWords[i]
        if (debug()):
            print ("In While Loop: answer is", makeWordAllCaps(answer))
            print ("In While Loop: length of listOfWords is", len(listOfWords))
        guess = listOfWordsInOrder[0]
        if (debug()):
            print ("Guess 1 is", guess)
        checkString = guessCheck(guess, answer)
        if (debug()):
            print (checkString)
        badLetters = []
        validWords = listOfWordsInOrder
        amountOfGuesses = 1
        while (guess != answer):
            j = 0
            while (j < len(checkString)):
                if (checkString[j] == 'X'):
                    badLetters += guess[j]
                j += 1
            k = 0
            l = 0
            while (k < len(checkString)):
                if (checkString[k] != 'X'):
                    if (l + 1 == len(checkString)):
                        validWords = removeItem(validWords, 0)
                    else:
                        l += 1
                k += 1
            else:
                validWords = filterWords(checkString, guess, badLetters, validWords)
            if (debug()):
                print ("In While Loop: validWords are:", validWords)
            guess = validWords[0]
            if (debug()):
                print ("badLetters are:", badLetters)
            amountOfGuesses += 1
            checkString = guessCheck(makeWordAllCaps(guess), makeWordAllCaps(answer))
            if (checkString != ['G', 'G', 'G', 'G']):
                if (debug()):
                    print ("Guess", amountOfGuesses, "is", makeWordAllCaps(guess))
            if (debug()):
                print (checkString)
        if (debug()):
            print (makeWordAllCaps(answer),",", amountOfGuesses)
        i += 1
    return listOfWordsInOrder

def playGameHeuristicThree(fileName):
    listOfLetterScores = letterScoreCurve(fileName)
    listOfLetters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    listOfLettersInOrder = letterScoresInOrder(listOfLetters, listOfLetterScores)
    if (debug()):
        print ("list is", listOfLettersInOrder)
    listOfWords = importFile(fileName)
    listOfWordScores = []
    i = 0
    while (i < len(listOfWords)):
        wordScore = heuristicThree(listOfWords[i], listOfLettersInOrder)
        listOfWordScores.append(wordScore)
        i += 1
    listOfWordsInOrder = wordScoresInOrder(listOfWords, listOfWordScores)
    if (debug()):
        print (listOfWordsInOrder)
    i = 0
    while (i < len(listOfWords)):
        answer = listOfWords[i]
        if (debug()):
            print ("In While Loop: answer is", makeWordAllCaps(answer))
            print ("In While Loop: length of listOfWordsInOrder is", len(listOfWordsInOrder))
        guess = listOfWordsInOrder[0]
        if (debug()):
            print ("Guess 1 is", guess)
        checkString = guessCheck(guess, answer)
        if (debug()):
            print (checkString)
        badLetters = []
        validWords = listOfWordsInOrder
        amountOfGuesses = 1
        while (guess != answer):
            j = 0
            while (j < len(checkString)):
                if (checkString[j] == 'X'):
                    badLetters += guess[j]
                j += 1
            k = 0
            l = 0
            while (k < len(checkString)):
                if (checkString[k] != 'X'):
                    if (l + 1 == len(checkString)):
                        validWords = removeItem(validWords, 0)
                    else:
                        l += 1
                k += 1
            else:
                validWords = filterWords(checkString, guess, badLetters, validWords)
            if (debug()):
                print ("In While Loop: validWords are:", validWords)
            guess = validWords[0]
            if (debug()):
                print ("badLetters are:", badLetters)
            amountOfGuesses += 1
            checkString = guessCheck(makeWordAllCaps(guess), makeWordAllCaps(answer))
            if (checkString != ['G', 'G', 'G', 'G']):
                if (debug()):
                    print ("Guess", amountOfGuesses, "is", makeWordAllCaps(guess))
            if (debug()):
                print (checkString)
        if (debug()):
            print (makeWordAllCaps(answer),",", amountOfGuesses)
        i += 1 
    return listOfWordsInOrder           


def playGameHeuristicFour(fileName):
    listOfLetterScores = letterScoreCurve(fileName)
    listOfLetters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    listOfLettersInOrder = letterScoresInOrder(listOfLetters, listOfLetterScores)
    if (debug()):
        print ("list is", listOfLettersInOrder)
    listOfWords = importFile(fileName)
    listOfWordScores = []
    i = 0
    while (i < len(listOfWords)):
        wordScore = heuristicFour(listOfWords[i], listOfLettersInOrder)
        listOfWordScores.append(wordScore)
        i += 1
    listOfWordsInOrder = wordScoresInOrder(listOfWords, listOfWordScores)
    if (debug()):
        print (listOfWordsInOrder)
    i = 0
    while (i < len(listOfWords)):
        answer = listOfWords[i]
        if (debug()):
            print ("In While Loop: answer is", makeWordAllCaps(answer))
            print ("In While Loop: length of listOfWordsInOrder is", len(listOfWordsInOrder))
        guess = listOfWordsInOrder[0]
        if (debug()):
            print ("Guess 1 is", guess)
        checkString = guessCheck(guess, answer)
        if (debug()):
            print (checkString)
        badLetters = []
        validWords = listOfWordsInOrder
        amountOfGuesses = 1
        while (guess != answer):
            j = 0
            while (j < len(checkString)):
                if (checkString[j] == 'X'):
                    badLetters += guess[j]
                j += 1
            k = 0
            l = 0
            while (k < len(checkString)):
                if (checkString[k] != 'X'):
                    if (l + 1 == len(checkString)):
                        validWords = removeItem(validWords, 0)
                    else:
                        l += 1
                k += 1
            else:
                validWords = filterWords(checkString, guess, badLetters, validWords)
            if (debug()):
                print ("In While Loop: validWords are:", validWords)
            guess = validWords[0]
            if (debug()):
                print ("badLetters are:", badLetters)
            amountOfGuesses += 1
            checkString = guessCheck(makeWordAllCaps(guess), makeWordAllCaps(answer))
            if (checkString != ['G', 'G', 'G', 'G']):
                if (debug()):
                    print ("Guess", amountOfGuesses, "is", makeWordAllCaps(guess))
            if (debug()):
                print (checkString)
        if (debug()):
            print (makeWordAllCaps(answer),",", amountOfGuesses)
        i += 1
    return listOfWordsInOrder  

def testLoop(lst):
    i = 0
    listOfNumbers = []
    while (i < len(lst)):
        listOfNumbers.append(heuristicOne(lst[i], letterScore(lst)))
        print (heuristicOne(lst[i], letterScore(lst)))
        i += 1
    return wordScoresInOrder(lst, listOfNumbers)


lst = [2, 8, 6, 1, 3, 4, 5, 10, 7, 9]
fakeListOfWords = ['word', 'bell', 'tire', 'five']
game = playGameHeuristicFour(sys.argv[1])
print (game)
#listOfScores = letterScoreCurve(sys.argv[1])
#test = wordScoresInOrder(listOfWords, listOfScores)
#print (test)
#word = 'ties'
#print (copyList(lst))
#print (maxIndex(lst))
#del lst[maxIndex(lst)]
#print (lst)
#print ("heuristicOne Score of", word, "is", heuristicOne(word, letterScore(sys.argv[1])))
#print ("letterScore output is:", letterScore(sys.argv[1]))
#print ("Random Stratagy:", sys.argv[1])
#playGameRandom(sys.argv[1])
#print (makeWordAllCaps('tHerE  I'))