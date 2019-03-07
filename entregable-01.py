#!/usr/bin/python
# -*- coding: ISO-8859-15 -*-

#  Developed by Juan Arteaga Carmona on 5/03/19 16:15
#  Last modified 5/03/19 16:12.
#  Copyright (c) 2019. All rights reserved.



# Ampliación de Inteligencia Artificial
# Problemas de Satisfacción de Restricciones
# Dpto. de C. de la Computación e I.A. (Univ. de Sevilla)
# ===================================================================

# -------------------------------------------------------------------- 
# Los siguientes apartados se proponen como ejercicio de programación que
# contará para la evaluación de la asignatura. Este entregable supone 0.75
# puntos de la nota total de la asignatura.  Se deberá entregar a través de la
# página de la asignatura, en el formulario a tal efecto que estará disponible
# junto a la ficha de alumno.


# IMPORTANTE: No cambiar el nombre ni a este archivo ni a las funciones que se
# piden. Si se entregan con un nombre distintoo con funcn otro nombre, 
# el entregable no será evaluado.
# --------------------------------------------------------------------



## ###################################################################
## HONESTIDAD ACADÉMICA Y COPIAS: la realización de los ejercicios es
## un trabajo personal, por lo que deben completarse por cada
## estudiante de manera individual.  La discusión y el intercambio de
## información de carácter general con los compañeros se permite (e
## incluso se recomienda), pero NO AL NIVEL DE CÓDIGO. Igualmente el
## remitir código de terceros, obtenido a través de la red o cualquier
## otro medio, se considerará plagio.

## Cualquier plagio o compartición de código que se detecte
## significará automáticamente la calificación de CERO EN LA
## ASIGNATURA para TODOS los alumnos involucrados. Por tanto a estos
## alumnos NO se les conservará, para futuras convocatorias, ninguna
## nota que hubiesen obtenido hasta el momento. Independientemente de
## OTRAS ACCIONES DE CARÁCTER DISCIPLINARIO que se pudieran tomar.
## ###################################################################



# -----------------------------------------------------------------------

# Lo que sigue es el código visto en la práctica 01 de clase, incluyendo:
# - Clase PSR para representar problemas de satisfacción de restricciones. 
# - Representación del problema de las n-reinas
# - Implementación del algoritmo AC-3

import random

class PSR:
    """Clase que describe un problema de satisfacción de
    restricciones, con los siguientes atributos:
       variables     Lista de las variables del problema
       dominios      Diccionario que asigna a cada variable su dominio
                     (una lista con los valores posibles)
       restricciones Diccionario que asocia a cada tupla de variables
                     involucrada en una restricción, una función que,
                     dados valores de los dominios de esas variables,
                     determina si cumplen o no la restricción.
                     IMPORTANTE: Supondremos que para cada combinación
                     de variables hay a lo sumo una restricción (por
                     ejemplo, si hubiera dos restricciones binarias
                     sobre el mismo par de variables, consideraríamos
                     la conjunción de ambas). 
                     También supondremos que todas las restricciones
                     son binarias
        vecinos      Diccionario que representa el grafo del PSR,
                     asociando a cada variable, una lista de las
                     variables con las que comparte restricción.

    El constructor recibe los valores de los atributos dominios y
    restricciones; los otros dos atributos serán calculados al
    construir la instancia."""

    def __init__(self, dominios, restricciones):
        """Constructor de PSRs."""

        self.dominios = dominios
        self.restricciones = restricciones
        self.variables = list(dominios.keys())

        vecinos = {v: [] for v in self.variables}
        for v1, v2 in restricciones:
            vecinos[v1].append(v2)
            vecinos[v2].append(v1)
        self.vecinos = vecinos


def n_reinas(n):
    """Devuelve el PSR correspondiente al problema de las n-reinas"""

    def n_reinas_restriccion(x,y):
        return lambda u,v: (abs(x-y) != abs(u-v) and u != v)

    doms = {x:list(range(1,n+1)) for x in range(1,n+1)}
    restrs = dict()
    for x in range(1,n):
        for y in range(x+1,n+1):
            restrs[(x,y)] = n_reinas_restriccion(x,y)
    return PSR(doms,restrs)




