import random , csv , time , statistics
import matplotlib.pyplot as plt

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
		self.lista_pos_reinas = []

	def ingresa_objeto_tablero( self , posicion ,simbolo):
		simbolo = '['+simbolo+']'
		self.tablero[ posicion[0] ][ posicion[1] ] = simbolo

	def ingresar_Reinas(self , lista_reinas ):
		for pos_reina in lista_reinas:
			self.lista_pos_reinas.append( pos_reina["pos"] ) 
			self.ingresa_objeto_tablero( pos_reina["pos"] , "R")
		

	def actualizar_posicion_reinas( self , lista_reinas_actualizadas ):
		
		for pos_anterior_reina in self.lista_pos_reinas: #Borramos de la tabla las posiciones de las reinas anteriores
			self.ingresa_objeto_tablero( pos_anterior_reina ,' ')
		self.lista_pos_reinas = []
		for pos_reina in lista_reinas_actualizadas: #Ingresamos las nuevas posiciones de las reinas
			self.ingresa_objeto_tablero( pos_reina["pos"] , "R")
			self.lista_pos_reinas.append( pos_reina["pos"] )
		

	def mover_reina( self , pos_inicial , pos_final ):
		self.ingresa_objeto_tablero( pos_final , "R") #Movemos el objeto del tablero
		self.ingresa_objeto_tablero( pos_inicial , " " ) #Borramos el objeto de la pos inicial del tablero

	def get_value_casila( self , posicion ):
		return self.tablero[ posicion[0] ][ posicion[1] ]

