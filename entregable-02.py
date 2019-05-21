# Ampliación de Inteligencia Artificial
# Procesos de Decisión de Markov
# Dpto. de C. de la Computación e I.A. (Univ. de Sevilla)
# ===================================================================

# *******************************************************************
# APELLIDOS: Arteaga Carmona
# NOMBRE: Juan
# *******************************************************************


# -------------------------------------------------------------------- 
# Los siguientes apartados se proponen como ejercicio de programación que
# contará para la evaluación de la asignatura. Este entregable supone 0.75
# puntos de la nota total de la asignatura.  Se deberá entregar a través de la
# página de la asignatura, en el formulario a tal efecto que estará disponible
# junto a la ficha de alumno.


# IMPORTANTE: No cambiar el nombre ni a este archivo ni a las funciones que se
# piden. Si se entregan con un nombre distinto,  el entregable no será
# evaluado. 
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

# Lo que sigue es el código visto en la práctica 03 de clase, incluyendo:
# - Clase genérica MDP para representar procesos de decisión de Markov
# - Subclase para el MDO "Rica y conocida"
# - Función que calcula la valoración respecto de una política dada



import random


class MDP(object):

    """La clase genérica MDP tiene como métodos la función de recompensa R,
    la función A que da la lista de acciones aplicables a un estado, y la
    función T que implementa el modelo de transición. Para cada estado y
    acción aplicable al estado, la función T devuelve una lista de pares
    (ei,pi) que describe los posibles estados ei que se pueden obtener al
    plical la acción al estado, junto con la probabilidad pi de que esto
    ocurra. El constructor de la clase recibe la lista de estados posibles y
    el factor de descuento.

    En esta clase genérica, las funciones R, A y T aparecen sin definir. Un
    MDP concreto va a ser un objeto de una subclase de esta clase MDP, en la
    que se definirán de manera concreta estas tres funciones"""  

    def __init__(self,estados,descuento):

        self.estados=estados
        self.descuento=descuento

    def R(self,estado):
        """Devuelve la recompensa"""
        pass

    def A(self,estado):
        """Devuelve las acciones aplicables"""
        pass
        
    def T(self,estado,accion):
        pass



class Rica_y_Conocida(MDP):
    
    def __init__(self,descuento=0.9):
        # RC: rica y conocida, RD: rica y desconocida, 
        # PC: pobre y conocida, PD: pobre y desconocida 
        self.Rdict={"RC":10,"RD":10,"PC":0,"PD":0}

        self.Tdict={("RC","No publicidad"):[("RC",0.5),("RD",0.5)],
                    ("RC","Gastar en publicidad"):[("PC",1)],
                    ("RD","No publicidad"):[("RD",0.5),("PD",0.5)],
                    ("RD","Gastar en publicidad"):[("PD",0.5),("PC",0.5)],
                    ("PC","No publicidad"):[("PD",0.5),("RC",0.5)],        
                    ("PC","Gastar en publicidad"):[("PC",1)],
                    ("PD","No publicidad"):[("PD",1)],
                    ("PD","Gastar en publicidad"):[("PD",0.5),("PC",0.5)]}
        super().__init__(["RC","RD","PC","PD"],descuento)
        
    def R(self,estado):
        return self.Rdict[estado]
        
    def A(self,estado):
        return ["No publicidad","Gastar en publicidad"]
        
    def T(self,estado,accion):
        return self.Tdict[(estado,accion)]
        

def valoración_respecto_política(pi,mdp, k):
    """Calcula una aproximación a la valoración de los estados respecto de la
    política pi, aplicando el método iterativo"""
    R, T, gamma = mdp.R, mdp.T, mdp.descuento
    V = {e:0 for e in mdp.estados}
    for _ in range(k):
        V1 = V.copy()
        for s in mdp.estados:
            V[s] = R(s) + gamma *(sum([p * V1[s1] for (s1, p) in T(s, pi[s])]))
    return V



# Estos son algunos ejemplos de ejecución del código anterior, visto en la práctica 3.

# >>> mdp_ryc=Rica_y_Conocida()
# >>> pi_ryc_ahorra={"RC":"No publicidad","RD":"No publicidad","PC":"No publicidad","PD":"No publicidad"}
# >>> pi_ryc_2={"RC":"No publicidad","RD":"Gastar en publicidad","PC":"No publicidad","PD":"Gastar en publicidad"}
# >>> pi_ryc_gastar={"RC":"Gastar en publicidad","RD":"Gastar en publicidad","PC":"Gastar en publicidad","PD":"Gastar en publicidad"}
# >>> valoración_respecto_política(pi_ryc_ahorra,mdp_ryc,200)
#{'PC': 14.876033057851238,
# 'PD': 0.0,
# 'RC': 33.05785123966942,
# 'RD': 18.18181818181818}

