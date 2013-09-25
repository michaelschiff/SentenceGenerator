import random
from itertools import islice

def normalize(mat):
    for row in mat:
        row_sum = sum(row)
        if row_sum is 0: continue
        for idx in xrange(len(row)):
            row[idx] = (row[idx]/float(row_sum))
    return mat

def sample(mat, m):
    if m >= len(mat) : raise IndexError("row index out of bounds")
    row = mat[m]
    if sum(row) is 0: return 0
    pick = random.random()
    idx, total = 0, row[0]
    while pick > total:
        idx += 1
        total += row[idx]
    return idx



class SentenceGenerator:
    
    def __init__(self, filepath):
        f = open(filepath, "r")
        self.text = f.readlines()
        self.dictionary = set()
        self.index = {} #word => num
        self.rev_index = [] #num => word
        self.build_index()
        
    def window(self, seq, n=2):
        "Returns a sliding window (of width n) over data from the iterable"
        "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
        it = iter(seq)
        result = tuple(islice(it, n))
        if len(result) == n:
            yield result    
        for elem in it:
            result = result[1:] + (elem,)
            yield result
        
    def build_index(self):
        for line in self.text:
            for word in line.split(" "):
                self.dictionary.add(word)

        #print self.dictionary

        for (word, index) in zip(self.dictionary, xrange(len(self.dictionary))):
            self.index[word] = index
            self.rev_index.append(word)
        num_text = []
        for line in self.text:
            for word in line.split(" "):
                num_text.append(self.index[word])
       
        #print num_text

        # row is current word
        # column is following word
        # value @ (row,col) is the number of times row was followed by col
        size = len(self.dictionary)
        self.prob_table = []
        for i in range(size):
            self.prob_table.append([0]*size)
        for (token, next_token) in self.window(num_text):
            self.prob_table[token][next_token] += 1
        normalize(self.prob_table)

        #print self.prob_table

    def generate_sentence(self, seed, length):
        if seed not in self.dictionary:
            print "I couldn't do that for you Hal"
        else:
            toPrint = seed+" "
            while length > 0:
                word_idx = sample(self.prob_table, self.index[seed])
                seed = self.rev_index[word_idx]
                toPrint += seed + " "
                length -= 1
            print toPrint

        

if __name__ == "__main__":
    x = SentenceGenerator("text.txt") 
    x.generate_sentence("this", 5)

