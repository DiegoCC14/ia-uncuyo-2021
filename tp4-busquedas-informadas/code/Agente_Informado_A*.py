#Nombre: Diego Rinaldo Cazon Condori
#Leg: 12947

import random , statistics
import networkx as nx

class MatrizNew():
		def __init__(self,filas,columnas):
				self.matriz = []
				for i in range(filas):
						self.matriz.append(['[ ]']*columnas)

		def mostrarMatriz(self):
				for x in range(len(self.matriz)):
					print("-",end="")
				print("")
				for x in range(len(self.matriz)-1,-1,-1):
						for i in range(len(self.matriz[0])):
								print(self.matriz[x][i],end=" ")
						print("")
				for x in range(len(self.matriz)):
					print("-",end="")
				print("")

class Tablero( MatrizNew ):
	def __init__( self , tamanio_tablero ):
		MatrizNew.__init__(self,tamanio_tablero,tamanio_tablero)
		self.tablero = self.matriz
		self.size = tamanio_tablero
		self.grafo = nx.Graph() #Representacin del tablero en forma de grafo

	def set_Representacion_Grafo( self ):
		
		for x in range(self.size):
			for y in range(self.size):
				if self.get_value_casila( (x,y) ) != '[O]':
					
					if self.get_value_casila( (x,y) ) == '[S]':
						self.grafo.add_node( (x,y) , value = "S" , recorrido = False , padre = None , peso = 0)
					else:
						self.grafo.add_node( (x,y) , value = None , recorrido = False , padre = None , peso = 0 )

					list_casillas_adyacentes = self.casillas_adyacentes_posibles( (x,y) )
					for casilla in list_casillas_adyacentes:
						self.grafo.add_edge( (x,y) , (casilla[0],casilla[1]) )

		#print( self.grafo.nodes['00'] ) #valor de un nodo
		#print( self.grafo.edges() )

	def casillas_adyacentes_posibles(self, posicion ):
		tamanio_tablero = self.size
		fila = posicion[0]
		columna = posicion[1]
		posibles_movimientos = []
		if fila+1 < tamanio_tablero and self.get_value_casila( (fila+1,columna) ) != "[O]":
			posibles_movimientos.append( (fila+1,columna) )
		if columna+1 < tamanio_tablero and self.get_value_casila( (fila,columna+1) ) != "[O]":
			posibles_movimientos.append( (fila,columna+1) )
		if fila-1 >= 0 and self.get_value_casila( (fila-1,columna) ) != "[O]":
			posibles_movimientos.append( (fila-1,columna) )
		if columna-1 >= 0 and self.get_value_casila( (fila,columna-1) ) != "[O]":
			posibles_movimientos.append( (fila,columna-1) )
		return posibles_movimientos

	def ingresa_objeto_tablero( self , posicion ,simbolo):
		simbolo = '['+simbolo+']'
		self.tablero[ posicion[0] ][ posicion[1] ] = simbolo

	def Ingresar_Obstaculos(self,lista_obstaculos):
		for casilla in lista_obstaculos:
			self.ingresa_objeto_tablero( casilla , "O")

	def Ingresar_Objetivo( self , pos_objetivo ):
		self.ingresa_objeto_tablero( pos_objetivo , "S")
	
	def get_value_casila( self , posicion ):
		return self.tablero[ posicion[0] ][ posicion[1] ]

