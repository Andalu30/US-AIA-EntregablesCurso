# Ampliación de Inteligencia Artificial
# Procesos de Decisión de Markov
# Dpto. de C. de la Computación e I.A. (Univ. de Sevilla)
# ===================================================================

# *******************************************************************
# APELLIDOS:
# NOMBRE: 
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
        pass

    def A(self,estado):
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
            V[s] = R(s) + gamma *(sum([p * V1[s1] for (s1,p) in T(s, pi[s])]))
    return V



# Estos son algunos ejemplos de ejecución del código anterior, visto en la práctica 3.

# >>> mdp_ryc=Rica_y_Conocida()

# >>> pi_ryc_ahorra={"RC":"No publicidad","RD":"No publicidad",
#                    "PC":"No publicidad","PD":"No publicidad"}

# >>> pi_ryc_2={"RC":"No publicidad","RD":"Gastar en publicidad",
#               "PC":"No publicidad","PD":"Gastar en publicidad"}

# >>> pi_ryc_gastar={"RC":"Gastar en publicidad","RD":"Gastar en publicidad",
#                  "PC":"Gastar en publicidad","PD":"Gastar en publicidad"}

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

