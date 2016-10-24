# -*- coding: utf-8 -*-
"""
Created on Feb 4, 2016

Identify and expand abbreviations in text.

@author: Jason Hays (jhays006)
"""

import re
from nltk.stem import PorterStemmer as Stemmer


class PhraseFinder(object):
    def __init__(self):
        self.s = Stemmer()
        # some of the same regex pieces are used in the makeAbbRegex function
        self.abbreviationRE = re.compile("\\(([A-Z]+)s?[\\);]", re.MULTILINE)
        self.wordPicker = re.compile("([A-z0-9\-]+('s|s')?)([^A-z0-9\-]*)", re.MULTILINE)
        self.fullText = ""
        
    def setup(self, fText):
        self.fullText = fText
        self.expandAbbreviatedTerms()
        
    def expandAbbreviatedTerms(self):
        f = re.finditer(self.abbreviationRE, self.fullText)
        for match in f:
            if match is not None:
                abR = self.makeAbbRegex(match)
                abb = match.group(1)
                fullword = re.search(abR, self.fullText)
                #print fullText
                if fullword is not None:
                    #print "full word",fullword.group(1)
                    self.replaceWordAwithB(abb, fullword.group(1)[:-1])
                else:
                    print "Empty", abb
                
    def doWordsMatch(self, A, B):
        return self.s.stem(A) == self.s.stem(B)
    
    def replaceWordAwithB(self, A, B):
        match = -1
        startIndex = 0
        while match is not None or match == -1:
            match = re.search(self.wordPicker, self.fullText[startIndex:])
            if match is not None: 
                if self.doWordsMatch(match.group(1), A):
                    wordStart = startIndex + match.start()
                    self.fullText = self.fullText[:wordStart] + B + self.fullText[wordStart+len(match.group(1)):]
                    
                startIndex += match.end()
            
    def makeAbbRegex(self, abbMatch):
        abb = abbMatch.group(1)
        regex = ""
        separators = "[A-z]*('s)?)(\\s((a|of|are|with|the|in|to)\\s)?|-[A-z]*)?"
        for index, c in enumerate(abb):
            regex += "((["+c.upper() + c.lower()+"]"+separators+")"
            if index > 0:
                regex+="?"
        regex = "("+regex+")"
        regex += "\\("+abbMatch.group()[1:-1]+"[\\);]"
        return re.compile(regex, re.MULTILINE)
    
    def garbage(self, length):
        # create a garbage string of the length "length"
        string = ""
        for i in range(length):
            string += "#"
        return string
    
    
    def getAbbreviations(self, text):
        global abbreviationRE
        arr = []
        f = re.finditer(abbreviationRE, text)
        for match in f:
            if match is not None:
                arr.append(match.group(1))
        return arr
    
    def getWords(self, text):
        global wordPicker
        arr = []
        f = re.finditer(self.wordPicker, text)
        for match in f:
            if match is not None:
                arr.append(match)
        return arr
    
    def getStemmedText(self, text):
        global wordPicker
        words = self.getWords(text)
        stemmedText = ""
        
        for word in words:
            stemmed = word.group(1)
            stemmed = self.s.stem(stemmed).lower()
            stemmedText += stemmed + word.group(3)
    
        return stemmedText
    
    def findText(self, phrase, replacement):
        # needs to find the phrase within 1 sentence
        # stems the words that are not all caps abbreviations
        # this should pull out task types, but not phrases that are rearranged
        # also, remove phrases as you go so that "working memory" and "memory"
        #  are not both hits.  Make sure to do longer phrases first.
        strPattern = "("
        # find any non punctuation followed by a punctuation.
        # finds the rest of the sentence, was probably only useful as I originally intended to implement it
        #patternEnd = "[^\\(\.!\?\\)\"]*[\"\\(\\)\.!\?]"
        words = phrase.split(" ")
        for index, word in enumerate(words):
            stemmed = word
            if word != word.upper():
                stemmed = self.s.stem(word)
                #print stemmed
            if index > 0:
                strPattern+="\s"
            strPattern += stemmed
        strPattern += ")"#+ patternEnd

        pat = re.compile(strPattern, re.MULTILINE)
        
        matches = re.finditer(pat, self.fullText)
        counter = 0
        #!!!!!!!!!!!!!!!! if you replace the garbage generator with
        #  the term ids, you will need to make sure to alter
        #  re.finditer to re.search where you change the input string.
        #  because the length of the terms varies, 
        #    you will mess up the later matches' indexing.
        #  Alternatively, you can put the finditer results into 
        #   a list and replace the terms starting from the end.
        #  (fyi, findall doesn't give match objects, just the string match)
        # use the sub method in the future
        for match in matches:
            if match is not None:
                self.fullText = self.fullText[:match.start()] + self.garbage(len(match.group(1))) + self.fullText[match.end(1):]
                counter += 1
        return counter