def dibuja_tablero_n_reinas(asig):
    """Dibuja el tablero de ajedrez a partir de una solución almacenada en asig"""
    

    def cadena_fila(i,asig):
        cadena="|"
        for j in range (1,n+1):
            if asig[i]==j:
                cadena += "X|"
            else:
                cadena += " |"
        return cadena
    
    n=len(asig)
    print("+"+"-"*(2*n-1)+"+")
    for i in range(1,n):
        print(cadena_fila(i,asig))
        print("|"+"-"*(2*n-1)+"|")
    print(cadena_fila(n,asig))
    print("+"+"-"*(2*n-1)+"+")





def arcos (psr):
    return {(x, y) for x in psr.variables for y in psr.vecinos[x]}

def restriccion_arco(psr, x, y):
    if (x, y) in psr.restricciones:
        return psr.restricciones[(x, y)]
    else:
        return lambda vx, vy: psr.restricciones[(y, x)](vy, vx)

def AC3(psr, doms):
    """Procedimiento para hacer arco consistente un problema de
    satisfacción de restricciones dado. Es destructivo respecto al
    atributo dominios"""

    cola = arcos(psr)
    while cola:
        (x, y) = cola.pop()
        func = restriccion_arco(psr,x, y)
        dom_previo_x = doms[x]
        mod_dom_x = False
        dom_nuevo_x = []
        for vx in dom_previo_x:
            if any(func(vx, vy) for vy in doms[y]):
                dom_nuevo_x.append(vx)
            else:
                mod_dom_x = True
        if mod_dom_x:
            doms[x] = dom_nuevo_x
            cola.update((z, x) for z in psr.vecinos[x] if z != y)
    return doms
# ----------------------------------------------------------------------------
    

# ----------------------------------------------------------------------
# Ejercicio 1
# -----------------------------------------------------------------------

# Modificar la función AC3 para definir una función AC3_parcial(psr,doms) que
# recibiendo un psr y un diccionario doms con asignaciones de dominios a
# variables (en el que no necesariamente están todas las variables), actualiza
# los dominios de doms, de manera que todos los arcos correspondientes a las
# variables de doms sean consisistentes. La función debe efectuar las
# modificaciones necesarias sobre el mismo diccionario doms (es destructiva 
# sobre doms).

# Ejemplos:

# >>> doms={2:[1,3],3:[2,3,4]}
# >>> AC3_parcial(n_reinas(4),doms)
# >>> doms
# {2: [1], 3: [3, 4]}

# >>> doms={2:[1,2,3],3:[2,3,4]}
# >>> AC3_parcial(n_reinas(4),doms)
# >>> doms
# {2: [1, 2], 3: [3, 4]}




def AC3_parcial(psr, doms):
    """
    Actualiza los dominos de manera que todos los arcos sean consistentes. Destructiva sobre los dominios.
    :param psr: PSR de entrada.
    :param doms: Diccionario con las asignaciones de dominios a variables. Permite asignaciones en las que no estan
                 todas las variables
    :return: Dominios actualizados siendo todos los arcos consistentes.
    """

    cola = arcos(psr)
    while cola:
        (x, y) = cola.pop()

        # Comprobamos si x o y no existen en los dominios (ya que no todas las variables deben porque estar indicadas en
        # la variable doms). En el caso de que no existan hacemos que el bucle continue sin prestarle atencion con la
        # instruccion continue. De esta forma, omitimos la necesidad de que todas las variables vengan indicadas en doms
        if x not in doms.keys() or y not in doms.keys():
            continue

        func = restriccion_arco(psr,x, y)
        dom_previo_x = doms[x]
        mod_dom_x = False
        dom_nuevo_x = []
        for vx in dom_previo_x:
            if any(func(vx, vy) for vy in doms[y]):
                dom_nuevo_x.append(vx)
            else:
                mod_dom_x = True
        if mod_dom_x:
            doms[x] = dom_nuevo_x
            cola.update((z, x) for z in psr.vecinos[x] if z != y)
    return doms



