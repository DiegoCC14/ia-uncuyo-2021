<h3>c)</h3>
El punto A nos pide que encontremos un camino optimo desde un punto A a un destino B dentro de un tablero 
de NxN, para este caso yo creo que el algoritmo que encuentra el camino mas optimo es BFS, DFS Limitado 
ingresa a una casilla y busca el objetivo, al no encontrarlo ingresa por el primer adyacente que encuentra 
y asi, el camino que puede trazar DFS Limitado puede llegar a ser de longitud igual a Limite, y dependiendo 
del Limite tomado puede que lo encuentre o no, por lo que puede llegar a dar un camino o no y este podria no 
ser el optimo, BFS en cambio toma los adyacentes y verifica que no sean el objetivo, luego si no lo encuentra,
de sus adyacentes busca por cada uno los adyacentes de estos y asi, siempre buscando primero entre las casillas
mas cercanas al punto Inicio A , de esta forma al encontrarse el objetivo sera por una casilla la cual es 
adyacente a otra y asi hasta llegar a A. tomando tales casillas llegaremos a formar el camino optimo.