# >>> valoración_respecto_política(pi_ryc_2,mdp_ryc,200)
#{'PC': 35.887499973543456,
# 'PD': 29.362499973543454,
# 'RC': 50.387499973543456,
# 'RD': 39.36249997354345}

# >>> valoración_respecto_política(pi_ryc_gastar,mdp_ryc,200)
# {'PC': 0.0, 'PD': 0.0, 'RC': 10.0, 'RD': 10.0}



#------------------------------------------------------------------------------
# Ejercicio 1 (es el Ejercicio 7 de la práctica)
#------------------------------------------------------------------------------


# En el tema 3 se ha visto que la valoración de un estado se define como la
# mejor valoración que pueda tener el estado, respecto a todas las políticas
# posibles. Y la política óptima es aquella que en cada estado realiza la
# acción con la mejor valoración esperada (entendiendo por valoración esperada
# la suma de las valoraciones de los estados que podrían resultar al aplicar
# dicha acción, ponderadas por la probabilidad de que ocurra eso). De esta
# manera, la valoración de un estado es la valoración que la política óptima
# asigna al estado.

# Para calcular tanto la valoración de los estados, como la política óptima,
# se han visto dos algoritmos: iteración de valores e iteración de
# políticas. En este ejercicio se pide implementar el algoritmo de iteración
# de políticas. En concreto, se pide definir una función
# "iteración_de_políticas(mdp,k)" que implementa el algoritmo de iteración de
# políticas, y devuelve dos diccionarios, uno con la valoración de los estados
# y otro con la política óptima. Los parámetros de esta función son:

# - mdp: un objeto de la clase MDP.
# - k: el número de iteraciones que se han de aplicar cada vez que se llame a 
#   la función auxiliar "valoración_respecto_política"



# Comparar la política óptima que se obtiene para el ejemplo de "Rica y conocida"
# con las políticas de los ejemplos anteriores y las valoraciones obtenidas.
# Comentar los resultados.
# ---------------------------------------------------------

import time

def iteración_de_políticas(mdp,k):
    """
    :param mdp: Objeto de la clase MDP
    :param k: Numero de iteraciones que se han de aplicar cada vez que se llame a la funcion auxiliar valoración_respecto_política
    :return: Diccionario con valoracion de los estados, Diccionario con política óptima.
    """

    def argmax(list, function):
        return max(list, key=function)

    def valoracion_accion_funcion(pi_s, estado, mdp, funcionValoracion):
        """ Encuentra la valoración esperada de una acción respecto de una función de valoración V"""
        aux = sum((p * funcionValoracion[e] for (e, p) in mdp.T(estado, pi_s)))
        return aux


    estadosMdp = mdp.estados

    # Politica optima, inicialmente random
    # dictPoliticaOptima = {x:random.choice(mdp.A(x)) for x in estadosMdp}

    # Con politica inicial random da bucles infinitos, con politica inicial con todo
    # al primer estado no WTF?? en fin...
    dictPoliticaOptima = {x: mdp.A(x)[0] for x in estadosMdp}

    # Valoracion de la politica optima, incialmente a 0
    dictValoracionEstados = {x:0 for x in estadosMdp}

    #Algoritmo pag 84 diapositivas
    puntoInicial = time.time()

    while True:
        dictValoracionEstados = valoración_respecto_política(dictPoliticaOptima,mdp, k)
        # print("DEBUG: valoracion respecto a politica: {}".format(dictValoracionEstados))
        actializada = False

        for estado in estadosMdp:
            pi_s = argmax(mdp.A(estado), lambda x: valoracion_accion_funcion(x, estado, mdp, dictValoracionEstados))

            if pi_s != dictPoliticaOptima[estado]:
                dictPoliticaOptima[estado] = pi_s
                actializada = True

            # Control de bucles infinitos, no deberia de hacer falta.
            dentrobucle = time.time()
            if dentrobucle-puntoInicial>3:
                break

        if not actializada:
            return dictPoliticaOptima, dictValoracionEstados






mdp_ryc=Rica_y_Conocida()

print("\nEjercicio 1)\n")
print("\n---Política del metodo de iteracion de políticas---")

