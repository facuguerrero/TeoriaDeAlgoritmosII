#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from stringMatching import StringMatching

class Naive(StringMatching):
    """Implementación del algoritmo ingenuo de exact matching."""
    def __init__(self):
        #Constructor de superclase
        super(StringMatching, self).__init__()

    def __str__(self):
        return "Naive Algorithm"

    #Override
    def find_match(self):
        """Encuentra todos los matchs de P en T.
            @return {List}: contiene las posiciones de inicio de todos
                            los matchs de P en T."""
        #definicion de variables para no usar 'self.' todo el tiempo
        P = self.pattern
        T = self.text
        #largo de los strings
        t_len = len(T)
        p_len = len(P)
        #lista de matchs
        matchs = []
        #ciclo principal del algoritmo
        for j in range(t_len):
            #if (j + p_len > t_len): break #manera inteligente de cortar
            for i in range(p_len):
                #Si se va de rango, cortamos.
                if (j + i == t_len): break
                #Si son diferentes, avanzamos en T
                if (P[i] != T[j+i]): break
                #Si i llego a valer el largo de P, entonces hay un match en j
                if (i == p_len-1): matchs.append(j)
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
        #largo de los strings
        t_len = len(T)
        p_len = len(Ps[0])
        #largo del set
        set_len = len(Ps)
        #lista de matchs
        matchs = []

        # ciclo principal del algoritmo
        for j in range(t_len):

            #si hay match
            for k in range(set_len):

                P = Ps[k]

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
