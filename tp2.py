from collections import Counter
import numpy as np
import sys

#1 Obtener las probabilidades de las palabras (separadas por espacios) contenidas en el archivo 'filename.txt'.

fileName = sys.argv[1]
print(fileName)

def splitWordsFromFile(fileName):  
    path = './samples/'+fileName
    with open(path, 'r', encoding='utf-8') as file:
        words = file.read().split()  
    return words

def generateWordsProbabilities(words):   
    frequencyWords = Counter(words) # {word: frequency}
    totalWords = len(words)
    probabilities = {word: count / totalWords for word, count in frequencyWords.items()} # {word : probabilty}
    return probabilities,list(probabilities.keys()),list(probabilities.values())


words = splitWordsFromFile(fileName)
dictionaryWords,S,PS = generateWordsProbabilities(words)
print('Palabras con su probabilidad: ', dictionaryWords)


#2- obtener el alfabeto codigo de las palabras

codeAlphabet = set()
for word in S:
    for code in word: 
        codeAlphabet.add(code)

print('Alfabeto codigo: ', codeAlphabet)

#3 calcular la entropia de la fuente y la longitud media del codigo

def calculateEntropy(d, orden):
    n = len(d)
    quantity = n**orden
    entropy = 0.0
    for i in range(quantity):
        entropy = entropy + d[i] * np.log2(1/d[i])
    return entropy


entropy=calculateEntropy(PS,1)
print('Entropia de la fuente: ',entropy)



def longitudMedia(p,X):
    n = len(p)
    l = 0
    for i in range(n):
        l = l + p[i] * len(X[i])
    return l

lMedia = longitudMedia(PS,S)
print('longitud media del codigo: ',lMedia)



#4 Comprobar si la codificación cumple las inecuaciones de Kraft y McMillan.

def calculateLengthWords(S):
    l =  np.zeros((len(S)), dtype=float)
    i=0
    for word in S:
        l[i] = len(word)
        i=i+1
    return l

def calcularKraft(a, l):
    k=0
    for length in l:
         k = k + a**(-length)
    return k

def satisfaceKraftMcMillan(a,l):
    k = calcularKraft(a,l)
    if (k <= 1):
        print(f'Satisface Kraft y Mc Millan ya que {k:.4f} <= 1')
        print('Es posible un codigo instantaneo')
        print('El codigo es univoco, las palabras codigo son distintas')
    else:        
        print(f'No satisface Kraft ya que {k:.4f} > 1')
        print('El codigo no es instantaneo')
    return k

k=satisfaceKraftMcMillan(len(codeAlphabet),calculateLengthWords(S))

#5 Determinar si el código es instantáneo y/o compacto.

def EsPrefijo(C1, C2):
    lc1 = len(C1)
    lc2 = len(C2)

    i = 0
    j = 0
    cond = True
    while (i < lc1 and j < lc2 and cond == True):
        if (C1[i] != C2[i]):
            cond = False
        i = i + 1
        j = j + 1
    return cond

def EsInstantaneo(S):
    cond = True
    l = len(S)
    i = 0
    while (i < l and cond == True):
        j = 0
        while (j < l and cond == True):
            if (i != j and EsPrefijo(S[i], S[j])):
                cond = False
            j = j + 1
        i = i + 1

    return cond

def esCompacto(P, d, orden):        
    long = longitudMedia(d, P)
    H = calculateEntropy(d, orden)
    print(f'H: {H:.2f} <= L:{long:.2f}')
    if (H <= long):
        print('Código compacto')
    else:
        print('Código no compacto')

esCompacto(S,PS,1) 

if k<=1:
    if EsInstantaneo(S):
        print('Se comprueba que el codigo es instantaneo')
    else:
        print('Se comprueba que el codigo no es instantaneo')