from caso_D import caso_D
from caso_L import caso_L
from graficar3d import ver_reticulado_3d
import numpy as np
from numpy import linalg as LA
m = 1.0
cm = m/100
mm = m/1000


a = np.arange(30, dtype=int)
R = 8*cm
t = 5*mm


ret_D = caso_D(R,t)
ret_L = caso_L(R,t)


ver_reticulado_3d(ret_D, 
    	axis_Equal=True, 
    	opciones_barras={
    	"ver_numeros_de_barras": False
    }, 
    llamar_show=True,
    zoom=180.,
    deshabilitar_ejes=True)


#Peso Propio
ret_D.ensamblar_sistema()
ret_D.resolver_sistema()
f_D = ret_D.recuperar_fuerzas()

#Carga Viva
ret_L.ensamblar_sistema()
ret_L.resolver_sistema()
f_L = ret_L.recuperar_fuerzas()

#Combinaciones de carga
f_1 = 1.4*f_D           #Combinacion 1
f_2 = 1.2*f_D + 1.6*f_L #Combinacion 2

#Caso Dominante
Fu=0
if LA.norm(1.2*ret_D.recuperar_fuerzas()+1.6*ret_L.recuperar_fuerzas())>LA.norm(1.4*ret_D.recuperar_fuerzas()):
    Fu=1.2*f_D + 1.6*f_L #Combinacion 2
    CasoDom = "Caso Dominante 1.2 D + 1.6 L"
    print(CasoDom)
elif LA.norm(1.2*ret_D.recuperar_fuerzas()+1.6*ret_L.recuperar_fuerzas())<LA.norm(1.4*ret_D.recuperar_fuerzas()):
    Fu=1.4*f_D
    CasoDom = "Caso Dominante 1.4D"
    print(CasoDom)


# Calcular factores
FU_dom = ret_D.recuperar_factores_de_utilizacion(Fu)
peso = ret_D.calcular_peso_total()
print(f"peso PREDISEÑO reticulado = {peso}")

import matplotlib.pyplot as plt

ver_reticulado_3d(ret_D, 
    opciones_nodos = {
        "usar_posicion_deformada": True,
        "factor_amplificacion_deformada": 60.,
    },
    opciones_barras = {
        "color_barras_por_dato": True,
        "ver_numeros_de_barras": False,
        "ver_dato_en_barras": True,
        "dato": Fu,
        "color_fondo": [1,1,1,0.4]
    }, 
    llamar_show=False,
    zoom=180.,
    deshabilitar_ejes=True)

plt.title(f"Tensiones {CasoDom}")
plt.show()

ver_reticulado_3d(ret_D, 
    opciones_nodos = {
        "usar_posicion_deformada": True,
        "factor_amplificacion_deformada": 60.,
    },
    opciones_barras = {
        "color_barras_por_dato": True,
        "ver_numeros_de_barras": False,
        "ver_dato_en_barras": True,
        "dato": FU_dom,
        "color_fondo": [1,1,1,0.4]
    }, 
    llamar_show=False,
    zoom=180.,
    deshabilitar_ejes=True)

plt.title(f"FU {CasoDom}")
plt.show()


#---------------REDISEÑO-------------
print(Fu[3])
ret_D.rediseñar(Fu)

#----------------CORRER MODELO CON VALORES NUEVOS----------------------
ret_D.ensamblar_sistema()
ret_L.ensamblar_sistema()
ret_D.resolver_sistema()
ret_L.resolver_sistema()
f_D = ret_D.recuperar_fuerzas()
f_L = ret_L.recuperar_fuerzas()

#---------------IDENTIFICAR NUEVOS CASOS-------------------------
#Caso Dominante Luego del rediseño
Fu=0
if LA.norm(1.2*ret_D.recuperar_fuerzas()+1.6*ret_L.recuperar_fuerzas())>LA.norm(1.4*ret_D.recuperar_fuerzas()):
    Fu=1.2*f_D + 1.6*f_L #Combinacion 2
    Fut=1.4*f_D #Combinacion 1
    CasoDom = "Caso Dominante 1.2 D + 1.6 L"
    print(CasoDom)
elif LA.norm(1.2*ret_D.recuperar_fuerzas()+1.6*ret_L.recuperar_fuerzas())<LA.norm(1.4*ret_D.recuperar_fuerzas()):
    Fu=1.4*f_D #Combinacion 1
    Fut=1.2*f_D + 1.6*f_L #Combinacion 2
    CasoDom = "Caso Dominante 1.4D"
    print(CasoDom)


peso = ret_D.calcular_peso_total()
print(f"peso reticulado REDISEÑADO = {peso}")

FU_dom = ret_D.recuperar_factores_de_utilizacion(Fu)
FU_n = ret_D.recuperar_factores_de_utilizacion(Fut)
import matplotlib.pyplot as plt

ver_reticulado_3d(ret_D, 
    opciones_nodos = {
        "usar_posicion_deformada": True,
        "factor_amplificacion_deformada": 60.,
    },
    opciones_barras = {
        "color_barras_por_dato": True,
        "ver_numeros_de_barras": False,
        "ver_dato_en_barras": True,
        "dato": Fu,
        "color_fondo": [1,1,1,0.4]
    }, 
    llamar_show=False,
    zoom=180.,
    deshabilitar_ejes=True)

plt.title(f"Tensiones {CasoDom} Rediseño")
plt.show()

ver_reticulado_3d(ret_D, 
    opciones_nodos = {
        "usar_posicion_deformada": True,
        "factor_amplificacion_deformada": 60.,
    },
    opciones_barras = {
        "color_barras_por_dato": True,
        "ver_numeros_de_barras": False,
        "ver_dato_en_barras": True,
        "dato": FU_dom,
        "color_fondo": [1,1,1,0.4]
    }, 
    llamar_show=False,
    zoom=180.,
    deshabilitar_ejes=True)

plt.title(f"FU {CasoDom} Rediseño")
plt.show()



