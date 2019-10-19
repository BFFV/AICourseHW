# Tarea 2 :mag:

### Nombre: Benjamín Farías Valdés
### Usuario de Github: BFFV

# Reporte

## Heurísticas

Se crearon 3 heurísticas alternativas a la básica propuesta, la principal que se pedía en el enunciado (`sliders_h_alternate`), además de `sliders_h_max` y `sliders_h_avg` para propósitos de testing. Estas son descritas a continuación:

- `sliders_h_alternate`: Heurística principal, propuesta para guiar de manera más eficiente la búsqueda. Está basada en la típica Distancia Manhattan, pero adaptándola al problema de Sliders y sacando su promedio. Como los Sliders permiten cruzar 'por fuera' del tablero y aparecer al extremo opuesto, existían casos en los que la Distancia Manhattan común NO representaba el camino más corto hacia el objetivo. Estos casos fueron detectados de la siguiente manera:

    - Se calcula la distancia horizontal de una casilla con respecto a su objetivo.
    - Si esta es MAYOR a la MITAD del ANCHO del tablero (Horizontal), entonces significa que es más corto avanzar en la dirección opuesta al objetivo y aparecer al OTRO lado del tablero (propiedad de Sliders).
    - Cuando ocurra esto, simplemente se toma el complemento de la distancia horizontal al objetivo con respecto al ANCHO (Horizontal) del tablero (ANCHO - Distancia Horizontal al objetivo), obteniendo así el componente X de la Distancia Manhattan Adaptada. En caso de que la distancia horizontal al objetivo NO sea mayor a la mitad del ANCHO, simplemente se elige como componente X directamente.
    - Se aplica esto mismo a la distancia vertical con respecto al objetivo, pero comparándola con el LARGO del tablero (Vertical), obteniendo así el componente Y de la Distancia Manhattan Adaptada.
    - Finalmente se suman ambos componentes, obteniendo la Distancia Manhattan Adaptada para una casilla.

    - Se aplica este método a cada casilla del tablero, y finalmente se divide por la cantidad de casillas total para obtener el promedio de las Distancias Manhattan Adaptadas. Esto hace que la heurística sea ADMISIBLE, ya que en el mejor caso, será necesario un camino de costo igual al `máximo` entre las Distancias Manhattan Adaptadas de cada casilla para llegar al estado objetivo, y el promedio NUNCA superará a dicho máximo (en el caso extremo será igual, pero NO mayor).

- `sliders_h_max`: Esta heurística corresponde a obtener el máximo entre las Distancias Manhattan Adaptadas de cada casilla, en un intento de evitar que algunas casillas queden mucho más lejos de su lugar correspondiente que otras. Es ADMISIBLE por el mismo argumento que la anterior (aunque en este caso será igual al costo del camino más corto 'ideal'). Fue menos eficiente que `sliders_h_alternate`, por lo que sólo se utilizó para realizar testing.

- `sliders_h_avg`: Esta heurística es casi igual a `sliders_h_alternate`, pero se diferencia sacando el promedio SOLAMENTE entre la cantidad de casillas que NO están en su lugar correcto (la heurística principal SÍ considera las casillas que están en su lugar correcto). Es ADMISIBLE por el mismo argumento que las anteriores. Fue menos eficiente que `sliders_h_alternate`, por lo que sólo se utilizó para realizar testing.

## Comparación de Algoritmos Anytime

- Resultados: El algoritmo `Anytime Weighted A*`, tras encontrar la primera solución, continuó encontrando más soluciones, pero estas mejoraban muy lento en la optimalidad (se demoraba en llegar a soluciones mejores que la actual, la mayoría tenían el MISMO costo). Por otro lado, el algoritmo `Restarting Weighted A*`, tras encontrar la primera solución, logró en las iteraciones posteriores encontrar soluciones que se acercaban más rápido al óptimo.

- Tiempo de Búsqueda: El algoritmo `Anytime Weighted A*` logró encontrar rápidamente varias soluciones en sus posteriores iteraciones, aprovechando que ya tenía las listas OPEN y CLOSED bastante desarrolladas. Por otro lado, el algoritmo `Restarting Weighted A*` tardaba más tiempo en encontrar más soluciones, debido a que tenía que volver a expandir muchos nodos nuevamente al volver a ejecutar `Weighted A*` desde 0.

En la siguiente tabla se muestran los resultados obtenidos utilizando la heurística básica propuesta y la alternativa indicada al comienzo de este reporte, probando ambos algoritmos con W=20 en el test case número 7 (s0) (el tiempo está en segundos):

| Algoritmo    | Costo (h_basic) | Tiempo (h_basic) | Costo (h_alternate) | Tiempo (h_alternate) |
|--------------|-----------------|------------------|---------------------|----------------------|
| AWA* (W=20)  | 7               | 360              | 8                   | 15                   |
| RWA* (W=20)  | 7               | 360              | 7                   | 15                   |

Como conclusión, si se necesitan realizar AJUSTES de soluciones encontradas en POCO tiempo, es recomendable utilizar `Anytime Weighted A*`. En el caso de que se requieran soluciones enfocadas en MEJORAR considerablemente la optimalidad, es mejor utilizar `Restarting Weighted A*`.
