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
    def agregar_restriccion(self, nodo, gdl, valor=0.0):
        if nodo not in self.restricciones:
            self.restricciones[nodo] = [[gdl, valor]]
        else:
            self.restricciones[nodo].append([gdl, valor])
        return

    def agregar_fuerza(self, nodo, gdl, valor):
        if nodo not in self.cargas:
            self.cargas[nodo] = [[gdl, valor]]
        else:
            self.cargas[nodo].append([gdl, valor])
        return

    def ensamblar_sistema(self):
        """Ensambla el sistema de ecuaciones"""
        
        Ngdl = self.Nnodos * self.Ndimensiones

        self.K = np.zeros((Ngdl,Ngdl), dtype=np.double)
        self.f = np.zeros((Ngdl), dtype=np.double)
        self.u = np.zeros((Ngdl), dtype=np.double)

        #Iterar sobre las barras
        for b in self.barras:
            ke = b.obtener_rigidez(self)
            fe = b.obtener_vector_de_cargas(self)

            #2D
            ni = b.obtener_conectividad()[0]
            nj = b.obtener_conectividad()[1]
            d = [2*ni, 2*ni+1, 2*nj, 2*nj+1]  #vector d
            Ndof_per_node = self.Ndimensiones*2

            #MDR
            for i in range(Ndof_per_node):
                p = d[i]
                for j in range(Ndof_per_node):
                    q = d[j]
                    self.K[p,q] += ke[i,j]
                self.f[p] += fe[j]

        return self.K, self.f
    def resolver_sistema(self):
        return
    def recuperar_fuerzas(self):
        return
    def __str__(self):
        s = "nodos:\n"
        for i in range(self.Nnodos):
            s += f"{i} : {self.obtener_coordenada_nodal(i)}\n"
        s += "barras:\n"
        for i in range(len(self.barras)):
        	s += f"{i} : {[self.barras[i].ni,self.barras[i].nj]}\n"
        return s 
