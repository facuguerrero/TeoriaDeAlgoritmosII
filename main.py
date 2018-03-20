#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Naive.Naive import Naive
from RabinKarp.RabinKarp import RabinKarp
import pyhash

def main():
    T = "abcxaabcdy"
    P = ["ab", "cx", "ya"]
    rabinKarp = RabinKarp()
    hasher = pyhash.murmur1_32()
    rabinKarp.setHasher(hasher)
    rabinKarp.set_n_patterns(P)
    rabinKarp.set_text(T)
    matchs = rabinKarp.find_multiple_match()
    print matchs

main()
