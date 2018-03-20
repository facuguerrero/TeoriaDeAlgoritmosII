#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
sys.path.append(os.path.dirname(os.path.dirname\
               (os.path.dirname(os.path.abspath(__file__)))))
from stringMatching import StringMatching

class MorrisPratt(StringMatching):
    """Implementación del algoritmo de Morris Pratt, primer optimizacion del
    ingenuo."""
    def __init__(self):
        super(StringMatching, self).__init__()

    def __str__(self):
        return "Morris-Pratt"

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
        mpNext = self.preprocessing(P, m)
        #Busqueda de matches
        i, j = 0, 0
        matchs = []
        #main loop
        while (j < n):
            #Cada vez que hay un mismatch, arrancamos a comparar desde el valor
            #que indique el preprocesamiento
            while (i > -1) and (P[i] != T[j]):
                i = mpNext[i]
            #Avanzamos en i y en j
            i, j = i+1, j+1
            #Si i >= m, entonces hubo un match!
            if (i >= m):
                #guardamos el lugar donde inicia el match
                matchs.append(j - i)
                #volvemos a empezar desde donde indique el preprocessing
                i = mpNext[i]
        return matchs

    def preprocessing(self, pattern, size):
        """Preprocesamiento del patrón.
            @param pattern {string}: Patron a procesar.
            @param size {int}: Tamaño del patron.
            @return {List}: 'mpNext', resultado del preprocesamiento de Morris
                           Pratt.
        """
        #definicion de mpNext
        mpNext = [0 for i in xrange(size + 1)]
        mpNext[0] = -1
        #inicializacion de variables
        i, j = 0, -1
        #Ciclo principal
        while (i < size):
            #En las coincidencias, i y j avanzan juntos (proximo caracter con
            #el que le sigue al de la ultima coincidencia) y, en caso que
            #p[i] != p[j], se va haciendo backtracking hasta llegar de nuevo
            #al origen.
            while (j > -1) and (pattern[i] != pattern[j]):
                j = mpNext[j]
            #avanzamos en i y en j
            i, j = i+1, j+1
            #Actualizamos la longitud de i al valor de j
            mpNext[i] = j
        #devolvemos la lista de preprocessing
        return mpNext
