import numpy as np
from scipy.linalg import solve, inv

class Reticulado(object):

    def __init__(self):
        super(Reticulado, self).__init__()
        self.xyz = np.zeros((0,3), dtype=np.double)
        self.Nnodos = 0
        self.barras = []
        self.cargas = {}
        self.restricciones = {}
        self.Ndimensiones = 2
        self.tiene_solucion = False

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
        return self.xyz[n, :]

    def calcular_peso_total(self):
        W = 0.0
        for b in self.barras:
            W += b.calcular_peso(self)
        return W

    def obtener_nodos(self):
        return self.xyz[0:self.Nnodos,:].copy()

    def obtener_barras(self):
    	return self.barras

#--------------- Entrega 2 --------------------

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

        # 0 : Aplicar restricciones
        Ngdl = self.Nnodos * self.Ndimensiones
        gdl_libres = np.arange(Ngdl)
        gdl_restringidos = []
        for i in range(Ngdl):
            if i in self.restricciones and len(self.restricciones[i]) == 2:
                gdl_restringidos.append(2 * i)
                gdl_restringidos.append(2 * i + 1)
            elif i in self.restricciones and len(self.restricciones[i]) == 1 and self.restricciones[i][0][0] == 0:
                gdl_restringidos.append(2 * i)
            elif i in self.restricciones and len(self.restricciones[i]) == 1 and self.restricciones[i][0][0] == 1:
                gdl_restringidos.append(2 * i + 1)

        # Identificar gdl_restringidos y llenar u
        # en valores conocidos.
        #
        # Hint: la funcion numpy.setdiff1d es util
        gdl_libres = np.setdiff1d(gdl_libres, gdl_restringidos)

        # Agregar cargas nodales a vector de cargas
        for nodo in self.cargas:
            for carga in self.cargas[nodo]:
                gdl = carga[0]
                valor = carga[1]
                gdl_global = 2*nodo + gdl
                #se agrega al nodo 4
                self.f[gdl_global] += valor

        # 1 Particionar:

        #       K en Kff, Kfc, Kcf y Kcc.
        Kff = self.K[np.ix_(gdl_libres, gdl_libres)]
        Kfc = self.K[np.ix_(gdl_libres, gdl_restringidos)]
        Kcf = Kfc.T
        Kcc = self.K[np.ix_(gdl_restringidos, gdl_restringidos)]

        #       f en ff y fc
        ff = self.f[gdl_libres]
        fc = self.f[gdl_restringidos]

        #       u en uf y uc
        uc = self.u[gdl_restringidos]

        # Resolver para obtener uf -->  Kff uf = ff - Kfc*uc
        # solucionar Kff uf = ff
        uf = solve(Kff, ff-Kfc@uc)
        self.Rc = Kcf @ uf + Kcc @ uc - fc

        # Asignar uf al vector solucion
        self.u[gdl_libres] = uf

        # Marcar internamente que se tiene solucion
        self.tiene_solucion = True

        return self.Rc

    def obtener_desplazamiento_nodal(self, n):
        """Entrega desplazamientos en el nodo n como un vector numpy de (2x1) o (3x1)
        """
        dofs = [2*n, 2*n+1]
        return self.u[dofs]
    
    def recuperar_fuerzas(self):
        """Una vez resuelto el sistema de ecuaciones, se forma un
        vector con todas las fuerzas de las barras. Devuelve un 
        arreglo numpy de (Nbarras x 1)
        """
        
        fuerzas = np.zeros((len(self.barras)), dtype=np.double)
        for i,b in enumerate(self.barras):
            fuerzas[i] = b.obtener_fuerza(self)

        return fuerzas

    def __str__(self):

        s = "nodos:\n"
        for n in range(self.Nnodos):
            s += f"  {n} : ( {self.xyz[n, 0]}, {self.xyz[n, 1]}, {self.xyz[n, 2]}) \n "
        s += "\n\n"

        s += "barras:\n"
        for i, b in enumerate(self.barras):
            n = b.obtener_conectividad()
            s += f" {i} : [ {n[0]} {n[1]} ] \n"
        s += "\n\n"

        s += "restricciones:\n"
        for nodo in self.restricciones:
            s += f"{nodo} : {self.restricciones[nodo]}\n"
        s += "\n\n"

        s += "cargas:\n"
        for nodo in self.cargas:
            s += f"{nodo} : {self.cargas[nodo]}\n"
        s += "\n\n"

        if self.tiene_solucion:
            s += "desplazamientos:\n"
            if self.Ndimensiones == 2:
                uvw = self.u.reshape((-1, 2))
                for n in range(self.Nnodos):
                    s += f"  {n} : ( {uvw[n, 0]}, {uvw[n, 1]}) \n "
        s += "\n\n"

        if self.tiene_solucion:
            f = self.recuperar_fuerzas()
            s += "fuerzas:\n"
            for b in range(len(self.barras)):
                s += f"  {b} : {f[b]}\n"
        s += "\n"
        
        return s
