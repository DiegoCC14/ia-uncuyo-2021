#Nombre: Diego Rinaldo Cazon Condori
#Leg: 12947

'''
IMPORTANTE -----------<<<>>>
=> Linea 106 a 111 se encuentran las configuraciones del agente y Tablero
----------------------<<<>>>
'''

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
	
	def get_value_casila( self , posicion ):
		return self.tablero[ posicion[0] ][ posicion[1] ]


class Agente_objetos():
	def __init__( self , pos_ini ):
		self.posicion_actual = pos_ini #Posicion en mapa fisicamente del agente

	def Ingresando_a_Tablero( self , tablero ):
		tablero.ingresa_objeto_tablero( self.posicion_actual ,'A' )

	def Distancia_Directa_Casillas_Mas_Lejana( self , tam_tablero ):
		#en tablero de tam5: (0,0) tiene casilla mas lejana (4,4) igual que (1,1) y (2,2) siempre que nos podamos mover en 4 direcciones
		#Simplificamos llevando todo punto al primer cuadrante de [0 a (tam_tablero/2) en fila y columna] = primer cuadrante
		fila = self.posicion_actual[0]
		columna = self.posicion_actual[1]
		#Llevamos la posicion al primer cuadrante del tablero pra simplificar cuentas
		if ( fila > (tam_tablero/2) ):
			fila = (tam_tablero-1) - fila
			
		if ( columna > (tam_tablero/2) ):
			columna = (tam_tablero-1) - columna
		fila_1_cuadrante = fila #Fila se encuentra en 1er cuadrante
		col_1_cuadrante = columna #Columna se encuentra en 1er cuadrante

		#Calculamos la cantidad de aristas entre la pos_1_cuadrante y el casillero mas lejano
		fila_lejana = tam_tablero-1
		columna_lejana = tam_tablero-1
		#Retornamos la cantidad de casillas que nos cuesta llegar a casilla mas lejana
		return (fila_lejana-fila_1_cuadrante) + (columna_lejana-col_1_cuadrante)

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

	def Busqueda_objetivo_en_tablero_met_anchura( self ,pos_objetivo , tablero ):
		if self.posicion_actual != pos_objetivo:
			
			diccionario_pos_recorridas = { str( self.posicion_actual ) :'R'} #R de recorrido
			casillas_posibles = [ self.posicion_actual ]
			diccionario_recorrido = {str( self.posicion_actual ):str( self.posicion_actual )}
			
			contador_casillas_recorridas = 0
			while len( casillas_posibles ) != 0:
				
				casilla = casillas_posibles.pop(0)
				
				contador_casillas_recorridas += 1

				casillas_mov_posible = Agente.Mov_posibles( casilla , tablero )
				diccionario_pos_recorridas[ str( casilla ) ] = 'R' #Registramos casilla actual
				for casilla_dudosa in casillas_mov_posible:
					
					if casilla_dudosa == pos_objetivo:
						diccionario_recorrido[str(casilla_dudosa)] = diccionario_recorrido[str(casilla)] + str(casilla_dudosa)
						return diccionario_recorrido , contador_casillas_recorridas
					else:
						try:
							diccionario_pos_recorridas[str(casilla_dudosa)] #Como no encuentra la llave genera error
						except:
							diccionario_recorrido[str(casilla_dudosa)] = diccionario_recorrido[str(casilla)] + str(casilla_dudosa) #Guardando camino
							casillas_posibles.append( casilla_dudosa ) #Lo metemoa a la lista para buscar adyacentes
							diccionario_pos_recorridas[ str( casilla_dudosa ) ] = 'R' #Registramos casilla para no recorrer
				
		else:
			return [posicion_actual] #El camino es la misma pos actual

	def Busqueda_objetivo_en_tablero_met_profundidad( self , pos_objetivo , tablero ):
		
		limite = 5*self.Distancia_Directa_Casillas_Mas_Lejana( tablero.size )

		if self.posicion_actual != pos_objetivo:
			#print( tablero.grafo.nodes[ fil_pos+col_pos ] )
			#print('ENCONTRADO:')
			#print( tablero.grafo.adj[ fil_pos+col_pos ] ) 
			pila_nodos = [ self.posicion_actual ]
			casillas_recorridas = 1
			while len(pila_nodos) != 0:
				
				nodo = pila_nodos.pop(0)

				if nodo == pos_objetivo:
					return casillas_recorridas
				if tablero.grafo.nodes[nodo]['recorrido'] == False and tablero.grafo.nodes[nodo]['peso'] != limite:
					casillas_recorridas += 1
					nodos_adyacentes = tablero.grafo.adj[ nodo ] #Retorna los nodos adyacentes

					for value_nodo in nodos_adyacentes:
						if tablero.grafo.nodes[value_nodo]['recorrido'] == False:
							pila_nodos = [value_nodo] + pila_nodos #Agregamos a la pila el nodo
							tablero.grafo.nodes[value_nodo]['padre'] = nodo
							tablero.grafo.nodes[value_nodo]['peso'] = tablero.grafo.nodes[nodo]['peso'] + 1 
				tablero.grafo.nodes[nodo]['recorrido'] = True

		else:
			return 0 #El camino es la misma pos actual
		

