#!/usr/bin/python

#LIBRARIES:
# Standard library
import os
import random
import re
import sys
from decimal import *
from optparse import OptionParser
#import cProfile

# Third-party libraries (only used temporarily for profiling)
#import memory_profiler


class VoseAlias(object):
    """ A probability distribution for discrete weighted random variables and its probability/alias
    tables for efficient sampling via Vose's Alias Method (a good explanation of which can be found at
    http://www.keithschwarz.com/darts-dice-coins/).
    """

    def __init__(self, dist, rng=None):
        """ (VoseAlias, dict[, RNG]) -> NoneType """
        self.dist = dist
        self.rng = rng or random.Random()
        self.alias_initialisation()
        self.table_prob_list = list(self.table_prob)

    def alias_initialisation(self):
        """ Construct probability and alias tables for the distribution. """
        # Initialise variables
        n = len(self.dist)
        self.table_prob = {}   # probability table
        self.table_alias = {}  # alias table
        small = []             # stack for probabilities smaller that 1
        large = []             # stack for probabilities greater than or equal to 1

        # Construct and sort the scaled probabilities into their appropriate stacks
        for o, p in self.dist.items():
            self.table_prob[o] = Decimal(p) * n

            if self.table_prob[o] < 1:
                small.append(o)
            else:
                large.append(o)

        # Construct the probability and alias tables
        while small and large:
            s = small.pop()
            l = large.pop()

            self.table_alias[s] = l

            self.table_prob[l] = (self.table_prob[l] + self.table_prob[s]) - Decimal(1)

            if self.table_prob[l] < 1:
                small.append(l)
            else:
                large.append(l)

        # The remaining outcomes (of one stack) must have probability 1
        while large:
            self.table_prob[large.pop()] = Decimal(1)

        while small:
            self.table_prob[small.pop()] = Decimal(1)

    def alias_generation(self):
        """ Return a random outcome from the distribution. """
        # Determine which column of table_prob to inspect
        col = self.rng.choice(self.table_prob_list)

        # Determine which outcome to pick in that column
        if self.table_prob[col] >= self.rng.random():
            return col
        else:
            return self.table_alias[col]

    def sample_n(self, size):
        """ Return a sample of size n from the distribution."""
        # Ensure a non-negative integer as been specified
        n = int(size)
        if n < 0:
            raise ValueError(f"Please enter a non-negative integer for the number of samples desired. size={n}")

        return [self.alias_generation() for i in range(n)]


#HELPER FUNCTIONS
def get_words(file):
    """ (str) -> list
    Return a list of words from a given corpus. """

    # Ensure the file is not empty
    if os.stat(file).st_size == 0:
        raise IOError("Please provide a file containing a corpus (not an empty file).")

    # Ensure the file is text based (not binary). This is based on the implementation
    #  of the Linux file command
    textchars = bytearray([7,8,9,10,12,13,27]) + bytearray(range(0x20, 0x100))
    with open(file, "rb") as bin_file:
        if bool(bin_file.read(2048).translate(None, textchars)):
            raise IOError("Please provide a file containing text-based data.")

    with open(file, "r") as corpus:
        words = corpus.read().split()
    return words


def sample2dist(sample):
    """ (list) -> dict (i.e {outcome:proportion})
    Construct a distribution based on an observed sample (e.g. rolls of a bias die) """
    increment = Decimal(1)/len(sample)

    dist = {}
    get = dist.get
    for o in sample: # o for outcome
        dist[o] = get(o, 0) + increment
    return dist


#COMMAND LINE HANDLING
def check_required_arguments(opts, parser):
    missing_options = []
    for option in parser.option_list:
        if re.match(r'^\[REQUIRED\]', option.help) and eval('opts.' + option.dest) is None:
            missing_options.extend(option._long_opts)
    if len(missing_options) > 0:
        parser.error('Missing REQUIRED parameters: ' + str(missing_options))
        parser.print_help()
        sys.exit(1)

def handle_options():
    parser = OptionParser()
    parser.add_option("-p", "--path", dest="path",
                      help="[REQUIRED] Path to corpus.", metavar="FILE")
    parser.add_option("-n", "--num", dest="n", type=int,
                      help="[REQUIRED] Non-negative integer specifying how many samples are desired.", metavar="INT")

    (options, args) = parser.parse_args()
    check_required_arguments(options, parser)
    return options

def main():
    # Handle command line arguments
    options = handle_options()

    try:
        # Construct distribution
        words = get_words(options.path)
        word_dist = sample2dist(words)
        VA_words = VoseAlias(word_dist)

        # Sample n words
        print("\nGenerating %d random samples:\n" % options.n)
        sample = VA_words.sample_n(options.n)
        for s in sample:
            print(s)
    except Exception as e:
        sys.exit("\nError: %s" % e)


if __name__ == "__main__":
    main()
