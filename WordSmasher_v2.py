import sys
import random
from itertools import islice
from collections import defaultdict

def normalize(mat):
    for word in mat:
        dict_of_nextwords = mat[word]
        word_occurances = sum(dict_of_nextwords.values())
        for next_word in dict_of_nextwords:
            dict_of_nextwords[next_word] = dict_of_nextwords[next_word] / float(word_occurances)
        

# The 'return -1' at the end is there because:
# In the special case that the text ends with a word
# that never showed up earlier in the text, we may be asked
# to sample from the words that follow it, of which there are none.
# returning -1 indicates to the caller that this has happened.
def sample(mat, m):
    next_word_dict = mat[m]
    pick = random.random()
    total = 0
    for next_word in next_word_dict:
        total += next_word_dict[next_word]
        if total >= pick:
            return next_word
    return -1


class SentenceGenerator:
    
    def __init__(self, filepath, arity):
        self.file = filepath
        # each index contains the dictionary of n-tuples of size index+1
        self.dictionaries = []
        # each index contains a dictionary mapping a tuple of index+1 words => num
        self.indexes = []
        # each index contains a dictionary mapping num => a tuple of index+1 words
        self.rev_indexes = []
        # each index contains the matrix of arity index+1
        self.prob_tables = []
        self.probabilities(arity)
        
    def window(self, seq, n=2):
        "Returns a sliding window (of width n) over data from the iterable"
        "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
        # TODO : handle window of size 1
        it = iter(seq)
        result = tuple(islice(it, n))
        if len(result) == n:
            yield result    
        for elem in it:
            result = result[1:] + (elem,)
            yield result

    def tuple_to_string(self, tup):
        return " ".join(tup) if len(tup) > 1 else tup[0]
        
    # builds dictionaries, indexes, and probability tables for each arity 1..n
    def probabilities(self, n):
        with open(self.file, 'r') as text_file:
            text = text_file.read().split(" ")
            for i in xrange(0, n):
                # for each arity, create a dictionary, indexes, and probability matrix
                dictionary = set()
                index = {}
                rev_index = []
                prob_table = defaultdict(lambda : defaultdict(lambda : 0))
                self.dictionaries.append(dictionary)
                self.indexes.append(index)
                self.rev_indexes.append(rev_index)
                self.prob_tables.append(prob_table)
                # scan the text in tuples of size i+1
                for word_tuple in self.window(text, i+1):
                    dictionary.add(self.tuple_to_string(word_tuple))
                for (token, idx) in zip(dictionary, xrange(len(dictionary))):
                    index[token] = idx
                    rev_index.append(token)
                # window over i+2 because i+1 is size of tuple and we want this and the next word
                for word_tuple in self.window(text, i+2):
                    seed_tuple_idx = index[" ".join(word_tuple[0:-1])]
                    # following word always comes from the arity 1 index
                    following_word_idx = self.indexes[0][word_tuple[-1]]
                    prob_table[seed_tuple_idx][following_word_idx] += 1
                normalize(prob_table)

    def generate_seed(self, arity):
        return random.sample(self.dictionaries[arity-1], 1)[0]
    
    
    def next_word(self, seed):
        word_idx = sample(self.prob_table, self.index[seed])
        return self.rev_index[word_idx]

    def sample(self, arity, current_string):
        prob_table = self.prob_tables[arity-1]
        current_string_idx = self.indexes[arity-1][current_string]
        return self.rev_indexes[0][sample(prob_table, current_string_idx)]
   
    def generate_sentence(self, arity, length):
        res = []
        res.extend(self.generate_seed(arity).split(" "))
        # length-1 since the seed is the first word
        for i in xrange(0, length-1):
            res.append(self.sample(arity, " ".join(res[-1*arity:])))
        return " ".join(res)

if __name__ == "__main__":
    # python WordSmasher_v2.py "sample.txt" 2 100
    # uses sample.txt, lookback size 2, 100 word sentence
    text = sys.argv[1]
    arity = int(sys.argv[2])
    length = int(sys.argv[3])
    x = SentenceGenerator(text, arity) 
    print x.generate_sentence(arity, length)