# ----------------------------------------------------------------------
# Ejercicio 2
# -----------------------------------------------------------------------
            
# La siguiente función implementa un algoritmo recursivo de backtracking
# básico para la resolución de problema de satisfacción de restricciones:


def psr_backtracking(psr):
    """Backtracking simple para problemas de satisfacción de restricciones""" 

    def consistente(psr,var,val,asig):
        for x in asig:
            if (var,x) in psr.restricciones:
                if not psr.restricciones[(var,x)](val,asig[x]):
                    return False
            elif (x,var) in psr.restricciones:
                if not psr.restricciones[(x,var)](asig[x],val):
                    return False
        return True

    def psr_backtracking_rec(asig,resto):
        if resto==[]:
            return asig
        else:
            var = resto[0]
            nuevo_resto=resto[1:]
            dom_var=psr.dominios[var]
            for val in dom_var: 
                if consistente(psr,var,val,asig): 
                    asig[var]=val   
                    result= psr_backtracking_rec(asig,nuevo_resto)
                    if result is not None:
                        return result
                    del asig[var]
            return None
            
    sol=psr_backtracking_rec(dict(),psr.variables)
    if sol is None:
        print("No tiene solución")
    return sol


# En el algoritmo anterior, siempre se toma la siguiente variable a asignar
# en el orden en el que aparecen (sin heurística) y no se realiza
# propagación de restricciones alguna.
#
# Como mejoras a este procedimiento
# básico, en clase hemos visto la técnica de "forward checking" para propagar
# restricciones cada vez que se asigna un valor a una variable, y también la
# heurística mrv para elegir la siguiente variable a asignar. 

# Es posible ampliar la propagación de restricciones más allá del
# forward checking, combinando backtracking con el algoritmo AC3 de
# consistencia de arcos. En este ejercicio se pide implementar esa mejora. 

# Veámoslo con un ejemplo. En el problema de las 4-reinas, vamos a describir
# cómo serían los pasos del algoritmo de backtracking con forward
# checking, y también cómo serían aplicando backtracking con AC3 (en ambos
# casos hasta la primera solución encontrada). 

# *) Si aplicamos forward checking (fc): 

# ------------------------------
# Asignación parcial (valor 1 de V1): {1:1}
# Resto de dominios, aplicando fc:    {2:[3,4],3:[2,4],4:[2,3]}

# Asignacion parcial (valor 3 de V2): {1:1,2:3}
# Resto de dominios, aplicando fc:    {3:[],4:[2]} (FALLO Y VUELTA ATRÁS)

# Asignación parcial (valor 4 de V2): {1:1,2:4}
# Resto de dominios, aplicando fc:    {3:[2],4:[3]}

# Asignación parcial (valor 2 de V3): {1:1,2:4,3:2}
# Resto de dominios, aplicando fc:    {4:[]} (FALLO Y VUELTA ATRÁS)

# Asignación parcial (valor 2 de V1): {1:2}
# Resto de dominios, aplicando fc:    {2:[4],3:[1,3],4:[1,3,4]}

# Asignación parcial (valor 4 de V2): {1:2,2:4}
# Resto de dominios, aplicando fc:    {3:[1],4:[1,3]}

# Asignación parcial (valor 1 de V3): {1:2,2:4,3:1}
# Resto de dominios, aplicando fc:    {4:[3]}

# Asignación parcial (valor 3 de V4): {1:2,2:4,3:1,4:3} (SOLUCIÓN)
# ------------------------------


# *) Si aplicamos AC3 para propagar las restricciones, los pasos del algoritmo 
# serían: 

