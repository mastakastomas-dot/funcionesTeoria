from math import log2
from math import log
from random import random
import math

def infobits(probs):
    listainfo = []

    for p in probs:
        info = log2(1/p)
        listainfo.append(info)

    return listainfo

def entriopia(probs, base = 2):

    ent = 0

    for p in probs:
        ent += log(1/p, base)*p

    return ent

def entriopiabinaria(w):

    alf = [1, 0]
    probs = [w, 1 - w]

    return entriopia(probs)



#sirve para hacer la lista del alfabeto y de las probabilidades de cada caracter en la cadena
def generalistas(cadena):
    listacuenta = []
    alfabeto = []
    total = 0

    for letra in cadena:
        if letra not in alfabeto:
            alfabeto.append(letra)
            listacuenta.append(1)
        else:
            indice = alfabeto.index(letra)
            listacuenta[indice] += 1
        total += 1
    probs = []

    for cant in listacuenta:
        probs.append(cant/total)

    return alfabeto, probs



#devuelve las probabilidades acumuladas
def probacumuladas(probs):
    pacums = []
    sum = 0
    for p in probs:
        sum += p
        pacums.append(sum)
    return pacums


#devuelve una letra al azar del alfabeto que se le pase
def letra(alfabeto, probabilidades):
    ran = random()

    for p in probabilidades:
        if ran < p:
            return alfabeto[probabilidades.index(p)]



#devuelve una cadena formada a partir del alfabeto
def generacadena(n, alfabeto, probabilidades):
    i = 1
    acums = probacumuladas(probabilidades)
    cad = ""
    while i <= n:
        cad += letra(alfabeto, acums)
        i += 1

    return cad

def obtiene_matriz(mensaje, alfabeto):

    n = len(alfabeto)

    matriz = [[0.0 for _ in range(n)] for _ in range(n)]

    for i in range(len(mensaje) -1):
        actual = mensaje[i]
        siguiente = mensaje[i+1]
        # aca cuenta la cantidad de veces que un mensaje aparece despues de otro
        columna = alfabeto.index(actual)
        fila = alfabeto.index(siguiente)
        matriz[fila][columna] += 1

    for j in range(n):
        suma_col = sum(matriz[i][j] for i in range(n))
        if suma_col > 0:
            for i in range(n):
                matriz[i][j] = matriz[i][j] / suma_col

    return matriz


def mostrar_matriz(matriz, alfabeto):
    # Definimos un ancho fijo para las columnas (8 caracteres queda bien para decimales)
    ancho = 8

    # 1. Armamos el encabezado superior con los símbolos (Columnas = Estado Actual)
    encabezado = "    |"
    for simbolo in alfabeto:
        encabezado += f"{simbolo:>{ancho}}"
    print(encabezado)

    # Imprimimos una línea separadora dinámica según el ancho total
    print("-" * len(encabezado))

    # 2. Recorremos e imprimimos cada fila
    for i in range(len(alfabeto)):
        # Iniciamos el texto de la fila con su símbolo (Filas = Estado Siguiente)
        fila_str = f"{alfabeto[i]:>3} |"

        for j in range(len(alfabeto)):
            # Formateamos cada probabilidad a 3 decimales (.3f) alineada a la derecha
            fila_str += f"{matriz[i][j]:>{ancho}.3f}"

        print(fila_str)







#devuelve la lista de la extension de orden N y sus probabilidades
def extension(alfa, probs, n):
    if n == 1:
        return alfa, probs

    alfa_pre, probs_pre =  extension(alfa, probs, n -1)

    nuevo_alfa = []
    nuevas_probs = []

    for i in range(len(alfa_pre)):
        for j in range(len(alfa)):
            simbolo = alfa_pre[i] + alfa[j]
            nuevo_alfa.append(simbolo)

            probabilidad = probs_pre[i] * probs[j]
            nuevas_probs.append(probabilidad)

    return nuevo_alfa, nuevas_probs



#entr = entriopia(probs)

#print(f"entriopia: {entr}")

def productoMatriz(matriz, vector):
    n = len(matriz)
    vecAux = [0] * n

    for i in range(n):
        for j in range(n):
            vecAux[i] += matriz[i][j] * vector[j]

    return vecAux

def cumpleTolerancia(vec1, vec2, tol = 0.001):
    vec3 = [abs(x-y) for x,y in zip(vec1, vec2)]

    return max(vec3) < tol


def vectorEstacionario(matriz, tol = 0.001):
    n = len(matriz)
    vec = [1/n] * n
    cumple = False
    while not cumple:
        vecAux = productoMatriz(matriz, vec)
        cumple = cumpleTolerancia(vec, vecAux, tol)

        vec = vecAux
    return vec

#CODIGOS
def no_singular(lista):
    for elem in lista:
        for elem2 in lista:
            if elem == elem2:
                return False

    return True


def instantaneo(lista):
    for i in range(len(lista)):
        for j in range(len(lista)):

            if i != j:
                if lista[j].startswith(lista[i]):
                    return False

    return True


def es_ud(lista):
    conjuntos = []
    nueva = []
    for elem in lista:
        for elem2 in lista:
            if elem != elem2:
                ocurre = elem2.startswith(elem)
                if ocurre:
                    nueva.append(elem2[len(elem):])

    while nueva:
        sufijo_actual = nueva.pop(0)

        if sufijo_actual in lista:
            return False

        conjuntos.append(sufijo_actual)

        for elem in lista:
            ocurre = sufijo_actual.startswith(elem)
            if ocurre:
                nuevo_sufijo = sufijo_actual[len(elem):]
                if nuevo_sufijo not in conjuntos and nuevo_sufijo not in nueva:
                    nueva.append(nuevo_sufijo)

            ocurre_inverso = elem.startswith(sufijo_actual)
            if ocurre_inverso:
                nuevo_sufijo = elem[len(sufijo_actual):]
                if nuevo_sufijo not in conjuntos and nuevo_sufijo not in nueva:
                    nueva.append(nuevo_sufijo)

    return True


def obtiene_alfa_codigo(lista):
    cad = ""
    for palabra in lista:
        for letra in palabra:
            if letra not in cad:
                cad += letra
    return cad

def genera_lista_longitud_palabras(lista):
    longitudes = [len(palabra) for palabra in lista]

    return longitudes

#se le pasa el codigo de cada simbolo
def sumatoria_kraft(lista):
    cad = obtiene_alfa_codigo(lista)
    longitudes = genera_lista_longitud_palabras(lista)

    r = len(cad)
    sumatoria = 0
    for longitud in longitudes:
        sumatoria += 1 / (r ** longitud)
    return sumatoria

def entriopia_codigo(probs, lista):
    cadena = obtiene_alfa_codigo(lista)

    r = len(cadena)

    entrio = entriopia(probs, r)
    return entrio

def longitud_media(lista, probs):
    L = sum(p * len(palabra) for p, palabra in zip(probs, lista))

    return L

def es_codigo_compacto(codigos, probabilidades):
    if instantaneo(codigos):
        R = len(obtiene_alfa_codigo(codigos))
        LONGITUDES = genera_lista_longitud_palabras(codigos)
        i = 0
        respuesta = True
        while i < len(codigos) and respuesta:
            limite_superior = math.ceil(-math.log(probabilidades[i], R))
            if LONGITUDES[i] > limite_superior:
                respuesta = False
            i += 1
    else:
        respuesta = False
    return respuesta







