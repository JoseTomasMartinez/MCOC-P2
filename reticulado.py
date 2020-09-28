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
        self.barras.append(barra)
        return
    def obtener_coordenada_nodal(self, n): 
        if n>= self.Nnodos:
                return
        return self.xyz[n,:]
    def calcular_peso_total(self):
        W = 0.0
        for b in self.barras:
            W += b.calcular_peso(self)
        return W
    def obtener_nodos(self):
        return self.xyz
    def obtener_barras(self):
    	return self.barras
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
        return