# ------------------------------
# Asignación parcial (valor 1 de V1):           {1:1}
# Resto de dominios, aplicando AC3 a 
#  {1:[1],2:[1,2,3,4],3:[1,2,3,4],4:[1,2,3,4]}: {2:[],3:[],4:[]} (FALLO)  

# Asignación parcial (valor 2 de V1):           {1:2}
# Resto de dominios, aplicando AC3 a 
#  {1:[2],2:[1,2,3,4],3:[1,2,3,4],4:[1,2,3,4]}: {2:[4],3:[1],4:[3]}   

# Asignación parcial (valor 4 de V2):                     {1:2,2:4}
# Resto de dominios, aplicando AC3 a {2:[4],3:[1],4:[3]}: {3:[1],4:[3]}   
#  

# Asignación parcial (valor 1 de V3):                {1:2,2:4,3:1}
# Resto de dominios, aplicando AC3 a {3:[1],4:[3]}:  {4:[3]}   

# Asignación parcial (valor 3 de V4): {1:2,2:4,3:1,4:1} (SOLUCIÓN)
# ------------------------------

# Como se observa, en el segundo caso, se generan menos nodos en el árbol de 
# búsqueda. 

# Se pide implementar una función psr_backtracking_ac3_mrv(psr) que devuelva
# una solución a un psr (o None si no tiene solución), aplicando el algoritmo
# de backtracking recursivo en el que además cada vez que se asigna un valor a
# una variable, se aplica AC3 sobre los dominios de las restantes variables
# para propagar restricciones. Como heurística para elegir la siguiente
# variable a asignar, usar MRV (desempatando aleatoriamente).

# NOTA: para aplicar AC3 cada vez, usar la función AC3_parcial, ya que no es
# necesario considerar cada vez todas las variables sino solo la asignada
# recientemente junto con el resto de variables que queden por asignar.  

# Ejemplos (no necesariamente tiene que salir esas soluciones, debido a la
# aleatoriedad para deshacer empates en mrv):

# >>> dibuja_tablero_n_reinas(psr_backtracking_ac3_mrv(n_reinas(4)))
# +-------+
# | |X| | |
# |-------|
# | | | |X|
# |-------|
# |X| | | |
# |-------|
# | | |X| |
# +-------+

# >>> dibuja_tablero_n_reinas(psr_backtracking_ac3_mrv(n_reinas(6)))
# +-----------+
# | | | | |X| |
# |-----------|
# | | |X| | | |
# |-----------|
# |X| | | | | |
# |-----------|
# | | | | | |X|
# |-----------|
# | | | |X| | |
# |-----------|
# | |X| | | | |
# +-----------+

# >>> dibuja_tablero_n_reinas(psr_backtracking_ac3_mrv(n_reinas(14)))
# +---------------------------+
# |X| | | | | | | | | | | | | |
# |---------------------------|
# | | | | | | | |X| | | | | | |
# |---------------------------|
# | | | | | |X| | | | | | | | |
# |---------------------------|
# | | | | | | | | | | | | |X| |
# |---------------------------|
# | | |X| | | | | | | | | | | |
# |---------------------------|
# | | | | | | | | | |X| | | | |
# |---------------------------|
# | | | | | | | | | | | | | |X|
# |---------------------------|
# | | | | |X| | | | | | | | | |
# |---------------------------|
# | | | | | | | | | | |X| | | |
# |---------------------------|
# | |X| | | | | | | | | | | | |
# |---------------------------|
# | | | | | | | | | | | |X| | |
# |---------------------------|
# | | | | | | |X| | | | | | | |
# |---------------------------|
# | | | | | | | | |X| | | | | |
# |---------------------------|
# | | | |X| | | | | | | | | | |
# +---------------------------+




