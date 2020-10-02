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

    def obtener_rigidez(self, ret):
        """Devuelve la rigidez ke del elemento. Arreglo numpy de (4x4)
        ret: instancia de objeto tipo reticulado
        """
        xi = (ret.obtener_coordenada_nodal(self.ni))[0]
        xj = (ret.obtener_coordenada_nodal(self.nj))[0]
        yi = (ret.obtener_coordenada_nodal(self.ni))[1]
        yj = (ret.obtener_coordenada_nodal(self.nj))[1]
        L = self.calcular_largo(ret)
        A = self.calcular_area()
        k = self.E*A/L
        T_t = np.matrix([(xi - xj) / L, (yi - yj) / L, (xj - xi) / L, (yj - yi) / L])
        ke = T_t.T @ T_t * k
        return ke

    def obtener_vector_de_cargas(self, ret):
        """Devuelve el vector de cargas nodales fe del elemento. Vector numpy de (4x1)
        ret: instancia de objeto tipo reticulado
        """
        #Implementar
        w = self.calcular_peso(ret)
        fe = np.array([0, -1, 0, -1]).T * w / 2
        return fe

    def obtener_fuerza(self, ret):
        """Devuelve la fuerza se que debe resistir la barra. Un escalar tipo double. 
        ret: instancia de objeto tipo reticulado
        """

        #Implementar
        xi = (ret.obtener_coordenada_nodal(self.ni))[0]
        xj = (ret.obtener_coordenada_nodal(self.nj))[0]
        yi = (ret.obtener_coordenada_nodal(self.ni))[1]
        yj = (ret.obtener_coordenada_nodal(self.nj))[1]
        ui = (ret.obtener_desplazamiento_nodal(self.ni))
        uj = (ret.obtener_desplazamiento_nodal(self.nj))
        L = self.calcular_largo(ret)
        A = self.calcular_area()
        k = self.E*A/L
        T_t = np.array([ (xi - xj)/L, (yi - yj)/L, (xj - xi)/L, (yj - yi)/L])
        ue = np.array([ui[0], ui[1], uj[0], uj[1]])

        #finalmente
        se = k*T_t@ue
        return se
