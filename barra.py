import numpy as np

g = 9.81 #[m/s**2]

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
        return [self.ni,self.nj]

    def calcular_area(self):
        A = np.pi*(self.R**2-(self.R-self.t)**2)
        return A

    def calcular_largo(self,reticulado):
        ret = reticulado
        xi = ret.obtener_coordenada_nodal(self.ni)
        xj = ret.obtener_coordenada_nodal(self.nj)
        dij = xi-xj
        return np.sqrt(np.dot(dij,dij))

    def calcular_peso(self,reticulado):
        A = np.pi*(self.R)**2-np.pi*(self.R-self.t)**2
        ret = reticulado
        xi = ret.obtener_coordenada_nodal(self.ni)
        xj = ret.obtener_coordenada_nodal(self.nj)
        dij = xi-xj
        L=np.sqrt(np.dot(dij,dij))
        p = self.ρ * A*L *g
        return p