def psr_backtracking_ac3_mrv(psr):
    # Se pide implementar una función psr_backtracking_ac3_mrv(psr) que devuelva
    # una solución a un psr (o None si no tiene solución), aplicando el algoritmo
    # de backtracking recursivo en el que además cada vez que se asigna un valor a
    # una variable, se aplica AC3 sobre los dominios de las restantes variables
    # para propagar restricciones. Como heurística para elegir la siguiente
    # variable a asignar, usar MRV (desempatando aleatoriamente).


    # una variable, se aplica AC3 sobre los dominios de las restantes variables
    # para propagar restricciones.

    """
    Función que aplica backtracking recursivo con seleccion de variable mediante la heurística MRV y ademas, aplica AC3
    sobre los dominios de las restantes variables.
    :param psr: PSR de entrada
    :return: None ó solución al PSR de entrada tras aplicar el algoritmo.
    """

    def consistente(psr, var, val, asig):
        for x in asig:
            if (var, x) in psr.restricciones:
                if not psr.restricciones[(var, x)](val, asig[x]):
                    return False
            elif (x, var) in psr.restricciones:
                if not psr.restricciones[(x, var)](asig[x], val):
                    return False
        return True

    def heuristica_seleccion_variable_y_resto(asig, resto):
        """
        Función que calcula la siguiente variable a escoger según el algoritmo MRV
        :param asig: Asignacion hasta el momento del algoritmo recursivo.
        :param resto: Resto de variables que aun quedan por asignar.
        :return: Devuelve la variable seleccionada, el nuevo resto y el dominio de la variable seleccionada.
        """

        # Recorremos el resto y comprobamos cuantas variables de su dominio son
        # consistentes para guardarlas en un diccionario.
        numero_valores_consistentes= {x:0 for x in resto}
        for i in resto:
            dominio_variable = psr.dominios[i]
            for val in dominio_variable:
                if consistente(psr, i, val, asig):
                    numero_valores_consistentes[i]=numero_valores_consistentes.get(i)+1

        # Comprobamos cual es la variable con menos variables consistentes.
        minimo_numero = min(numero_valores_consistentes.values())
        # print('Valores consistentes: ',numero_valores_consistentes, 'Min:',minimo_numero)

        # Es posible que haya mas de una variable con el mismo numero de consistencias, las guardamos todas en una lista
        opciones_minimas = []
        for k in numero_valores_consistentes.keys():
            if numero_valores_consistentes.get(k) == minimo_numero:
                opciones_minimas.append(k)

        # Si está sola seleccionamos esa y sino seleccionamos una al azar.
        if len(opciones_minimas) > 1:
            opcion = random.choice(opciones_minimas)
        else:
            opcion = opciones_minimas[0]


        variable = opcion
        dom_var = psr.dominios[variable]
        nuevo_resto = resto.copy()
        nuevo_resto.remove(variable)

        # print('Variable: ', variable, '\nResto: ', nuevo_resto)

        return opcion, nuevo_resto, dom_var



    def aplica_ac3_dominios(psr, variable, nuevo_resto, dom_var,asig):
        # cada vez que se asigna un valor a
        # una variable, se aplica AC3 sobre los dominios de las restantes variables
        # para propagar restricciones.


        variables_y_dominios = {x:psr.dominios[x] for x in nuevo_resto}
        copia_asig = asig.copy()


        for i in copia_asig:
            copia_asig[i] = [copia_asig[i]]

        variables_y_dominios = {**variables_y_dominios,**copia_asig}

        print('Asig: ',asig)
        print('var_y_doms_w_asig: ', variables_y_dominios, '\t Variable: ',variable)

        ac3sol = AC3_parcial(psr, variables_y_dominios)
        print('AC3: ', ac3sol)



        for i in ac3sol:
            psr.dominios[i] = ac3sol[i]
            psr.dominios = {**psr.dominios, **copia_asig}



        print(psr.dominios)


        return None


    def psr_backtracking_rec(asig, resto):
        if resto == []:
            print('Asignacion Final: ', asig)
            return asig
        else:
            print('Asignacion Parcial: ', asig)
            variable, nuevo_resto, dom_var = heuristica_seleccion_variable_y_resto(asig, resto)
            # variable = resto[0]
            # nuevo_resto = resto[1:]


            aplica_ac3_dominios(psr, variable, nuevo_resto, dom_var,asig)



            for val in dom_var:
                if consistente(psr, variable, val, asig):
                    asig[variable] = val
                    # print('ASIG: ', asig,'\n------------------------')
                    result = psr_backtracking_rec(asig, nuevo_resto)
                    if result is not None:
                        return result
                    else:
                        # print('del', asig[variable], 'ASIG:',asig)
                        del asig[variable]
            return None

    sol = psr_backtracking_rec(dict(), psr.variables)
    if sol is None:
        print("No tiene solución")
    return sol



















