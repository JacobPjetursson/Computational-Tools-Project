import mmh3
from bitarray import bitarray
import math


class BloomFilter:

    def __init__(self, m=None, A=None):
        self.fpr = 0.001
        if A:
            self.n = len(A)
            self.A = A
        else:
            self.n = self.getFilterSize(m)
            self.A = bitarray(self.n)
            self.A.setall(False)
            # Ensure multiple of 8
            self.A.fill()
            self.n = len(self.A)
        # K is (almost) always 7 with fpr=0.01
        self.k = 10

    def train(self, sentences):
        for sentence in sentences:
            for i in range(self.k):
                j = mmh3.hash(sentence, i, signed=True) % self.n
                self.A[j] = True

    def classify(self, sentences):
        totalSentences = len(sentences)
        plagiarizedSentences = 0
        for sentence in sentences:
            match = True
            for i in range(self.k):
                j = mmh3.hash(sentence, i, signed=True) % self.n
                if not self.A[j]:
                    match = False
            if match:
                plagiarizedSentences += 1
        plagiarism_percent = (float(plagiarizedSentences) / float(totalSentences)) * 100
        return plagiarism_percent

    def getFilterSize(self, m):
        n = (m * abs(math.log(self.fpr))) / (math.log(2) ** 2)
        return int(math.ceil(n))

    def saveFilter(self, fileName):
        with open(fileName, 'wb+') as f:
            self.A.tofile(f)

def loadFilter(fileName):
    bitarr = bitarray()
    with open(fileName, 'rb') as f:
        bitarr.fromfile(f)

    return BloomFilter(A=bitarr)


def prepare_sentences(article):
    sentences = []
    for line in article.split("\n"):
        if line:
            for sentence in line.split("."):
                if sentence.startswith(" ") and len(sentence) > 1:
                    sentence = sentence[1:]
                if sentence.endswith(" ") and len(sentence) > 1:
                    sentence = sentence[:-1]
                if len(sentence) > 1 and len(sentence.split(" ")) > 1:
                    sentences.append(sentence)
    return sentences
