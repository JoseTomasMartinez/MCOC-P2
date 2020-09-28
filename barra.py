# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 17:58:58 2020

@author: Felipe Bravo
"""

import numpy as np

class Barra(object):
    def __init__(self, ni, nj, R, t, E, ρ, σy):
        super(Barra, self).__init__()
        self.ni = ni
        self.nj = nj
        self.R = R
        self.t = t
        self.E = E
        self.ρ = ρ
        self.σy = σy
    def obtener_conectividad(self):
        self.c = [self.ni,self.nj]        
        return self.c
    def calcular_area(self):
        self.A = np.pi()*(self.R**2-(self.R-self.t)**2)
        return A
    def calcular_largo(self,reticulado):
        ret = reticulado
        xi = ret.obtener_coordenada_nodal(self.ni)
        xj = ret.obtener_coordenada_nodal(self.ni)
        L = xi-xj
        return np.sqrt(L(0)**2+L(1)**2+L(2)**2)
    def calcular_peso(self):
        self.p =  self.ρ*self.A*self.L
        return self.p