#------------------------------------------------------------------------------
# Ejercicio 3
#------------------------------------------------------------------------------

# Un sudoku es una cuadrícula 9x9, dividida en 9 subcuadrículas 3x3 y en la
# que algunas casillas contienen un número del 1 al 9 y el resto están en
# blanco. Resolver el sudoku consiste en rellenar todos las casillas en
# blanco con números del 1 al 9, de manera que no se repitan números en la
# misma fila, ni en la misma columna, ni en cada subcuadrícula.

#   Definir una función "psr_sudoku(puestas)" que devuelve un PSR asociado a un
# sudoku 9x9; "puestas" es un diccionario que a las coordenadas de las casillas
# inicialmente rellenas, le asigna el valor que tienen. NOTA: se penalizará si 
# se implementa listando manualmente una a una las restricciones del problema. 

#   Usando esta función y el algoritmo de backtracking con AC3 y MRV anterior,
# definir una función "resuelve_sudoku(puestas)" que resuelva Sudokus. Esta
# función debe dibujar la solución encontrada.

# Por ejemplo:

# Sudoku 1

#                 +-------------------+
#                 | |7| ||8|5| || | | |
#                 |-------------------|
#                 | |3| || | | ||5| |7|
#                 |-------------------|
#                 | | | || | |7|| |6| |
#                 |-------------------|
#                 |-------------------|
#                 |4| | || | | || | |1|
#                 |-------------------|
#                 |2|9|3|| | | || | |4|
#                 |-------------------|
#                 | | | ||7| |6|| |9| |
#                 |-------------------|
#                 |-------------------|
#                 | | |2||1|3|9|| | | |
#                 |-------------------|
#                 | | | || | | ||1| | |
#                 |-------------------|
#                 |1| | ||2| | || | | |
#                 +-------------------+

def sudoku1():
    return {(1,2):7, (1,4):8, (1,5):5, (2,2):3, (2,7):5, (2,9):7,
            (3,6):7, (3,8):6, (4,1):4, (4,9):1, (5,1):2, (5,2):9,
            (5,3):3, (5,9):4, (6,4):7, (6,6):6, (6,8):9, (7,3):2,
            (7,4):1, (7,5):3, (7,6):9, (8,7):1, (9,1):1, (9,4):2}

# >>> resuelve_sudoku(sudoku1())
# +-------------------+
# |6|7|1||8|5|3||9|4|2|
# |-------------------|
# |9|3|8||6|2|4||5|1|7|
# |-------------------|
# |5|2|4||9|1|7||3|6|8|
# |-------------------|
# |-------------------|
# |4|6|7||3|9|2||8|5|1|
# |-------------------|
# |2|9|3||5|8|1||6|7|4|
# |-------------------|
# |8|1|5||7|4|6||2|9|3|
# |-------------------|
# |-------------------|
# |7|5|2||1|3|9||4|8|6|
# |-------------------|
# |3|8|6||4|7|5||1|2|9|
# |-------------------|
# |1|4|9||2|6|8||7|3|5|
# +-------------------+

# Sudoku 2 (wikipedia)

