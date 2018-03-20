#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Naive.Naive import Naive
from ZhuTakaoka.zt import ZT
from RabinKarp.RabinKarp import RabinKarp
from Colussi.MorrisPratt.MorrisPratt import MorrisPratt
from Colussi.KnuthMorrisPratt.KnuthMorrisPratt import KnuthMorrisPratt
from Colussi.Colussi import Colussi
import pyhash
import random
import time
import sys

LONGEST_DNA_PATTERN = 4
LONGEST_NUMBER_PATTERN = 4
LONGEST_CHARS_PATTERN = 4

RED   = "\033[1;31m"
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
MAGENTA = "\033[1;35m"
YELLOW = "\033[1;33m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"

#DNA DATA INIT
DNA_FILES = [['Testing Dataset/hprt_excerpt.dat', '1.6kb'], \
             #['Testing Dataset/hprt.dat', '56.7kb'], \
             #['Testing Dataset/rbs.dat', '180.4kb'], \
             ['Testing Dataset/ecoli.dat', '4.6Mb'] ]
DNA_PATTERNS = []
dna_alphabet = ['a','g','c','t']
dna_sizes = [8, 1024]#, 64, 256, 1024]
for i in dna_sizes:
    pattern = ""
    for j in xrange(i):
        pattern += random.choice(dna_alphabet)
    DNA_PATTERNS.append(pattern)
pattern = ""
DNA = ["DNA", 4, DNA_PATTERNS, DNA_FILES]

#ENGLISH DATA INIT
ENGLISH_FILES = [['Testing Dataset/bible_excerpt.txt', '1.2kb'], \
                 ['Testing Dataset/bible.txt', '4Mb']]
#Una palabra corta y una frase larga
ENGLISH_PATTERNS = ['the', \
                    'Now therefore, I pray thee, let thy servant abide instead \
of the lad a bondman to my lord; and let the lad go up with \
his brethren']
ENGLISH = ["English", 90, ENGLISH_PATTERNS, ENGLISH_FILES]

#SPANISH DATA INIT
SPANISH_FILES = [['Testing Dataset/egmf.txt', '64.5kb'], \
                 ['Testing Dataset/quijote.txt', '2.2Mb']]
#Una palabra corta y una frase larga
SPANISH_PATTERNS = ['de', \
                    'Con silencio grande estuve escuchando lo que mi amigo me\
                     decía, y de tal']
SPANISH = ["Spanish", 106, SPANISH_PATTERNS, SPANISH_FILES]

#RANDOM DATA INIT
#Random numbers
PI_FILE = [['Testing Dataset/pi_excerpt.txt', '1.5kb'],
           ['Testing Dataset/pi.txt', '1Mb']]
PI_PATTERNS = []
pi_alphabet = [str(i) for i in xrange(10)]
pi_sizes = [2, 32, 128, 1024]
for i in pi_sizes:
    pattern = ""
    for j in xrange(i):
        pattern += random.choice(pi_alphabet)
    PI_PATTERNS.append(pattern)
pattern = ""
PI = ["Random Numbers", 10, PI_PATTERNS, PI_FILE]
#Random letters
RANDOM_FILE = [['Testing Dataset/random.txt', '100kb']]
RANDOM_PATTERNS = []
random_alphabet = [i for i in xrange(65, 91)]
random_alphabet += [i for i in xrange(97, 123)]
random_alphabet += [32, 33]
random_sizes = [8, 64, 256, 1024]
for i in random_sizes:
    pattern = ""
    for j in xrange(i):
        pattern += chr(random.choice(random_alphabet))
    RANDOM_PATTERNS.append(pattern)
pattern = ""
RANDOM = ["Random Characters", 54, RANDOM_PATTERNS, RANDOM_FILE]

#CODE DATA INIT
CODE_FILES = [['Testing Dataset/compress.c', '39.6kb'], \
                 ['Testing Dataset/y.tab.c', '268.4kb']]
#10 palabras mas comunes en lenguaje C
CODE_PATTERNS = ['if', 'define', 'ifndef', 'include']
CODE = ["Code", 114, CODE_PATTERNS, CODE_FILES]

#DATA UNION
TYPES = [DNA, ENGLISH]#, SPANISH, PI, RANDOM, CODE]
#################################Aux funcs#####################################

def found_matches(list):
    return len(list) > 0

##############################Testing##########################################

####BASIC TESTING####

def no_match_test(algorithm):
    """P not in T"""
    #setup
    T = "aabxaabcdy"
    P = "aaby"
    algorithm.set_text(T)
    algorithm.set_pattern(P)
    #test
    if found_matches(algorithm.find_match()):
        print "Match found when there were none. Algorithm: " + str(algorithm)
        return False
    return True

def empty_pattern_test(algorithm):
    """len(P) == 0"""
    T = "aabxaabcdy"
    P = ""
    algorithm.set_text(T)
    algorithm.set_pattern(P)
    #test
    if found_matches(algorithm.find_match()):
        print "Match found with empty pattern. Algorithm: " + str(algorithm)
        return False
    return True

