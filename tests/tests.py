#!/usr/bin/env python

#LIBRARIES:
# Standard library
import math
import random
import unittest
from decimal import *

# Local application
from vose_sampler import vose_sampler

# Common paths and error messages
valid_folder = "tests/file_examples/valid_files/"
invalid_folder = "tests/file_examples/invalid_files/"

empty_file_error = "Error\: Please provide a file containing a corpus \(not an empty file\)."
binary_file_error = "Error\: Please provide a file containing text-based data."
nonnegative_integer_error = "Error\: Please enter a non-negative integer for the number of samples desired\: "


class TestValidation(unittest.TestCase):
    """ unittest methods for testing validation checks within vose_sampler
    work as expected. """

    def test_empty_file(self):
        """Test vose_sampler.get_words against empty files """
        self.assertRaisesRegexp(SystemExit, empty_file_error, vose_sampler.get_words, invalid_folder + "empty.txt")

    def test_binary_file1(self):
        """Test vose_sampler.get_words against .epub files """
        self.assertRaisesRegexp(SystemExit, binary_file_error, vose_sampler.get_words, invalid_folder + "Alice.epub")

    def test_binary_file2(self):
        """Test vose_sampler.get_words against .mobi files """
        self.assertRaisesRegexp(SystemExit, binary_file_error, vose_sampler.get_words, invalid_folder + "Alice.mobi")

    def test_binary_file3(self):
        """Test vose_sampler.get_words against .pdf files """
        self.assertRaisesRegexp(SystemExit, binary_file_error, vose_sampler.get_words, invalid_folder + "Alice.pdf")

    def test_binary_file4(self):
        """Test vose_sampler.get_words against .wav files """
        self.assertRaisesRegexp(SystemExit, binary_file_error, vose_sampler.get_words, invalid_folder + "zero.wav")

    def test_negative_integer(self):
        """Test vose_sampler.VoseAlias.alias_generation against a size
        specified by a negative integer. """
        words = vose_sampler.get_words(valid_folder + "small.txt")
        word_dist = vose_sampler.sample2dist(words)
        VA_words = vose_sampler.VoseAlias(word_dist)
        self.assertRaisesRegexp(SystemExit, nonnegative_integer_error + "-1",  VA_words.sample_n, -1)

    def test_zero_integer(self):
        """Test vose_sampler.ProbDistribution.alias_generation against a size
        defined by zero. """
        words = vose_sampler.get_words(valid_folder + "small.txt")
        word_dist = vose_sampler.sample2dist(words)
        VA_words = vose_sampler.VoseAlias(word_dist)
        self.assertRaisesRegexp(SystemExit, nonnegative_integer_error + "0",  VA_words.sample_n, 0)


class TestAccuracy(unittest.TestCase):
    """ unittest methods for testing the accuracy of method within vose_sampler. """

    def dbinom(self, x, n, p):
        """ Compute the probability of x successes in n flips of a coin that produces
        a head with probability p (i.e. the probability density of a Binomial RV). """
        f = math.factorial
        C = Decimal(f(n) / (f(x) * f(n-x)))
        return C * p**x * (1-p)**(n-x)

    def test_output_get_word(self):
        """Test vose_sampler.get_words to ensure it correctly produces a list of
        words from a given corpus. """
        actual = vose_sampler.get_words(valid_folder + "single_word.txt")
        expected = ["Speechmatics"]
        self.assertEqual(actual, expected)

    def test_output_create_dist(self):
        """Test vose_sampler.ProbDistribution.create_dist to ensure it correctly
        produces a uniform distribution for a list of words representing a standard die. """
        numbers_dist = vose_sampler.sample2dist(["one","two","three","four","five","six"])
        VA_numbers = vose_sampler.VoseAlias(numbers_dist)
        actual = VA_numbers.dist
        prob = Decimal(1)/Decimal(6)
        expected = {"one":prob, "two":prob, "three":prob, "four":prob, "five":prob, "six":prob}
        self.assertEqual(actual, expected)

    def test_output_alias_generation(self):
        """Test vose_sampler.ProbDistribution.alias_generation to ensure it
        generates words with same distribution as the original corpus. This
        performs a 2-sided hypothesis test at the 1% significance level, that:
        H_0: observed proportion a randomly selected word is equal to the
             proportion seen in the original corpus (i.e. p_original == p_observed)
        H_1: p_original != p_observed
        """
        print("WARNING: There is a random element to test_output_alias_generation\n\
        so it is likely to occasionally fail, nonetheless if the alias_generation\n\
        method is working correctly failures will be very rare (testing at alpha=0.01\n\
        implies we should expect a Type I error about 1% of the time).")

        # Construct a ProbDistribution
        words = vose_sampler.get_words(valid_folder + "small.txt")
        word_dist = vose_sampler.sample2dist(words)
        VA_words = vose_sampler.VoseAlias(word_dist)

        # Generate sample and calculate the number of observations for a randomly selected word
        word = random.choice(list(VA_words.dist))

        n = 1000

        t = 0
        for i in range(n):
            if VA_words.alias_generation() == word:
                t += 1

        # Compute the p-value
        p_original = VA_words.dist[word]

        p_low = math.fsum([self.dbinom(x, n, p_original) for x in range(t,n+1)])
        p_high = math.fsum([self.dbinom(x, n, p_original) for x in range(t+1)])

        p = 2*min(p_low, p_high)

        # Do not accept H_0 if p <= alpha
        alpha = 0.01
        self.assertGreater(p, alpha)

    def test_roundtrip(self):
        dist = {"H": Decimal(0.2), "T": Decimal(0.8)}
        VA = vose_sampler.VoseAlias(dist)
        sample = VA.sample_n(100000)
        computed_dist = vose_sampler.sample2dist(sample)
        self.assertAlmostEqual(dist.get("H"), computed_dist.get("H"), delta=0.01)
        self.assertAlmostEqual(dist.get("T"), computed_dist.get("T"), delta=0.01)


if __name__ == "__main__":
    unittest.main()
