#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from stringMatching import StringMatching
import pyhash

class RabinKarp(StringMatching):
    """Implementación del algoritmo de Rabin y Karp de exact matching."""
    def __init__(self):
        #Constructor de superclase
        super(StringMatching, self).__init__()

    def setHasher(self, hasher, name):
        self.hasher = hasher
        self.hash_name = name

    def getHasher(self):
        return self.hash_name    

    def __str__(self):
        return "Rabin-Karp Algorithm"

    #Override
    def find_match(self):
        """Encuentra todos los matchs de P en T.
            @return {List}: contiene las posiciones de inicio de todos
                            los matchs de P en T."""
        #definicion de variables para no usar 'self.' todo el tiempo
        P = self.pattern
        T = self.text
        H = self.hasher
        #largo de los strings
        t_len = len(T)
        p_len = len(P)
        #lista de matchs
        matchs = []

        #Valor de hash del patron
        hPatternValue = H(P)

        # ciclo principal del algoritmo
        for j in range(t_len):

            #se chequean los valores de hash del patron contra el
            #valor de hash de la palabra actual
            #solo si hay un match se verifica letra por letra
            hStringValue = H(T[j:p_len + j])

            #si hay match
            if (hPatternValue == hStringValue):

                #se verifica letra por letra
                for i in range(p_len):
                    # Si se va de rango, cortamos.
                    if (j + i == t_len): break
                    # Si son diferentes, avanzamos en T
                    if (P[i] != T[j + i]): break
                    # Si i llego a valer el largo de P, entonces hay un match en j
                    if (i == p_len - 1): matchs.append(j)

        #Devolvemos la lista
        return matchs


    def find_multiple_match(self):
        """Encuentra todos los matchs de los n patrones en T. Se asume un tamaño
            fijo m para cada patron.
            @return {List}: contiene las posiciones de inicio de todos
                            los matchs de los n Ps en T."""
        #definicion de variables para no usar 'self.' todo el tiempo
        Ps = self.patterns
        T = self.text
        H = self.hasher
        #largo de los strings
        t_len = len(T)
        p_len = len(Ps[0])
        #largo del set
        set_len = len(Ps)
        #lista de matchs
        matchs = []

        #calculo los valores de hash para cada patron
        hPatterns = []
        for P in Ps:
            #Valor de hash del patron
            hPatterns.append(H(P))

        # ciclo principal del algoritmo
        for j in range(t_len):

            #se chequean los valores de hash del patron contra el
            #valor de hash de la palabra actual
            #solo si hay un match se verifica letra por letra
            hStringValue = H(T[j:p_len + j])

            #si hay match
            for k in range(set_len):

                hPatternValue = hPatterns[k]
                P = Ps[k]

                if (hPatternValue == hStringValue):

                    #se verifica letra por letra
                    for i in range(p_len):
                        # Si se va de rango, cortamos.
                        if (j + i == t_len): break
                        # Si son diferentes, avanzamos en T
                        if (P[i] != T[j + i]): break
                        # Si i llego a valer el largo de P, entonces hay un match en j
                        if (i == p_len - 1): matchs.append(j)

        #Devolvemos la lista
        return matchs
