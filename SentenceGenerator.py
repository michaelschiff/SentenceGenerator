import sys
import random
from WordSmasher_v2 import *
if __name__ == "__main__":
    filename = sys.argv[1]
    num_to_generate = int(sys.argv[2])
    min_length = int(sys.argv[3])
    max_length = int(sys.argv[4])

    blue = "\x1b[34;5m"
    magenta = "\x1b[35;2m"

    
    def blue_print(s):
        print blue
        print s

    def magenta_print(s):
        print magenta
        print s

    
    sg = SentenceGenerator(filename)
    
    for i in xrange(num_to_generate):
        blue_print("#########################################################################")
        magenta_print(sg.generate_sentence(random.randint(min_length, max_length)))