politica,valoracion = iteración_de_políticas(mdp_ryc,200)
print("Politica óptima: \t\t{}".format(politica))
print("Con una valoracion de: {}".format(valoracion))


#----------------------------------------------------------------------
print("\n---Políticas de los ejemplos anteriores---")

pi_ryc_ahorra = {"RC": "No publicidad", "RD": "No publicidad", "PC": "No publicidad", "PD": "No publicidad"}
print("\nPolítica de ahorro: \t{}".format(pi_ryc_ahorra))
print("Con una valoracion de: {}".format(valoración_respecto_política(pi_ryc_ahorra,mdp_ryc,200)))

pi_ryc_2={"RC":"No publicidad","RD":"Gastar en publicidad","PC":"No publicidad","PD":"Gastar en publicidad"}
print("\nPolítica 2: \t\t\t{}".format(pi_ryc_2))
print("Con una valoracion de: {}".format(valoración_respecto_política(pi_ryc_2,mdp_ryc,200)))

pi_ryc_gastar={"RC":"Gastar en publicidad","RD":"Gastar en publicidad","PC":"Gastar en publicidad","PD":"Gastar en publicidad"}
print("\nPolítica gastar: \t\t{}".format(pi_ryc_gastar))
print("Con una valoracion de: {}".format(valoración_respecto_política(pi_ryc_gastar,mdp_ryc,200)))

print("\n---Comentario---")
print("Como se puede observar, la valoración de la política optima es "
      "mayor que todas las valoraciones de los ejemplos anteriores.\n"
      "Esto se debe a que hemos aplicado el algoritmo de iteración de políticas "
      "y, por lo tanto, hemos encontrado la política que hace que estos valores sean máximos.")

# --------------------------------------------------------------------------


















#------------------------------------------------------------------------------
# Ejercicio 2 
#------------------------------------------------------------------------------


# Aplicar el algoritmo anterior para encontrar políticas óptimas para
# problemas de movimiento de robot en rejillas como el descrito en las
# diapositivas. Supondremos una cuadrícula como la que se describe en la
# diapositiva 72.

# Definir una función 
#     "politica_óptima_cuadrícula(recompensa,ruido,descuento,iter)" 
# que recibe los siguientes argumentos:

# - recompensa: es la recompensa asociada a las casillas no terminales (por
#   defecto -0.04. 
# - ruido: es la probabilidad de que al aplicarse una acción, el robot vaya a
#   una de las casillas perpendiculares al movimiento que en realidad se
#   pretendía. Por defecto es 0.2 (es decir, 0.1 de probabilidad por cada 
#   dirección perpendicular a la que se pretende ir).  
# - descuento: la tasa de descuento aplicada. Por defecto 0.9
# - iter:  número de iteraciones a realizar cada vez que se estima la
#   valoración asociada a una política. Por defecto, su valor es 100. 

# La función debe imprimir por pantalla la cuadrícula en la que en cada casilla 
# se coloca la flecha que describe la acción que recomienda la política óptima 
# que se ha calculado.             


print("\n\nEjercicio 2)---")

