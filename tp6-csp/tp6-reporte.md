<h2>1)</h2>

Variables: Casillas del tablero vacias, que son del 1 al 9

Dominios: {1, 2, 3, 4, 5, 6, 7, 8, 9}

Restriccion: 2 variables que se encuentren en la misma columna, fila o region (cuadrado) , segun las reglas , no pueden tener igual valor.

<h2>2)</h2>

La arco consistencia es un metodo que usamos para comprobar que en nuestro estado actual es posible encontrar solucion y que las restricciones aun se cumplen.

Primero definimos las variables y los dominios de que son los colores
Dominio = {  red , blue , green }
como ya definimos a WA = red , V = blue
1- tomamos los nodos con color fijo y verificamos que los nodos adyacentes cumplan con la restriccion quedando cada nodo con las siguientes dominios posibles:
    <br>
    SA = {green}
    <br>
    NT = { blue } 
    <br>
    Q   = { red}
    <br>
    NSW = {}
    <br>
2 – NSW queda sin color posible, lo que no puede ser posible.