def lista_par_ordanado_aleatorio( cant_pares_ordenados , tamanio_tablero ):
	lista = []
	for x in range( cant_pares_ordenados ):
		x = random.randint(0,tamanio_tablero-1)
		y = random.randint(0,tamanio_tablero-1)
		lista.append( (x,y) )
	return lista

#Diego Rinaldo Cazon Condori
#Legajo: 12947



acomulador_casillas_recorridas_anchura = 0
acomulador_casillas_recorridas_prof = 0
busqueda_correcta = 30

lista_resultados_anchu = []
lista_resultados_profu = []

for x in range(30):

	#--CONFIGURACION --->>>>
	Tamanio_Tablero = 100
	pos_inicial = ( random.randint(0,99) , random.randint(0,99) )
	objetivo = ( random.randint(0,99) , random.randint(0,99) )
	cant_Obstaculos = random.randint(600,1500)
	#--CONFIGURACION --->>>>

	tablero = Tablero(Tamanio_Tablero)
	lista_obstaculos = lista_par_ordanado_aleatorio(cant_Obstaculos,Tamanio_Tablero)
	tablero.Ingresar_Obstaculos( lista_obstaculos )

	tablero.ingresa_objeto_tablero( objetivo , 'S')

	Agente = Agente_objetos( pos_inicial )
	Agente.Ingresando_a_Tablero( tablero )

	tablero.set_Representacion_Grafo() #Generamos el grafo
	casillas_recorridas_prof = Agente.Busqueda_objetivo_en_tablero_met_profundidad( objetivo ,tablero )
	print("Casillas_Recorridas Prof: ", casillas_recorridas_prof)
	if casillas_recorridas_prof == None:
		#input("")
		casillas_recorridas_prof = 0
		busqueda_correcta -=1
	else:
		lista_resultados_profu.append( casillas_recorridas_prof )	
	acomulador_casillas_recorridas_prof += casillas_recorridas_prof
	

	Solucion , casillas_recorridas = Agente.Busqueda_objetivo_en_tablero_met_anchura( objetivo , tablero )
	lista_resultados_anchu.append( casillas_recorridas )
	print("Casillas_Recorridas Anch: ", casillas_recorridas)
	acomulador_casillas_recorridas_anchura += casillas_recorridas
	'''
	print('Solucion:')
	if Solucion!=None:
		print( Solucion[str(objetivo)] )
	else:
		print('No existe solucion')
	'''
	#print( Agente.Busqueda_objetivo_en_tablero_met_anchura( objetivo , tablero )[str( (1, 2) )] )

	'''
	tablero.mostrarMatriz()

	father = tablero.grafo.nodes[str(objetivo[0])+str(objetivo[1])]['padre']
	while father!= None:
		print( father )
		father = tablero.grafo.nodes()[father]['padre']
	'''

print( acomulador_casillas_recorridas_anchura/30 )
print( acomulador_casillas_recorridas_prof/busqueda_correcta )

print( statistics.stdev( lista_resultados_anchu ) )
print( statistics.stdev( lista_resultados_profu ) )