class MovimientoRobot(MDP):

    def __init__(self, recompensa, ruido, descuento):

        self.Rdict = {"11": recompensa, "12": recompensa, "13": recompensa, "14": 1,
                      "21": recompensa, "22": -100000000, "23": recompensa, "24": -1,
                      "31": recompensa, "32": recompensa, "33": recompensa, "34": recompensa}

        mitad_ruido = ruido/2.

        self.Tdict = {("11", "arriba"):     [("11", 1 - mitad_ruido), ("12", mitad_ruido)],
                      ("11", "abajo"):      [("21", 1 - ruido),       ("11", mitad_ruido), ("12", mitad_ruido)],
                      ("11", "izquierda"):  [("11", 1 - mitad_ruido), ("21", mitad_ruido)],
                      ("11", "derecha"):    [("12", 1 - ruido),       ("11", mitad_ruido), ("21", mitad_ruido)],

                      ("12", "arriba"):     [("12", 1 - ruido), ("11", mitad_ruido), ("13", mitad_ruido)],
                      ("12", "abajo"):      [("12", 1 - ruido), ("11", mitad_ruido), ("13", mitad_ruido)],
                      ("12", "izquierda"):  [("11", 1 - ruido), ("12", ruido)],
                      ("12", "derecha"):    [("13", 1 - ruido), ("12", ruido)],

                      ("13", "arriba"):     [("13", 1 - ruido), ("12", mitad_ruido), ("14", mitad_ruido)],
                      ("13", "abajo"):      [("23", 1 - ruido), ("14", mitad_ruido), ("12", mitad_ruido)],
                      ("13", "izquierda"):  [("12", 1 - ruido), ("13", mitad_ruido), ("23", mitad_ruido)],
                      ("13", "derecha"):    [("14", 1 - ruido), ("13", mitad_ruido), ("23", mitad_ruido)],

                      # ("14", "arriba"): [("14", 1 - mitad_ruido), ("13", mitad_ruido)],
                      # ("14", "abajo"): [("24", 1 - ruido), ("13", mitad_ruido), ("14", mitad_ruido)],
                      # ("14", "izquierda"): [("13", 1 - ruido), ("14", mitad_ruido), ("24", mitad_ruido)],
                      # ("14", "derecha"): [("14", 1 - mitad_ruido), ("24", mitad_ruido)],

                      ("14", "arriba"):     [],
                      ("14", "abajo"):      [],
                      ("14", "izquierda"):  [],
                      ("14", "derecha"):    [],

                      ("21", "arriba"):     [("11", 1 - ruido), ("21", ruido)],
                      ("21", "abajo"):      [("31", 1 - ruido), ("21", ruido)],
                      ("21", "izquierda"):  [("21", 1 - ruido), ("11", mitad_ruido), ("31", mitad_ruido)],
                      ("21", "derecha"):    [("21", 1 - ruido), ("11", mitad_ruido), ("31", mitad_ruido)],

                    # nunca se llega al 22
                    #   ("22", "arriba"): [("22", 1.)],
                    #   ("22", "abajo"): [("22", 1.)],
                    #   ("22", "izquierda"): [("22", 1.)],
                    #   ("22", "derecha"): [("22", 1.)],

                      ("23", "arriba"):     [("13", 1 - ruido), ("23", mitad_ruido), ("24", mitad_ruido)],
                      ("23", "abajo"):      [("33", 1 - ruido), ("23", mitad_ruido), ("24", mitad_ruido)],
                      ("23", "izquierda"):  [("23", 1 - ruido), ("13", mitad_ruido), ("33", mitad_ruido)],
                      ("23", "derecha"):    [("24", 1 - ruido), ("13", mitad_ruido), ("23", mitad_ruido)],

                      # ("24", "arriba"): [("14", 1 - ruido), ("24", mitad_ruido), ("23", mitad_ruido)],
                      # ("24", "abajo"): [("34", 1 - ruido), ("23", mitad_ruido), ("23", mitad_ruido)],
                      # ("24", "izquierda"): [("23", 1 - ruido), ("34", mitad_ruido), ("14", mitad_ruido)],
                      # ("24", "derecha"): [("24", 1 - ruido), ("34", mitad_ruido), ("14", mitad_ruido)],
                      #
                      ("24", "arriba"):     [],
                      ("24", "abajo"):      [],
                      ("24", "izquierda"):  [],
                      ("24", "derecha"):    [],


                      ("31", "arriba"):     [("21", 1 - ruido),       ("31", mitad_ruido), ("32", mitad_ruido)],
                      ("31", "abajo"):      [("31", 1 - mitad_ruido), ("32", mitad_ruido)],
                      ("31", "izquierda"):  [("31", 1 - mitad_ruido), ("21", mitad_ruido)],
                      ("31", "derecha"):    [("32", 1 - ruido),       ("31", mitad_ruido), ("21", mitad_ruido)],

                      ("32", "arriba"):     [("32", 1 - ruido), ("31", mitad_ruido), ("33", mitad_ruido)],
                      ("32", "abajo"):      [("32", 1 - ruido), ("31", mitad_ruido), ("33", mitad_ruido)],
                      ("32", "izquierda"):  [("31", 1 - ruido), ("32", ruido)],
                      ("32", "derecha"):    [("33", 1 - ruido), ("32", ruido)],

                      ("33", "arriba"):     [("23", 1 - ruido), ("32", mitad_ruido), ("34", mitad_ruido)],
                      ("33", "abajo"):      [("33", 1 - ruido), ("32", mitad_ruido), ("34", mitad_ruido)],
                      ("33", "izquierda"):  [("32", 1 - ruido), ("23", mitad_ruido), ("33", mitad_ruido)],
                      ("33", "derecha"):    [("34", 1 - ruido), ("33", mitad_ruido), ("23", mitad_ruido)],

                      ("34", "arriba"):     [("24", 1 - ruido),       ("34", mitad_ruido), ("33", mitad_ruido)],
                      ("34", "abajo"):      [("34", 1 - mitad_ruido), ("33", mitad_ruido)],
                      ("34", "izquierda"):  [("33", 1 - ruido),       ("34", mitad_ruido), ("24", mitad_ruido)],
                      ("34", "derecha"):    [("34", 1 - mitad_ruido), ("24", mitad_ruido)],
                      }

        super().__init__(["11", "12", "13", "14", "21", "23", "24", "31", "32", "33", "34"], descuento)

    def R(self, estado):
        return self.Rdict[estado]

    def A(self, estado):
        return ["arriba", "abajo", "izquierda", "derecha"]

    def T(self, estado, accion):
        return self.Tdict[(estado, accion)]


