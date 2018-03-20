PSIZE = 4200 #Maximo tamanioo del patron

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from stringMatching import StringMatching

class ZT(StringMatching):
    def __init__(self):
        #Constructor de superclase
        super(StringMatching, self).__init__()
        self.aSize = 0
        self.indices = {}

    def __str__(self):
        return "Zhu-Takaoka"

    def setSize(self, t):
        self.aSize = t

    def encontrarCaracteres(self):
        carac = []
        for ci in self.text:
            if(ci not in carac):
                carac.append(ci)
        carac.sort()
        return carac

    def crearIndices(self):
        """Funcion auxiliar para estandarizar los
        indices de los elementos de un alfabeto y no
        depender del codigo ascii"""
        l = self.encontrarCaracteres()
        i=0
        for c in l:
            self.indices[c] = i
            i+=1

    def suffixes( self, lenP ):

        patron = self.pattern
        #PSIZE = lenP
        #Inicializacion del vector a devolver.
        suf = [0 for x in xrange(0,PSIZE)]

        suf[lenP - 1] = lenP
        g = lenP - 1

        for x in xrange(0, lenP-1):#queremos que vaya hasta lenP-2
            #En realidad queremos hacer el for al revez entonces:
            i = lenP - 2 - x
            if( (i > g) and (suf[i + lenP - 1 -f] < i - g) ):
                suf[i] = suf[i + lenP - 1 - f]
            else:
                if(i < g):
                    g = i
                f = i
                while(g >=0 and patron[g] == patron[g+lenP-1-f]):
                    g-=1
                    suf[i] = f-g
        return suf

    def preBmGs( self, lenP ):
        patron = self.pattern
        #Inicializacion del vector
        #PSIZE = lenP
        bmgs = [0 for x in xrange(0,PSIZE)]
        suf = self.suffixes(lenP)

        for i in xrange(0, lenP):
            bmgs[i] = lenP
        for i in xrange(0,lenP):
            #Este for en realidad va al revez
            x = lenP - 1 - x
            if(suf[x] == x+1):
                for y in xrange(1,lenP - 1 - x):
                    if(bmgs[y] == lenP):
                        bmgs[y] = lenP-1-x
        for x in xrange(0,lenP-1):
            bmgs[lenP - 1 - suf[x]] = lenP - 1 - x
        return bmgs


    def preZtBc(self, lenP ):
        patron = self.pattern
        ASIZE = 256
        #Armado de la matriz
        ztbc = [0] * ASIZE
        for i in xrange(ASIZE):
            ztbc[i] = [0] * ASIZE
        for x in xrange(0, ASIZE):
            for y in xrange(0, ASIZE):
                ztbc[x][y] = lenP
        #LLenamos cada codigo
        for x in xrange(0,ASIZE):
            """Marca el primer caracter del patron
            con lenP-1 (esta mas a la izq)"""
            ztbc[x][ord(patron[0])] = lenP -1

        for x in xrange(1, lenP - 1):
            """Entramos a la posicion de la matriz
            que corresponde a las posiciones (i-1,i)
            del patron y le seteamos la posicion en la que
            se encuentra"""
            ztbc[ord(patron[x-1])][ord(patron[x])] = lenP - 1 - x
        return ztbc

    def find_match( self ):

        #Me quedo con las 2 longitudes.
        lenP = len(self.pattern)
        lenT = len(self.text)

        if(lenP <= 0 or lenT<= 0):
            return []

        #Creo el diccionario que contiene los indices de los elementos del alfabeto
        self.crearIndices()

        #Fase de preprocesamiento
        BMGS = self.preBmGs( lenP )
        ZTBC = self.preZtBc( lenP )

        #Concatenamos el patron 2 veces al final del texto
        self.text += self.pattern
        self.text += self.pattern

        matches = []

        #Pasamos a buscar el patron en el texto
        contador = 0
        j = 0
        while(j <= lenT - lenP):
            i = lenP - 1
            while( i >= 0 and self.pattern[i] == self.text[i+j]):
                i-=1
            if(i<0):
                contador+=1
                matches.append(j)
                j += BMGS[0]
            else:
                index1 = self.text[j+lenP - 2]
                index2 = self.text[j+lenP-1]
                j += max(BMGS[i], ZTBC[ord(index1)][ord(index2)] )
        return matches

z = ZT()
z.set_text("amigo cigomo estas")
z.set_pattern("ig")
z.setSize(256)
print z.find_match()