class Agente():
	def __init__( self , pos_reinas ):
		
		self.lista_reinas = [] #Contiene las reinas y sus posiciones y pesodeataque local
		for pos_reina in pos_reinas:
			self.lista_reinas.append( {"pos":pos_reina , 'contador_atacado':0 } ) #Numero alazar en contador_atacado, luego se recalcula 

		self.reinas_atacadas_global = 0 #Contiene globalmente las reinas atacadas

		self.calcula_ataque_local_y_global_entre_reinas() #Calculamos reinas atacadas global y de cada reina

	def calcula_ataque_local_y_global_entre_reinas( self ):
		
		ataque_global = 0
		for reina in self.lista_reinas:
			ataque_local = self.ataque_de_reinas_a_casilla( reina["pos"] ) #Calcula la cantidad de reinas que atacan actualmente
			reina["contador_atacado"] = ataque_local #seteamos la cantidad 
			ataque_global += ataque_local
		self.reinas_atacadas_global = ataque_global

	def ataque_de_reinas_a_casilla( self , pos_casilla ):
		#La reina no puede encontrarse en la misma columna que la pos_casilla

		contador_reinas_atacando = 0 #Contara cuantas reinas estan atacando
		for reina in self.lista_reinas:

			if reina["pos"][1] != pos_casilla[1] and self.casilla_atacada_por_reina( pos_casilla , reina["pos"] ): #Si la casilla se esta atacando entonces sumamos 1
				contador_reinas_atacando +=1

		return contador_reinas_atacando #Retornamos la cantidad de reinas atacando a la casilla #Retorna la cantidad de reinas que atacan la casilla 'pos_casilla'

	def casilla_atacada_por_reina( self, casilla_1 , casilla_2  ): #Retorna True si las 2 casillas pueden estar siendo atacadas entre si. 
		if casilla_1[0] == casilla_2[0] or casilla_1[1] == casilla_2[1]: #Se encuentran en la misma fila o columna, reina atacando
			return True
		if abs(casilla_1[0] - casilla_2[0]) == abs(casilla_1[1] - casilla_2[1]): #Se encuentran en la misma diagonal, reina atacando 
			return True
		return False

	def retorna_casillas_con_valor_minimo( self , tam_tablero ):
		#Buscamos todos los valores minimos de la tabla
		casilla_candidata_a_mover = { "reina_a_mover": [] , "cant_reinas_atacando":9999999} #Luego se recalculara , es solo para entrar 
		for reina in self.lista_reinas :
			columna = reina['pos'][1] #Se encuentra en la misma columna que la reina, lo que cambia es la fila
			for fila in range( tam_tablero ):
				if reina["pos"][0] != fila: #Siempre que no se trate de la misma casilla que reina
					
					casilla = ( fila , columna )
					reinas_atacando = self.ataque_de_reinas_a_casilla( casilla )

					if reinas_atacando < casilla_candidata_a_mover['cant_reinas_atacando']:

						casilla_candidata_a_mover["reina_a_mover"] = [ { "pos_reina":reina["pos"] , "ataque_local": reina['contador_atacado'] , "pos_mover": casilla } ] #La reinas candidatas a mover
						casilla_candidata_a_mover["cant_reinas_atacando"] = reinas_atacando #la cantidad de ataques 
					elif reinas_atacando == casilla_candidata_a_mover['cant_reinas_atacando'] :
						casilla_candidata_a_mover["reina_a_mover"].append( { "pos_reina":reina["pos"] , "ataque_local": reina['contador_atacado'] , "pos_mover": casilla } ) 

		return casilla_candidata_a_mover

	def Cambiar_reina_de_posicion( self , pos_reina , pos_destino ):
		#Cambia de posicion una reina
		for reina in self.lista_reinas:
			if reina["pos"] == pos_reina:
				reina["pos"] = pos_destino
				break

	def Problema_de_las_n_reinas_Hill_Climbing( self , tablero ):
		
		contadorEtapas = 0
		
		estados = [ self.reinas_atacadas_global ]

		Minimo_Local = False
		while Minimo_Local == False:
			
			ATAQUE_GLOBAL_ACTUAL = self.reinas_atacadas_global
			
			reinas_candidatas_cambiar = { 
				"pos_reinas": [ 
					{
					"pos_act":[ (-1,-1) , (-1,-1) ],
					"mov":[ (-1,-1) , (-1,-1) ]
					}
				],
				"disminucion_Ataque": -9999
			}
			
			lista_reinas_restantes = self.lista_reinas.copy()

			for reina_actual in self.lista_reinas:
				
				lista_reinas_restantes.pop( 0 ) #Sacamos la reina_actual

				for reina_restante in lista_reinas_restantes:
					
					ataque_combinado_reinas = reina_actual['contador_atacado'] + reina_restante['contador_atacado']

					nueva_pos_reina_actual = ( reina_restante["pos"][0] , reina_actual["pos"][1] )
					nueva_pos_reina_restante = ( reina_actual["pos"][0] , reina_restante["pos"][1] )

					lista_reina_calculo_casillas = []
					for reina in self.lista_reinas:
						if reina == reina_actual:
							lista_reina_calculo_casillas.append( nueva_pos_reina_actual )
						elif reina == reina_restante:
							lista_reina_calculo_casillas.append( nueva_pos_reina_restante )
						else:
							lista_reina_calculo_casillas.append( reina["pos"] )
					
					amenaza_casilla = 0
					for casilla_a_calcular in [ nueva_pos_reina_actual , nueva_pos_reina_restante ]: 
					
						for casilla in lista_reina_calculo_casillas:
							if casilla != casilla_a_calcular and self.casilla_atacada_por_reina( casilla_a_calcular , casilla ):
								amenaza_casilla += 1 
					
					descuento_ataque_global = ataque_combinado_reinas - amenaza_casilla

					if descuento_ataque_global > reinas_candidatas_cambiar['disminucion_Ataque']:
						reinas_candidatas_cambiar['disminucion_Ataque'] = descuento_ataque_global 
						reinas_candidatas_cambiar['pos_reinas'] = [ { "pos_act":[ reina_actual["pos"] , reina_restante["pos"] ], "mov":[ nueva_pos_reina_actual , nueva_pos_reina_restante ] } ]
					elif descuento_ataque_global == reinas_candidatas_cambiar['disminucion_Ataque']:
						reinas_candidatas_cambiar['pos_reinas'].append( { "pos_act":[ reina_actual["pos"] , reina_restante["pos"] ], "mov":[ nueva_pos_reina_actual , nueva_pos_reina_restante ] } )



			num_al = random.randint( 0 , len( reinas_candidatas_cambiar['pos_reinas'] )-1 )

			self.Cambiar_reina_de_posicion( reinas_candidatas_cambiar['pos_reinas'][num_al]["pos_act"][0] , reinas_candidatas_cambiar['pos_reinas'][num_al]["mov"][0] )
			self.Cambiar_reina_de_posicion( reinas_candidatas_cambiar['pos_reinas'][num_al]["pos_act"][1] , reinas_candidatas_cambiar['pos_reinas'][num_al]["mov"][1] )

			tablero.mover_reina( reinas_candidatas_cambiar['pos_reinas'][num_al]["pos_act"][0] , reinas_candidatas_cambiar['pos_reinas'][num_al]["mov"][0] )
			tablero.mover_reina( reinas_candidatas_cambiar['pos_reinas'][num_al]["pos_act"][1] , reinas_candidatas_cambiar['pos_reinas'][num_al]["mov"][1] )

			self.calcula_ataque_local_y_global_entre_reinas()

			estados.append( self.reinas_atacadas_global )
			print( estados )

			if self.reinas_atacadas_global == 0:
				Minimo_Local = True
			elif ATAQUE_GLOBAL_ACTUAL <= self.reinas_atacadas_global:
				Minimo_Local = True

			contadorEtapas += 1
			
			#tablero.mostrarMatriz()
			#print( "ataque global: ",self.reinas_atacadas_global )
		
		return contadorEtapas
		#return estados

	def Problema_de_las_n_reinas_Simulated_Annealing( self , tablero ):
		Estados_Recorridos = 0
		Minimo_Local = False
		
		estados = [ self.reinas_atacadas_global ]

		while self.reinas_atacadas_global != 0 :
			
			ATAQUE_GLOBAL_ACTUAL = self.reinas_atacadas_global
			
			reinas_candidatas_cambiar = { 
				"pos_reinas": [ 
					{
					"pos_act":[ (-1,-1) , (-1,-1) ],
					"mov":[ (-1,-1) , (-1,-1) ]
					}
				],
				"disminucion_Ataque": -9999
			}
			
			lista_reinas_restantes = self.lista_reinas.copy()

			for reina_actual in self.lista_reinas:
				
				lista_reinas_restantes.pop( 0 ) #Sacamos la reina_actual

				for reina_restante in lista_reinas_restantes:
					
					ataque_combinado_reinas = reina_actual['contador_atacado'] + reina_restante['contador_atacado']

					nueva_pos_reina_actual = ( reina_restante["pos"][0] , reina_actual["pos"][1] )
					nueva_pos_reina_restante = ( reina_actual["pos"][0] , reina_restante["pos"][1] )

					lista_reina_calculo_casillas = []
					for reina in self.lista_reinas:
						if reina == reina_actual:
							lista_reina_calculo_casillas.append( nueva_pos_reina_actual )
						elif reina == reina_restante:
							lista_reina_calculo_casillas.append( nueva_pos_reina_restante )
						else:
							lista_reina_calculo_casillas.append( reina["pos"] )
					
					amenaza_casilla = 0
					for casilla_a_calcular in [ nueva_pos_reina_actual , nueva_pos_reina_restante ]: 
					
						for casilla in lista_reina_calculo_casillas:
							if casilla != casilla_a_calcular and self.casilla_atacada_por_reina( casilla_a_calcular , casilla ):
								amenaza_casilla += 1 
					
					descuento_ataque_global = ataque_combinado_reinas - amenaza_casilla

					if descuento_ataque_global > reinas_candidatas_cambiar['disminucion_Ataque']:
						reinas_candidatas_cambiar['disminucion_Ataque'] = descuento_ataque_global 
						reinas_candidatas_cambiar['pos_reinas'] = [ { "pos_act":[ reina_actual["pos"] , reina_restante["pos"] ], "mov":[ nueva_pos_reina_actual , nueva_pos_reina_restante ] } ]
					elif descuento_ataque_global == reinas_candidatas_cambiar['disminucion_Ataque']:
						reinas_candidatas_cambiar['pos_reinas'].append( { "pos_act":[ reina_actual["pos"] , reina_restante["pos"] ], "mov":[ nueva_pos_reina_actual , nueva_pos_reina_restante ] } )

			if reinas_candidatas_cambiar['disminucion_Ataque'] <= 0: #Si con el paso anterior no disminuimos entonces tomaresmo camino aleatorio para salir del minimo local
				for x in range(3): #Realizamos 3 pasos aleatorios
					num_al_1 = random.randint( 0 , len( self.lista_reinas )-1 )
					reina_alazar_1 = self.lista_reinas[ num_al_1 ]

					num_al_2 = random.randint( 0 , len( self.lista_reinas )-1 )
					reina_alazar_2 = self.lista_reinas[ num_al_2 ] 

					nueva_pos_reina_1 = ( reina_alazar_2["pos"][0] , reina_alazar_1["pos"][1] )
					nueva_pos_reina_2 = ( reina_alazar_1["pos"][0] , reina_alazar_2["pos"][1] )

					self.Cambiar_reina_de_posicion( reina_alazar_1["pos"] , nueva_pos_reina_1 )
					self.Cambiar_reina_de_posicion( reina_alazar_2["pos"] , nueva_pos_reina_2 )

			else:
				num_al = random.randint( 0 , len( reinas_candidatas_cambiar['pos_reinas'] )-1 )

				self.Cambiar_reina_de_posicion( reinas_candidatas_cambiar['pos_reinas'][num_al]["pos_act"][0] , reinas_candidatas_cambiar['pos_reinas'][num_al]["mov"][0] )
				self.Cambiar_reina_de_posicion( reinas_candidatas_cambiar['pos_reinas'][num_al]["pos_act"][1] , reinas_candidatas_cambiar['pos_reinas'][num_al]["mov"][1] )

			tablero.actualizar_posicion_reinas( self.lista_reinas.copy() )
			
			self.calcula_ataque_local_y_global_entre_reinas()

			estados.append( self.reinas_atacadas_global )
			
			Estados_Recorridos += 1

			#tablero.mostrarMatriz()
		
		return Estados_Recorridos
		#return estados
