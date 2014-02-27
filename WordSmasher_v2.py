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
    
    def __init__(self, filepath):
        f = open(filepath, "r")
        self.text = f.readlines()
        self.dictionary = set()
        self.index = {} #word => num
        self.rev_index = [] #num => word
        self.probabilities()
        
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
        
    def probabilities(self):
        for line in self.text:
            for word in line.split(" "):
                self.dictionary.add(word)
        print "found " + str(len(self.dictionary)) + " unique words"
        
        for (word, index) in zip(self.dictionary, xrange(len(self.dictionary))):
            self.index[word] = index
            self.rev_index.append(word)
        num_text = []
        for line in self.text:
            for word in line.split(" "):
                num_text.append(self.index[word])
        
        # a dictionary, whose default value is a dictionary, whose default value is 0.
        self.prob_table = defaultdict(lambda : defaultdict(lambda : 0))
        for (token, next_token) in self.window(num_text): 
            self.prob_table[token][next_token] += 1
        normalize(self.prob_table)


    def generate_seed(self):
        return random.sample(self.dictionary, 1)[0]
    
    
    # because of the special case described above: we generate samples of the next word,
    # until we get a non-negative index, generating a new seed each time.  We use a new seed
    # because the seed that returned a sample of -1 will always return a sample of -1.
    def generate_sentence_seed(self, seed, length):
        if seed not in self.dictionary:
            print "I couldn't do that for you Hal"
        else:
            toPrint = seed+" "
            while length > 0:
                word_idx = -1
                while word_idx < 0: 
                    word_idx = sample(self.prob_table, self.index[seed])
                    seed = self.generate_seed()
                seed = self.rev_index[word_idx]
                toPrint += seed + " "
                length -= 1
            return toPrint
    
    
    def generate_sentence(self, length):
        return self.generate_sentence_seed(self.generate_seed(), length)
        

if __name__ == "__main__":
    x = SentenceGenerator("text.txt") 
    x.generate_sentence_seed("this", 5)

