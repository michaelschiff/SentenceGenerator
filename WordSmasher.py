#! /bin/python

import sys, random

legend = """    Noun                            N
    Plural                          p
    Noun Phrase                     h
    Verb (usu participle)           V
    Verb (transitive)               t
    Verb (intransitive)             i
    Adjective                       A
    Adverb                          v
    Conjunction                     C
    Preposition                     P
    Interjection                    !
    Pronoun                         r
    Definite Article                D
    Indefinite Article              I
    Nominative                      o"""

NOUN = 'N'
PLURAL = 'p'
NOUN_PHRASE = 'h'
VERB = 'V'
TRANSITIVE_VERB = 't'
INTRANSITIVE_VERB = 'i'
ADJECTIVE = 'A'
ADVERB = 'v'
CONJUNCTION = 'C'
PREPOSITION = 'P'
INTERJECTION = '!'
PRONOUN = 'r'
DEFINITE_ARTICLE = 'D'
INDEFINITE_ARTICLE = 'I'
NOMINATIVE = 'o'

def quit():
    print "run with: 'python " + sys.argv[0] + " num_sentences pos_tokens'"
    print "pos_tokens: "
    print legend
    sys.exit(1)


if (len(sys.argv) < 3):
    quit()
try:
    int(sys.argv[1])
except:
    quit()
    

word_set = {}
word_set[NOUN] = set()
word_set[PLURAL] = set()
word_set[NOUN_PHRASE] = set()
word_set[VERB] = set()
word_set[TRANSITIVE_VERB] = set()
word_set[INTRANSITIVE_VERB] = set()
word_set[ADJECTIVE] = set()
word_set[ADVERB] = set()
word_set[CONJUNCTION] = set()
word_set[PREPOSITION] = set()
word_set[INTERJECTION] = set()
word_set[PRONOUN] = set()
word_set[DEFINITE_ARTICLE] = set()
word_set[INDEFINITE_ARTICLE] = set()
word_set[NOMINATIVE] = set()

with open("part-of-speech.txt", "r") as pos_database:
    for line in pos_database:
        item = line.split('\t')
        phrase = item[0]
        tag = item[1]
        for t in tag:
            if t != '|' and t !='\n' and t != 'e':
                word_set[t].add(phrase)

for i in range(int(sys.argv[1])):
    for command in sys.argv[2:]:
        if command[0]=="-":
            print command[1:],
        else:
            phrases = word_set[command]
            print random.sample(phrases, 1)[0],
    print ""