def empty_text_test(algorithm):
    """len(T) == 0"""
    T = ""
    P = "aaby"
    algorithm.set_text(T)
    algorithm.set_pattern(P)
    #test
    if found_matches(algorithm.find_match()):
        print "Match found on empty text. Algorithm: " + str(algorithm)
        return False
    return True

def pattern_longer_than_text_test(algorithm):
    """len(P) > len(T)"""
    T = "aab"
    P = "aaby"
    algorithm.set_text(T)
    algorithm.set_pattern(P)
    #test
    if found_matches(algorithm.find_match()):
        print "Match found with pattern longer than text. Algorithm: " \
            + str(algorithm)
        return False
    return True

def pattern_equals_text_test(algorithm):
    """P == T"""
    T = "abcdabbed"
    P = "abcdabbed"
    algorithm.set_text(T)
    algorithm.set_pattern(P)
    #test
    if not found_matches(algorithm.find_match()):
        print "Match not found when pattern equals text. Algorithm: " \
            + str(algorithm)
        return False
    return True

#######PERFORMANCE TESTING#######
def text_testing(algorithm, name, size, patterns, files):
    #Buscamos los patrones en los textos
    #Printing and format
    sys.stdout.write(BOLD)
    print "\n  Performance test on ",
    sys.stdout.write(RED)
    print name,
    sys.stdout.write(RESET)
    sys.stdout.write(BOLD)
    print " files. Alphabet size: ",
    sys.stdout.write(RED)
    print str(size)
    sys.stdout.write(RESET)
    #Main body
    for f in files:
        try:
            fd = open(f[0], 'r')
        except IOError:
            print "Error while trying to open file '" + f[0] + "'."
            continue
        #printing and format
        print "\n  Now processing ",
        sys.stdout.write(GREEN)
        print "'" + f[0][16:] + "'",
        sys.stdout.write(RESET)
        print " (" + f[1] + ")."
        #Setting T
        algorithm.set_text(fd.read())
        for pattern in patterns:
            #Setting P
            algorithm.set_pattern(pattern)
            #Printing and format
            print "    Searching for matchs with pattern: ",
            sys.stdout.write(BLUE)
            print pattern,
            sys.stdout.write(RESET)
            print "."
            #Matching
            start = time.time()
            matches = algorithm.find_match()
            end = time.time()
            #Printing and format
            print "    Found ",
            sys.stdout.write(YELLOW)
            print str(len(matches)),
            sys.stdout.write(RESET)
            print " matches on ",
            sys.stdout.write(MAGENTA)
            print str(end - start) + "s."
            sys.stdout.write(RESET)

        fd.close()

##########################################main#################################

def main():
    ######Naive tests######
    #init
    naive = Naive()
    zt = ZT()
    rabinKarp = RabinKarp()
    mp = MorrisPratt()
    kmp = KnuthMorrisPratt()
    colussi = Colussi()
    hashers = [("Spooky 32 bits", pyhash.spooky_32()),
               ("FNV 32 bits", pyhash.fnv1_32()),
               ("Murmur 32 bits", pyhash.murmur1_32()),
               ("City 32 bits", pyhash.city_32())]
    #csv
    import csv
    try:
        fd = open('results_all.csv', 'w')
    except IOError:
        print "Error while trying to open file 'results.csv'."
        return
    #setup
    algorithms = [naive, rabinKarp]
    #tests
    for algorithm in algorithms:
        sys.stdout.write(BOLD)
        print "\nBasic tests for: ",
        sys.stdout.write(CYAN)
        print str(algorithm)
        sys.stdout.write(RESET)
        lenHashers = 1
        if (str(algorithm) == "Rabin-Karp Algorithm"):
            lenHashers = len(hashers)

        for i in xrange(lenHashers):
            #si es el algoritmo de Rabin Karp se van seteando disntintos algoritmos
            if (str(algorithm) == "Rabin-Karp Algorithm"):
                algorithm.setHasher(hashers[i][1])
                sys.stdout.write(RED)
                print "  Hashing function: ",
                sys.stdout.write(GREEN)
                print hashers[i][0]
                sys.stdout.write(RESET)
            #basic tests
            value = no_match_test(algorithm)
            value = empty_pattern_test(algorithm)
            value = empty_text_test(algorithm)
            value = pattern_longer_than_text_test(algorithm)
            value = pattern_equals_text_test(algorithm)
            if value: print "  Basic tests OK"
            else:
                print "Basic tests ERROR"
                return 0
        for i in xrange(lenHashers):
            #performance tests
            if (i == 0):
                sys.stdout.write(BOLD)
                print "Performance tests for: ",
                sys.stdout.write(CYAN)
                print str(algorithm)
                sys.stdout.write(RESET)
            if (str(algorithm) == "Rabin-Karp Algorithm"):
                algorithm.setHasher(hashers[i][1])
                sys.stdout.write(RED)
                print "\n  Hashing function: ",
                sys.stdout.write(GREEN)
                print hashers[i][0]
                sys.stdout.write(RESET)
            #Testing
            for test in TYPES:
                text_testing(algorithm, test[0], test[1], test[2], test[3])
    fd.close()

if __name__ == '__main__':
    main()
