from reticulado import Reticulado
from barra import Barra
from math import *

def caso_D(R,t):
    # Unidades base
    m = 1.
    kg = 1.
    s = 1.
    g = 9.81 *m/s**2

    #Unidades derivadas
    N = kg*m/s**2
    cm = m/100
    mm = m/1000
    KN = 1000 *N

    Pa = N / m**2
    KPa = 1000 *Pa
    MPa = 1000 *KPa
    GPa = 1000 *MPa

    #Parametros
    L = 5.0 *m
    H = 3.5 *m
    B = 2.0 *m

    #Inicializar modelo
    ret = Reticulado()

    #Nodos
    ret.agregar_nodo(0     , 0   , 0         ) # 0
    ret.agregar_nodo(L     , 0   , 0         ) # 1
    ret.agregar_nodo(2*L   , 0   , 0         ) # 2
    ret.agregar_nodo(3*L,    0   , 0         ) # 3
    ret.agregar_nodo(L/2   , B/2 , H         ) # 4
    ret.agregar_nodo(3*L/2 , B/2 , H         ) # 5
    ret.agregar_nodo(5*L/2 , B/2 , H         ) # 6
    ret.agregar_nodo(0     , B   , 0         ) # 7
    ret.agregar_nodo(L     , B   , 0         ) # 8
    ret.agregar_nodo(2*L   , B   , 0         ) # 9
    ret.agregar_nodo(3*L   , B   , 0         ) # 10

    #Barras
    props = [R, t, 200*GPa, 7600*kg/m**3, 420*MPa]

    ret.agregar_barra(Barra(0, 1, *props))   # 0
    ret.agregar_barra(Barra(1, 2, *props))   # 1
    ret.agregar_barra(Barra(2, 3, *props))   # 2
    ret.agregar_barra(Barra(4, 5, *props))   # 3
    ret.agregar_barra(Barra(5, 6, *props))   # 4
    ret.agregar_barra(Barra(7, 8, *props))   # 5
    ret.agregar_barra(Barra(8, 9, *props))   # 6
    ret.agregar_barra(Barra(9, 10, *props))   # 7
    ret.agregar_barra(Barra(0, 7, *props))   # 8
    ret.agregar_barra(Barra(1, 8, *props))   # 9
    ret.agregar_barra(Barra(2, 9, *props))   # 10
    ret.agregar_barra(Barra(3, 10, *props))   # 11
    ret.agregar_barra(Barra(0, 8, *props))   # 12
    ret.agregar_barra(Barra(7, 1, *props))   # 13
    ret.agregar_barra(Barra(1, 9, *props))   # 14
    ret.agregar_barra(Barra(8, 2, *props))   # 15
    ret.agregar_barra(Barra(2, 10, *props))   # 16
    ret.agregar_barra(Barra(9, 3, *props))   # 17
    ret.agregar_barra(Barra(0, 4, *props))   # 18
    ret.agregar_barra(Barra(7, 4, *props))   # 19
    ret.agregar_barra(Barra(4, 8, *props))   # 20
    ret.agregar_barra(Barra(4, 1, *props))   # 21
    ret.agregar_barra(Barra(8, 5, *props))   # 22
    ret.agregar_barra(Barra(1, 5, *props))   # 23
    ret.agregar_barra(Barra(5, 9, *props))   # 24
    ret.agregar_barra(Barra(5, 2, *props))   # 25
    ret.agregar_barra(Barra(2, 6, *props))   # 26
    ret.agregar_barra(Barra(9, 6, *props))   # 27
    ret.agregar_barra(Barra(6, 10, *props))   # 28
    ret.agregar_barra(Barra(6, 3, *props))   # 29

    ret.agregar_restriccion(0, 0, 0) #0
    ret.agregar_restriccion(0, 1, 0) #0
    ret.agregar_restriccion(0, 2, 0) #0
    ret.agregar_restriccion(7, 0, 0) #7
    ret.agregar_restriccion(7, 1, 0) #7
    ret.agregar_restriccion(7, 2, 0) #7
    ret.agregar_restriccion(3, 1, 0) #3
    ret.agregar_restriccion(3, 2, 0) #3
    ret.agregar_restriccion(10, 1, 0) #10
    ret.agregar_restriccion(10, 2, 0) #10

    return ret