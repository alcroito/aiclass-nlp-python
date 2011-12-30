__author__ = 'Placinta'

import re, collections, math

class Models:
    def __init__(self):
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'

    def words(self, text): return re.findall('[a-z]+', text.lower())

    def corpusAsText(self):
        with open('corpus/big.txt', 'r') as f:
            text = f.read()
        text += ' '
        with open('corpus/words.txt', 'r') as f:
            text += f.read()
        text += ' '
        with open('corpus/additional.txt', 'r') as f:
            text += f.read()
        return text

    def trainWordUnigramModel(self, features):
        model = collections.defaultdict(lambda: 1)
        for f in features:
            model[f] += 1
        return model

    def createWordUniGramModel(self):
        self.unigram = self.trainWordUnigramModel(self.words(self.corpusAsText()))
        self.word_count = len(self.unigram)

    def getWordProbability(self, phrase):
        words = phrase.split(' ')
        joint_probability = 1
        for word in words:
            joint_probability += math.log(float(self.unigram[word]) / self.word_count)
        return joint_probability

    def iterate_lines(self, foo): return iter(foo.splitlines())

    def letterNgrams(self, text, number_of_chars = 5): # 5,9 <- worked
        ngram = ''
        list_of_ngrams = []
        for character in text:
            if character not in self.alphabet:
                list_of_ngrams.append(ngram)
                ngram = ''
                continue
            ngram = ngram + character
            if len(ngram) == number_of_chars:
                #yield ngram
                list_of_ngrams.append(ngram)
                ngram = ngram[number_of_chars - 1]
        return list_of_ngrams

    def trainLetterNgrams(self, features):
        model = collections.defaultdict(lambda: 1)
        for f in features:
            model[f] += 1
        return model

    def createLetterModel(self):
        text = self.corpusAsText()
        self.letter_ngram = self.trainLetterNgrams(self.letterNgrams(text.lower()))
        self.ngram_count = len(self.letter_ngram)

    def sliceDict(self, d, s):
        return {k:v for k,v in d.iteritems() if k.startswith(s)}

    def getWordProbabilities(self, phrase):
        words = phrase.split(' ')
        joint_probability = 0
        i = 0
        for word in words:
            i += 1
            if word == '':
                continue
            count = self.unigram[word]
            joint_probability += math.log10(float(count) / self.word_count)
        return joint_probability

    def getLetterProbabilities(self, phrase):
        words = phrase.split(' ')
        nr_of_words = len(words)
        joint_probability = 0
        i = 0
        for word in words:
            i += 1
            if i == nr_of_words:
                count = sum(self.sliceDict(self.letter_ngram, word).itervalues())
                if not count:
                    count = 1
            else:
                count = self.letter_ngram[word]
            if word == '':
                count = 1
            joint_probability += math.log10(float(count) / self.ngram_count)
        return joint_probability