def política_óptima_cuadrícula(recompensa=-0.04,ruido=0.2,descuento=0.9,iter=100):
    """
    :param recompensa: Recompensa asociada a las casillas no terminales, por defecto -0.04
    :param ruido: Probabilidad de que al aplicarse una accion, el robot vaya a una de las casillas perpendiculares, por defecto es 0.2, 0.1 por cada perpendicular
    :param descuento: Tasa de descuento aplicada, por defecto 0.9
    :param iter: Numero de iteraciones a realizar cada vez que se estima la valoracion asocuada a una politica, por defecto 100-
    :return: void. Imprime por pantalla la cuadrícula.
    """

    def dibujaCuadricula(dict):
        """Encargada de dibujar la cuadrícula solucion"""
        flechas = {"arriba": "↑",
                   "abajo": "↓",
                   "izquierda": "←",
                   "derecha": "→"
                   }

        print("-----------------")
        print("| " + flechas[dict["11"]]+" | " + flechas[dict["12"]] +" | " +flechas[dict["13"]]   +" | " + " "+" |")
        print("-----------------")
        print("| " + flechas[dict["21"]]+" | " + "*"                 +" | " + flechas[dict["23"]]  +" | " + " "+" |")
        print("-----------------")
        print("| " + flechas[dict["31"]]+" | " + flechas[dict["32"]] +" | " +flechas[dict["33"]]   +" | " + flechas[dict["34"]]+" |")
        print("-----------------")


    mdp_robot = MovimientoRobot(recompensa, ruido, descuento)
    politica, valoracion = iteración_de_políticas(mdp_robot, iter)

    print("Recompensa: {}, Ruido: {}, Descuento: {}, Iteraciones: {}".format(recompensa,ruido,descuento,iter))
    #print(valoracion)
    dibujaCuadricula(politica)


def ejemplosEj2():
    print("\nEjemplo1:")
    política_óptima_cuadrícula(descuento=1)

    print("\nEjemplo2:")
    política_óptima_cuadrícula(recompensa=-2,descuento=1)

    print("\nEjemplo3:")
    política_óptima_cuadrícula(recompensa=-0.1)

    print("\nEjemplo4:")
    política_óptima_cuadrícula(recompensa=10)

    print("\nEjemplo5:")
    política_óptima_cuadrícula(ruido=0.6)

ejemplosEj2()


# Lo siguiente es un ejemplo de resultados obtenidos
# >>> política_óptima_cuadrícula(descuento=1)

# -----------------
# | → | → | → |   |
# -----------------
# | ↑ | * | ↑ |   |
# -----------------
# | ↑ | ← | ← | ← |
# -----------------

# >>> política_óptima_cuadrícula(recompensa=-2,descuento=1)
            
# -----------------
# | → | → | → |   |
# -----------------
# | ↑ | * | → |   |
# -----------------
# | → | → | → | ↑ |
# -----------------
            
# >>> política_óptima_cuadrícula(recompensa=-0.1)

# -----------------
# | → | → | → |   |
# -----------------
# | ↑ | * | ↑ |   |
# -----------------
# | ↑ | → | ↑ | ← |
# -----------------


# >>> política_óptima_cuadrícula(recompensa=10)

# -----------------
# | ← | ← | ← |   |
# -----------------
# | ↓ | * | ← |   |
# -----------------
# | ← | ← | ← | ↓ |
# -----------------

# >>> política_óptima_cuadrícula(ruido=0.6)


# -----------------
# | ↑ | → | ↑ |   |
# -----------------
# | ↑ | * | ← |   |
# -----------------
# | ↑ | ↑ | ← | ↓ |
# -----------------

