__author__ = 'Placinta'

from Models import Models
from Combination import Combination
import copy

class Unshred:
    def __init__(self, verbose = False):
        self.encrypted_string = (
                  "de|  | f|Cl|nf|ed|au| i|ti|  |ma|ha|or|nn|ou| S|on|nd|on" "\n"
                  "ry|  |is|th|is| b|eo|as|  |  |f |wh| o|ic| t|, |  |he|h " "\n"
                  "ab|  |la|pr|od|ge|ob| m|an|  |s |is|el|ti|ng|il|d |ua|c " "\n"
                  "he|  |ea|of|ho| m| t|et|ha|  | t|od|ds|e |ki| c|t |ng|br" "\n"
                  "wo|m,|to|yo|hi|ve|u | t|ob|  |pr|d |s |us| s|ul|le|ol|e " "\n"
                  ' t|ca| t|wi| M|d |th|"A|ma|l |he| p|at|ap|it|he|ti|le|er' "\n"
                  'ry|d |un|Th|" |io|eo|n,|is|  |bl|f |pu|Co|ic| o|he|at|mm' "\n"
                  "hi|  |  |in|  |  | t|  |  |  |  |ye|  |ar|  |s |  |  |. ")
        self.rows = 8
        self.columns = 19
        self.matrix = [ [ 0 for i in range(self.columns) ] for j in range(self.rows) ]
        self.combination = Combination(self.rows, self.columns)
        self.used_column_indices = []
        self.verbose = verbose

    def iterate_lines(self, foo): return iter(foo.splitlines())

    def parseIntoMatrix(self):
        i = 0
        for line in self.iterate_lines(self.encrypted_string):
            row_values = line.split('|')
            for j, value in enumerate(row_values):
                if value != '':
                    self.matrix[i][j] = value
            i += 1

    def initModels(self):
        self.corp = Models()
        self.corp.createLetterModel()
        self.corp.createWordUniGramModel()

    def computeCombinationProbability(self, phrases):
        sum = 0
        for phrase in phrases:
            sum += self.corp.getLetterProbabilities(phrase)
            sum += self.corp.getWordProbabilities(phrase)
        if self.verbose:
            print '{0:15f}  |{1:s}|'.format(sum, phrases[0])
            #print sum, phrases

        return sum

    def getBestCombination(self):
        max_prob = -100000
        max_combination = ''
        max_index = 0
        for index, pair in enumerate(self.matrix[0]):
            # Don't check columns we already added
            if index in self.used_column_indices:
                continue

            temp_combination = copy.deepcopy(self.combination)

            # Get column values for index
            new_column_values = [self.matrix[i][index] for i in range(self.rows)]

            temp_combination.appendColumn(new_column_values)
            phrases_to_check = temp_combination.returnPhrases()
            # Compute probabilities
            probability = self.computeCombinationProbability(phrases_to_check)

            if probability > max_prob:
                max_prob = probability
                max_combination = temp_combination
                max_index = index
        if self.verbose:
            print '->{0:13f}  |{1:s}|'.format(max_prob, max_combination.returnFirstPhrase())

        self.used_column_indices.append(max_index)
        return max_prob, max_combination

    def unshred(self):
        # Find uppercase
        for index, pair in enumerate(self.matrix[0]):
            if pair[0].isupper():
                self.combination.appendColumn([self.matrix[i][index] for i in range(self.rows)])
                self.used_column_indices.append(index)
                break

        # Find next best combinations and append them
        for i in range(1, 19):
            prob, combination = self.getBestCombination()
            #print prob, combination
            self.combination = combination

    def displayResult(self):
        print '\n The unencrypted message is:\n'
        self.combination.display()

    def execute(self):
        self.parseIntoMatrix()
        self.initModels()
        self.unshred()
        self.displayResult()
        return

App = Unshred(verbose=True)
App.execute()