# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 19:11:25 2020

@author: Felipe Bravo
"""
import numpy as np

class Reticulado(object):
    def __init__(self):
        super(Reticulado, self).__init__()
        self.xyz = np.zeros((0,3), dtype=np.double)
        self.Nnodos = 0
        self.barras = []
        self.cargas = {}
        self.restricciones = {}
    def agregar_nodo(self, x, y, z=0):
        self.xyz.resize((self.Nnodos+1,3))
        self.xyz[self.Nnodos,:] = [x,y,z]
        self.Nnodos +=1
        return
    def agregar_barra(self, barra):
        return
    def obtener_coordenada_nodal(self, n): 
        s = self.xyz[n,:]
        return s
    def calcular_peso_total(self):
        return
    def obtener_nodos(self):
        return 
    def obtener_barras(self):
        return 
    def agregar_restriccion(self, nodo, gdl, valor=0.0):
        return
    def agregar_fuerza(self, nodo, gdl, valor):
        return
    def ensamblar_sistema(self):
        return
    def resolver_sistema(self):
        return
    def recuperar_fuerzas(self):
        return
    def __str__(self):
        s = "Hola soy un reticulado!\n"
        s += "mis nodos son:"
        s += f"{self.xyz}"
        return s