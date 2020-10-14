# Entrega 4 - Diseño del reticulado

COMENTARIO: archivos python utilizados: caso_L.py, caso_D.py, reticulado.py, barra.py y Fu_caso.py.

* Se realiza el siguiente reticulado de largo = 15 m, ancho = 2 m y alto = 3,5 m, compuesto por barras de sección circular de radio R = 8 cm y espesor t = 5 mm. Los nodos 0 y 7 están completamente fijos, mientras que 3 y 10 son libres de deslizar solo en la dirección X (longitudinal). Se considera que además de la carga muerta (D) de peso propio, este se debe diseñar para una sobrecarga de uso (L) que corresponde a una carga distribuida sobre el tablero central de qL = 400 kg/m^2. Se consideran para su análisis 2 casos de combinaciones de carga. Las cuales son: Caso 1: 1.4 D  , Caso 2: 1.2 D + 1.6 L.

* Inicialmente el programa de reticulado entrega los siguientes resultados para tensiones y factores de utilización respectivos:

![1](https://user-images.githubusercontent.com/69275311/95888168-217ba800-0d57-11eb-8585-9700c260adf2.png)
![2](https://user-images.githubusercontent.com/69275311/95888183-25a7c580-0d57-11eb-876d-a47fa34dca22.png)
![3](https://user-images.githubusercontent.com/69275311/95888187-27718900-0d57-11eb-987a-767d817d98a0.png)
![4](https://user-images.githubusercontent.com/69275311/95888195-28a2b600-0d57-11eb-9745-675070fe3e92.png)
![5](https://user-images.githubusercontent.com/69275311/95888202-29d3e300-0d57-11eb-8eac-41f32483e1b2.png)

* El Peso total de la estructura inicial resulta: 24197.43808 [N]

## 1) 
Luego de determinar que la combinacion de carga con mayor valor absoluto es la que involucra cargas vivas y muertas (1,2 D + 1,6 L), se escogieron las barras 3, 4, 18, 19 y 29, cuyo nodos son (4,5), (5,6), (0,4), (7,4) y (6,3) respectivamente. Para elegir las barras se escribió un codigo que identifique las barras que poseen mayor fuerza para así rediseñarlas y optimizar la estructura. Las fuerzas de las barras 3 y 4 antes de ser rediseñadas son iguales a 50.800N y un facto de utilización igual a 0,06, mientras que las tres restantes tienen una fuerza de 23.140N y factor de utilizacion 0,03. Luego de aplicar el rediseño se disminuyen las fuerzas de las barras 3 y 4 a 50.577N y 50.354N, con un factor de utilización de 0,98 y 0,97. Por otro lado las barras 18, y 29 disminuyeron su fuerza a 22.559N y 22.165N con un factor de utilización de 1 y 0,96, mientras que la barra 19 aumento a 23.524 con un factor de utilización de 0,94. Si biene la barra 19 aumento en algo su fuerza, la estrucutura mejoró la distribución de las fuerzas y el peso notablemente, ya que las barras rediseñadas poseen factores de utulización muy cercanos a 1. 


## 2)

Para utilizar la función de rediseño de cada barra utilizada, en primer lugar se seleccionaron con la función rediseñar del reticulado, las 5 fuerzas de mayor magnitud dentro del reticulado. Para esto se fueron almacenando las fuerzas dentro de un vector, guardande el subindice dentro del vector. Luego de elegidas las 5 fuerzas, se utiliza el vector en la función rediseñar de las barras, donde en primer lugar forzamos la fluencia y suponemos que el óptimo está en R=t, aguantando la mayor fuerza y lo hará más liviano. De esa manera ajustamos a 0.97 el FU, lo que generará un aumento en el factor de fluencia a largo plazo, lo que se traduce en las 2 primeras líneas de la función mostrada. Posteriormente con while se comprueba que la esbeltez se deba cumplir, entonces si esto no se cumple, se ajusta y se sube el área con R y t, y se baja el FU si es que FU>1 o λ<300.

Cabe mencionar que para obtener el reticulado rediseñado y los gráficos, se creó un nuevo archivo llamado Fu_caso.py

A continuación se muestra la función rediseñar de las barras:

```
def rediseñar(self, Fu, ret, φ=0.9):

		self.R = np.sqrt(abs(Fu)/(φ*self.σy*np.pi*0.98))
		self.t = np.sqrt(abs(Fu)/(φ*self.σy*np.pi*0.98))
		A = self.calcular_area()
		I = self.calcular_inercia()
		L = self.calcular_largo(ret)
		FU = (abs(Fu)/(φ*A*self.σy))
		i = np.sqrt(I/A)
		λ =L/i
		while FU > 1. and λ<300:
			self.R=1.05*self.R
			self.t=1.05*self.t
		print (f"FU,λ = {FU,λ}")
		return None
```


## 3)
Nuevas fuerzas y factores de utilización para caso dominante:
![TensionesCasoDominante](https://user-images.githubusercontent.com/53920966/95929337-1e55db80-0d9a-11eb-8c3b-d5675f8f567a.png)
![FUcasodominante](https://user-images.githubusercontent.com/53920966/95929399-4b09f300-0d9a-11eb-82bd-078c55dc74f3.png)

Nuevas fuerzas y factores de utilización para caso No dominante:
![Tensiones](https://user-images.githubusercontent.com/53920966/95929451-670d9480-0d9a-11eb-82b0-24aa34cff32c.png)
![FU](https://user-images.githubusercontent.com/53920966/95929454-67a62b00-0d9a-11eb-95f4-dd7117b961fb.png)




## 4)



## 5)

Al observar la nueva distribución obtenida, se observa que los FU se ditribuyeron de mejor manera que originalmente. Los valores globales de los FU aumentaron el valor cumpliendo que FU < 1, y fueran lo más cercano posible, para lograr una correcta optimización. Al rediseñar las barras de la nueva estructura, se generó un cambio en el área de cada sección de las barras, por lo tanto el peso total de la estructura disminuyo de 24197.43808 [N] a 20141.3740 [N]. Si es que se optimiza toda la estructura, podrías significar una reduccion del 50% de su peso original, generanod un ahorro en costos de acero.

Los cambios que se pueden hacer para mejorar aun más el costo de la estructura, es lograr mejorar aún más el peso total, acercándo los demás factores de utilización a 1, o simplemente eliminar aquellas barras cuyo FU son iguales a cero y que no aporten estabilidad a la estructura. Lo que generaría una disminución en el peso total, haciendola más rentable económicamente.
