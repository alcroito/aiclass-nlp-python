__author__ = 'Placinta'

class Combination:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.used_columns = 0
        self.values = [ [ ] for j in range(self.rows) ]

    def __repr__(self):
        return self.values.__repr__()

    def __str__(self):
        return self.values.__str__()

    def appendColumn(self, values):
        for index, value in enumerate(values):
            self.values[index].append(value)
        self.used_columns += 1

    def returnFirstPhrase(self):
        return "".join(self.values[0]).lower()

    def returnPhrases(self):
        phrases = []
        for row in self.values:
            phrases.append("".join(row).lower())
        return phrases

    def display(self):
        for row in self.values:
            print "".join(row)

