#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from stringMatching import StringMatching

class Colussi(StringMatching):
    """Implementación del algoritmo de Colussi, tercer optimizacion
    del ingenuo, extension de Knuth Morris Pratt."""
    def __init__(self):
        super(StringMatching, self).__init__()

    def __str__(self):
        return "Colussi"

    def find_match(self):
        """Encuentra todos los matchs de P en T.
            @return {List}: contiene las posiciones de inicio de todos
                            los matchs de P en T."""
        #definicion de variables para no usar 'self.' todo el tiempo
        P = self.pattern
        T = self.text
        #largo de los strings
        n = len(T)
        m = len(P)
        if m < 1 or n < 1: return []
        #preprocesamiento del patron
        h, next, shift, nd = self.preprocessing(P, m)
        #busqueda de matchs
        matchs = []
        i, j, last = 0, 0, -1
        while j <= n - m:
            while (i < m) and (last < j + h[i]) and (P[h[i]] == T[j + h[i]]):
                i += 1
            if (i >= m) or (last >= j + h[i]):
                matchs.append(j)
                i = m
            if i > nd: last = j + m - 1
            j += shift[i]
            i = next[i]
        return matchs

    def preprocessing(self, pattern, size):
        """Preprocesamiento del patrón.
            @param pattern {string}: Patron a procesar.
            @param size {int}: Tamaño del patron.
        """
        pattern += " "
        #definicion de arreglos a utilizar
        h = [0 for i in xrange(size+1)]
        next = [0 for i in xrange(size+1)]
        shift = [0 for i in xrange(size+1)]
        hmax = [0 for i in xrange(size+1)]
        kmin = [0 for i in xrange(size+1)]
        nhd0 = [0 for i in xrange(size+1)]
        rmin = [0 for i in xrange(size+1)]
        i,k,nd,q,r,s = 0,0,0,0,0,0
        #calculo de hmax
        i, k = 1, 1
        while True:
            while (pattern[i] == pattern[i - k]): i+=1
            hmax[k] = i
            q = k + 1
            while (hmax[q - k] + k < i):
                hmax[q] = hmax[q - k] + k
                q+=1
            k = q
            if k == i + 1: i = k
            #condicion de corte [es un do-while]
            if k > size: break
        #calculo de kmin
        for i in xrange(size, 0, -1):
            if hmax[i] < size:
                kmin[hmax[i]] = 1
        #calculo de rmin
        for i in xrange(size-1, -1, -1):
            if hmax[i + 1] == size: r = i + 1
            if kmin[i] == 0: rmin[i] = r
            else: rmin[i] = 0
        #calculo de h
        s = -1
        r = size
        for i in xrange(size):
            if kmin[i] == 0:
                r -= 1
                h[r] = i
            else:
                s += 1
                h[s] = i
        nd = s
        #calculo de shift
        for i in xrange(nd + 1):
            shift[i] = kmin[h[i]]
        for i in xrange(nd + 1, size):
            shift[i] = rmin[h[i]]
        shift[size] = rmin[0]
        #calculo de nhd0
        s = 0
        for i in xrange(size):
            nhd0[i] = s
            if kmin[i] > 0: s += 1
        #calculo de next
        for i in xrange(nd + 1):
            next[i] = nhd0[h[i] - kmin[h[i]]]
        for i in xrange(nd + 1, size):
            next[i] = nhd0[size - rmin[h[i]]]
        next[size] = nhd0[size - rmin[h[size - 1]]]

        return h, next, shift, nd