class Agente_Informado():
	def __init__( self , pos_inicial , pos_objetivo ):
		self.posicion_actual = pos_inicial
		self.pos_objetivo = pos_objetivo #Este Agente conoce la posicion y la va a usar 

	def Ingresando_a_Tablero( self , tablero ):
		tablero.ingresa_objeto_tablero( self.posicion_actual ,'A' )
	
	def Mov_posibles( self, pos_act , tablero ):
		#Buscamos en el mapa caminos posibles
		tamanio_tablero = tablero.size
		fila = pos_act[0]
		columna = pos_act[1]
		posibles_movimientos = []
		if fila+1 < tamanio_tablero and tablero.get_value_casila( (fila+1,columna) ) != "[O]":
			posibles_movimientos.append( (fila+1,columna) )
		if columna+1 < tamanio_tablero and tablero.get_value_casila( (fila,columna+1) ) != "[O]":
			posibles_movimientos.append( (fila,columna+1) )
		if fila-1 >= 0 and tablero.get_value_casila( (fila-1,columna) ) != "[O]":
			posibles_movimientos.append( (fila-1,columna) )
		if columna-1 >= 0 and tablero.get_value_casila( (fila,columna-1) ) != "[O]":
			posibles_movimientos.append( (fila,columna-1) )
		return posibles_movimientos

	def dist_supuesta_a_objetivo( self , posicion ):
		#En columna directa y fila directa cuanto nos cuesta llegar 
		distancia_total =  abs( self.pos_objetivo[0] - posicion[0] )
		distancia_total +=  abs( self.pos_objetivo[1] - posicion[1] )
		return distancia_total
	
	def Busqueda_A_Estrella( self , tablero ):
		
		
		costo = 0 + self.dist_supuesta_a_objetivo( self.posicion_actual )
		cola = [self.posicion_actual]
		dicc_pos_recorrido = { costo : cola } #Diccionario que respetara el costo y el tiempo de ingreso 

		contador = 0
		while len(cola) != 0:
			

			nodo_act = cola.pop(0) #Sacamos al primero de la cola
			

			if tablero.grafo.nodes[nodo_act]["recorrido"] == False: 

				tablero.grafo.nodes[nodo_act]["recorrido"] = True #El nodo actual queda recorrido
			
				contador += 1
				if nodo_act == self.pos_objetivo:
					return contador
				
				nodos_adyacentes = tablero.grafo.adj[ nodo_act ]
				for nodo_ady in nodos_adyacentes:

					if tablero.grafo.nodes[nodo_ady]["recorrido"] == False: #Solo si el nodo no fue recorrido

						tablero.grafo.nodes[nodo_ady]["padre"] = nodo_act #Asignamos padre aunque luego se sobreescriba
						tablero.grafo.nodes[nodo_ady]["peso"] = tablero.grafo.nodes[nodo_act]["peso"] + 1 #peso padre + 1 al nodo adyacente
						peso_actual = tablero.grafo.nodes[nodo_ady]["peso"]
						
						valor_supuesto = peso_actual + self.dist_supuesta_a_objetivo( nodo_ady )

						try:
							cola_pesos = dicc_pos_recorrido[ valor_supuesto ] #Existe el peso
							cola_pesos.append( nodo_ady ) #Anadimos el nodo a la cola					
						except:
							#Genero error de key en diccionario
							#No existe el peso lo creamos
							dicc_pos_recorrido[ valor_supuesto ] = [nodo_ady] #Ahora existe el peso en la cola
				
			cola = [] #Busqueda de la cola a tomar
			list_pesos = sorted( list(dicc_pos_recorrido.keys()) ) #Vemos los pesos ordenados de el diccionario
			for peso in list_pesos:
				if len(dicc_pos_recorrido[peso]) != 0:
					cola = dicc_pos_recorrido[peso]
					break

def lista_par_ordanado_aleatorio( cant_pares_ordenados , tamanio_tablero ):
	lista = []
	for x in range( cant_pares_ordenados ):
		x = random.randint(0,tamanio_tablero-1)
		y = random.randint(0,tamanio_tablero-1)
		lista.append( (x,y) )
	return lista

acomulador = 0
lista_deviacion = []
for x in range(30):
	#--CONFIGURACION --->>>>
	Tamanio_Tablero = 100
	pos_inicial = ( random.randint(0,99) , random.randint(0,99) )
	objetivo = ( random.randint(0,99) , random.randint(0,99) )
	cant_Obstaculos = random.randint(600,1500)
	#--CONFIGURACION --->>>>

	lista_obstaculos = lista_par_ordanado_aleatorio( cant_Obstaculos , Tamanio_Tablero )

	tablero = Tablero( Tamanio_Tablero )
	tablero.Ingresar_Obstaculos( lista_obstaculos )
	tablero.Ingresar_Objetivo( objetivo )

	agente = Agente_Informado( pos_inicial , objetivo)
	agente.Ingresando_a_Tablero( tablero )

	tablero.set_Representacion_Grafo() #Representacion del tablero en grafos luego de ingresar todo

	estados_explorados = agente.Busqueda_A_Estrella( tablero )
	acomulador += estados_explorados
	lista_deviacion.append( estados_explorados )

print( acomulador/30 )
print( statistics.stdev(lista_deviacion) )


