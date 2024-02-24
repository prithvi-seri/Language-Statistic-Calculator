myFile =  open('AroundTheWorldIn80Days.txt', 'r')
import nltk

def wordLengthDistribution():
    global words
    words = [token for token in nltk.tokenize.word_tokenize(text) if sum(char.isalpha() for char in token)] # filter out non-word tokens (there are a lot of .....s in the book)
    lengthDistribution = {}
    for word in words:
        if len(word) in lengthDistribution:
            lengthDistribution[len(word)] += 1
        else: lengthDistribution[len(word)] = 1
    
    print('Word Length Distribution:')
    for length in sorted(lengthDistribution.keys()):
        print(f'{length}: {lengthDistribution[length]}')
    print()

def partOfSpeechDistribution():
    posList = nltk.pos_tag(words)
    posFreqList = {'Nouns': 0, 'Pronouns': 0, 'Verbs': 0, 'Adjectives': 0, 'Adverbs': 0, 'Conjunctions': 0, 'Prepositions': 0, 'Determiners': 0, 'Interjections': 0}
    for i in range(len(posList)):
        pos = posList[i][1]
        first = pos[0]  # first char of position indicator
        if first == 'N': posFreqList['Nouns'] += 1
        if pos[:2] == 'PR' or pos == 'WP': posFreqList['Pronouns'] += 1
        if first == 'V' or pos == 'MD': posFreqList['Verbs'] += 1
        if first == 'J' or pos == 'CD': posFreqList['Adjectives'] += 1
        if first == 'R' or pos == 'WRB': posFreqList['Adverbs'] += 1
        if pos == 'CC': posFreqList['Conjunctions'] += 1                            # need to add a second condition for when pos == 'IN' (might be a conjunction, not just a preposition)
        if pos == 'IN' or pos == 'TO' and posList[i+1][1][0] != 'V': posFreqList['Prepositions'] += 1   # second condition: word after 'to' is not a verb (avoids including infinitives)
        if pos[-2:] == 'DT': posFreqList['Determiners'] += 1
        if pos == 'UH': posFreqList['Interjections'] += 1

    print('Part of Speech Distribution (all words):')
    for pos in posFreqList:
        print(f'{pos}: {posFreqList[pos]}')
    print()

def numQuotes():
    quotedPassages = []
    inQuote = False
    passage = []
    for i in range(len(text)):
        if text[i] == '"' and (inQuote or not text[i + 1] == ' '): # second condition avoids when quotation marks are used to mean ditto in the novel
            if not inQuote:     # opening quotation mark
                passage = []
            else:           # closing quotation mark
                quotedPassages.append(''.join(passage))
            inQuote = not inQuote
        else:
            if inQuote: passage.append(text[i])      
    quotedPassages.remove('City')   # only time non-dialogue quote pair is used
    
    print(f'Number of Quoted Passages: {len(quotedPassages)}')
    print()

def identifySpeakers():     # NOT WORKING
    global text
    quotedPassages = []     # (passage, speaker)
    inQuote = False
    passage = []
    start = 0
    end = 0
    for i in range(len(text)):
        if text[i] == '"' and (inQuote or not text[i + 1] == ' ') and not (814 <= i <= 819): # second condition avoids when quotation marks are used to mean ditto in the novel
                                                                            # avoid "City"
            if not inQuote:     # opening quotation mark
                passage = []
                start = i
            else:           # closing quotation mark
                end = i
                x = 0
                while True:
                    def innerloop():
                        for idx in (start - x, end + x):
                            if 0 <= idx < len(text) and text[idx].isupper():
                                speaker = []
                                while text[idx] != ' ' and not text[idx + 1].isupper:       # NOT WORKING
                                    speaker.append(text[idx])
                                    idx += 1
                                return ''.join(speaker)
                        return None
                    speaker = innerloop()
                    if speaker: break
                    x += 1
                quotedPassages.append((''.join(passage), speaker))
            inQuote = not inQuote
        else:
            if inQuote: passage.append(text[i])
    
    print(f'Number of Quoted Passages: {len(quotedPassages)}')
    print()

def main():
    global text
    text = myFile.read().replace('\n', ' ')
    myFile.close()
    wordLengthDistribution()
    partOfSpeechDistribution()
    numQuotes()
    #identifySpeakers()

if __name__ == '__main__': main()