#                 +-------------------+
#                 |5|3| || |7| || | | |
#                 |-------------------|
#                 |6| | ||1|9|5|| | | |
#                 |-------------------|
#                 | |9|8|| | | || |6| |
#                 |-------------------|
#                 |-------------------|
#                 |8| | || |6| || | |3|
#                 |-------------------|
#                 |4| | ||8| |3|| | |1|
#                 |-------------------|
#                 |7| | || |2| || | |6|
#                 |-------------------|
#                 |-------------------|
#                 | |6| || | | ||2|8| |
#                 |-------------------|
#                 | | | ||4|1|9|| | |5|
#                 |-------------------|
#                 | | | || |8| || |7|9|
#                 +-------------------+

def sudoku2():
    return {(1,1):5, (1,2):3, (1,5):7, (2,1):6, (2,4):1, (2,5):9,
            (2,6):5, (3,2):9, (3,3):8, (3,8):6, (4,1):8, (4,5):6,
            (4,9):3, (5,1):4, (5,4):8, (5,6):3, (5,9):1, (6,1):7,
            (6,5):2, (6,9):6, (7,2):6, (7,7):2, (7,8):8, (8,4):4,
            (8,5):1, (8,6):9, (8,9):5, (9,5):8, (9,8):7, (9,9):9}

# >>> resuelve_sudoku(sudoku2())
# +-------------------+
# |5|3|4||6|7|8||9|1|2|
# |-------------------|
# |6|7|2||1|9|5||3|4|8|
# |-------------------|
# |1|9|8||3|4|2||5|6|7|
# |-------------------|
# |-------------------|
# |8|5|9||7|6|1||4|2|3|
# |-------------------|
# |4|2|6||8|5|3||7|9|1|
# |-------------------|
# |7|1|3||9|2|4||8|5|6|
# |-------------------|
# |-------------------|
# |9|6|1||5|3|7||2|8|4|
# |-------------------|
# |2|8|7||4|1|9||6|3|5|
# |-------------------|
# |3|4|5||2|8|6||1|7|9|
# +-------------------+

# Sudoku 3

#                 +-------------------+
#                 |9|5| || | | ||6|7| |
#                 |-------------------|
#                 | | | || | |7||3|1| |
#                 |-------------------|
#                 |8| | ||5|6|1|| | | |
#                 |-------------------|
#                 |-------------------|
#                 |2|3| || | | || | | |
#                 |-------------------|
#                 | | |9|| | | ||1| | |
#                 |-------------------|
#                 | | | || | | || |3|7|
#                 |-------------------|
#                 |-------------------|
#                 | | | ||1|4|5|| | |9|
#                 |-------------------|
#                 | |9|4||2| | || | | |
#                 |-------------------|
#                 | |8|5|| | | || |2|1|
#                 +-------------------+


def sudoku3():
    return {(1,1):9, (1,2):5, (1,7):6, (1,8):7, (2,6):7, (2,7):3,
            (2,8):1, (3,1):8, (3,4):5, (3,5):6, (3,6):1, (4,1):2,
            (4,2):3, (5,3):9, (5,7):1, (6,8):3, (6,9):7, (7,4):1,
            (7,5):4, (7,6):5, (7,9):9, (8,2):9, (8,3):4, (8,4):2,
            (9,2):8, (9,3):5, (9,8):2, (9,9):1}

# >>> resuelve_sudoku(sudoku3())
    
# +-------------------+
# |9|5|1||3|2|4||6|7|8|
# |-------------------|
# |6|4|2||8|9|7||3|1|5|
# |-------------------|
# |8|7|3||5|6|1||2|9|4|
# |-------------------|
# |-------------------|
# |2|3|7||4|1|9||8|5|6|
# |-------------------|
# |5|6|9||7|8|3||1|4|2|
# |-------------------|
# |4|1|8||6|5|2||9|3|7|
# |-------------------|
# |-------------------|
# |3|2|6||1|4|5||7|8|9|
# |-------------------|
# |1|9|4||2|7|8||5|6|3|
# |-------------------|
# |7|8|5||9|3|6||4|2|1|
# +-------------------+


