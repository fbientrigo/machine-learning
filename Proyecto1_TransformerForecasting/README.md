## Datos Completed Forecasted

Convencion de nombres
- `pp` y `tmp`: grupo precipitacion y temperatura
- `_f` quiere decir predicho o pronosticado
- `_o` observados
- `_s` estaticos, tamaño de cuenca por ejemplo
- `mean, min, max` estadistico
- `gfs`, `pdir, era5, imerg` global forecast system y otras fuentes de datos observacionales; `era5` es un modelo; `pdir, imerg, gfs` son satelitaltes


La precipitacion contiene solo min, pero se refiere a la acumulada del dia;
- `_b_none` es sin importancia
- `d1` es la acumulacion de un dia
- `p{n}d` se refeire a plus 3d, osea de haber una fecha; es cuando se hizo el pronostico pero este fue para mas de `n` dias sobre esa fecha; en el ejemplo es cuantos dias mas
    - el `0d` se refeire a hacerlo a las 12 y pronosticar para eld ia (todos son hechos cuando empieza el dia)

*Si me sale 1 de enero en un archivo p3d, entonces el pronostico es para el 4 de enerp*

## Observados


- Siempre existe un `p0d` pues se refeire al dia actual y no a futuro, osea no hay prediccion

___

# Formato
- `date` es la fecha de referencia
- los archivos originales son los datos enteros; los que son floats son previamente generados pero no es lo que 
- `name_id` es algo que se puede botar; proviene de archivos internos

#### archivo extra de informacion
habra un archivo donde se encuentran los
- latencia (no importa por ahora)
- factor de escala
- la unidad probablemente son todas para ese tipo

___

# Columnas
cada columna es un ID de una estacion; 
- ordenadas por region de norte a sur (no se desea que el modelo aprenda a disernir las regiones; pues aprenderia los bias)
- los ID siempre miden 8; de no tener 8 va un 0 alfrente.

___

# Unidades
Las unidades se encuentran escaladas
- `pp` milimetros de lluvia al dia
- `tmp` celcius
en alguno de ellos es Kelvin
Todos los datos tienen un factor de escala; 
para precipitacion el factor de escala es 10; osea que guardo con solo 1 decimal de precision (algunos pueden tener un factor de escala distinto; algunos con 100)
$$
5.1 [\text{ml}] \rightarrow 51 
$$
- en mi caso he de dividir por el factor de escala para obtener las unidades correctas
- el archivo contendra el nombre de la unidad

___


# Que se desea
*Generar un dato que tenga un error similar al que tendria el modelo; 
el pronostico para mañana tienee un error pero pasado tiene uno distinto.*

Con esto se quiere aprender sobre la prediccion de precipitacion / temperatura
- de manera de que sea posible utilizarlos;
- entremedio los datos tienen agujeros, por tanto seria lo ideal poder generarlos

- no deseo llenar el pronostico con las realidades, deseo simular un pronostico
(problema inverso, datos reales y predecir datos pronosticados; aprender a despronosticar)

Los errores:
- los errores son heterocedasticos, y no son normales
- comenzar por temperatura en lugar de precipitacion que es mas facil (la precipitacion posee condiciones como que jamas es negativo)


### Ideas que tuvieron
- correccion cuantil cuantil; curva de cuantiles como una funcion parametrizable
    - problema: en el norte tenia percentiles 0 en la mayoria de lugares;
    - lo que se intento fue operar siempre que no fuera 0

# Ideas que tengo
- el modelo ha de aprender sobre el error (agregandole un factor cedastico a los datos)

$$
P(X) = O(X) + \eta (t)
$$

- $P$ predicho
- $O$ observado
- $\eta (t)$ es un error con el que vienen los datos

$$
P(X) - O(X) = \eta
$$

aprender la distribucion de $\eta$ dentro de los datos que se tienen;
de manera de poder generar los datos previos con 

$$
P(X) \leftarrow O(X) + \eta (t)
$$

- agrupar columnas con errores similares en base a la distribucion que tengan; de manera de poder encontrar un error distinto para cuando analizemos un lugar

$$
\eta(t) = \eta_{\alpha} (t)
$$

donde $\alpha$ sera un grupo de vectores que describen un grupo de climas; obtenidos con KMeans o PCA