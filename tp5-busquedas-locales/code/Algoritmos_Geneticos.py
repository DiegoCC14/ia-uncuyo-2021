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

class Agente_Genetico():
	
	def __init__( self , lista_pos_tableros ):
		
		self.tam_poblacion = len( lista_pos_tableros )
		self.tam_tableros = len( lista_pos_tableros[0] )
		
		self.tableros = []
		for nro_tablero in range( self.tam_poblacion ):
			
			dicc_pos_tablero = []
			for pos in lista_pos_tableros[nro_tablero]:
				dicc_pos_tablero.append( {"pos":pos , 'contador_atacado':0 } )
			
			self.tableros.append( { "reinas_atacadas_global":0 , 'posiciones':dicc_pos_tablero } )

		for nro_tabero in range( self.tam_poblacion ): #Calculamos para todoos los tableros el danio entre estas
			self.calcula_ataque_local_y_global_entre_reinas( nro_tabero )

	def calcula_ataque_local_y_global_entre_reinas( self , nro_tabero ):
		
		ataque_global = 0
		for reina in self.tableros[nro_tabero]["posiciones"]:
			ataque_local = self.ataque_de_reinas_a_casilla( reina["pos"] , nro_tabero ) #Calcula la cantidad de reinas que atacan actualmente
			reina["contador_atacado"] = ataque_local #seteamos la cantidad 
			ataque_global += ataque_local
		self.tableros[nro_tabero]["reinas_atacadas_global"] = ataque_global

	def ataque_de_reinas_a_casilla( self , pos_casilla , nro_tabero ):
		#Dado un nro de tablero, este metodo retorna el ataque global entre reinas
		#La reina no puede encontrarse en la misma columna que la pos_casilla

		contador_reinas_atacando = 0 #Contara cuantas reinas estan atacando
		for reina in self.tableros[nro_tabero]["posiciones"]:

			if reina["pos"][1] != pos_casilla[1] and self.casilla_atacada_por_reina( pos_casilla , reina["pos"] ): #Si la casilla se esta atacando entonces sumamos 1
				contador_reinas_atacando +=1

		return contador_reinas_atacando #Retornamos la cantidad de reinas atacando a la casilla #Retorna la cantidad de reinas que atacan la casilla 'pos_casilla'

	def casilla_atacada_por_reina( self, casilla_1 , casilla_2  ): #Retorna True si las 2 casillas pueden estar siendo atacadas entre si. 
		if casilla_1[0] == casilla_2[0] or casilla_1[1] == casilla_2[1]: #Se encuentran en la misma fila o columna, reina atacando
			return True
		if abs(casilla_1[0] - casilla_2[0]) == abs(casilla_1[1] - casilla_2[1]): #Se encuentran en la misma diagonal, reina atacando 
			return True
		return False

	def mostrar_tablero( self , nro_tablero ):
		tablero = Tablero( self.tam_tableros )
		tablero.ingresar_Reinas( self.tableros[nro_tablero]["posiciones"] )
		tablero.mostrarMatriz()

	def mostrar_todos_los_tableros( self ):
		for nro_tablero in range(self.tam_poblacion):
			self.mostrar_tablero(nro_tablero) 
	
	def traer_los_n_menores( self , traer_n_primeros ):
		lista_tablero_primeros = []
		for tablero_actual in self.tableros:
			
			pos_ingresar = 0
			for pos_tablero in range( len(lista_tablero_primeros) ):
				tablero_comparar = lista_tablero_primeros[pos_tablero]
				pos_ingresar +=1
				if tablero_actual["reinas_atacadas_global"] < tablero_comparar["reinas_atacadas_global"]:
					pos_ingresar = pos_tablero
					break 

			lista_tablero_primeros.insert(pos_ingresar,tablero_actual)
		return lista_tablero_primeros[0:traer_n_primeros]

	def cambiar_reina_de_posicion( self , pos_tablero , pos_reina , pos_destino ): #retorna copia de tablero
		#Cambia de posicion una reina
		pos_tab_copy = [] #TENEMOS PROBLEMAS CON REFERENCIA DE LISTA Y DICCIONARIOS
		for reina in pos_tablero:
			pos_tab_copy.append( reina.copy() ) 
		
		for reina in pos_tab_copy:
			if reina["pos"] == pos_reina:
				reina["pos"] = pos_destino
				break
		return pos_tab_copy
	
	def cambiar_posicion_entre_2_reinas(self , pos_tablero , pos_reina_1 , pos_reina_2):
		nueva_pos_1 = ( pos_reina_2[0] , pos_reina_1[1] )
		nueva_pos_2 = ( pos_reina_1[0] , pos_reina_2[1] )
		pos_tablero_nuevo = self.cambiar_reina_de_posicion( pos_tablero.copy() , pos_reina_1 , nueva_pos_1 )
		pos_tablero_nuevo = self.cambiar_reina_de_posicion( pos_tablero_nuevo.copy() , pos_reina_2 , nueva_pos_2 )
		return pos_tablero_nuevo.copy()

	def Problema_de_las_n_reinas_Genetico( self ):
		
		Minimo_Absoluto = False
		Estados_Recorridos = 0

		while Minimo_Absoluto == False:
			#Traigo los n/2 menores de ataque global
			tablero_mejor_adaptados = self.traer_los_n_menores( int( self.tam_poblacion/2) )  #Traigo a los 2 mejor puntuados, menos ataque global


			if tablero_mejor_adaptados[0]["reinas_atacadas_global"] == 0: #Si de los traidos el primero tiene ataque cero entonces terminamos ejecucion
				Minimo_Absoluto = True
			else:

				list_asignacion_hijos = []
				for x in range( int(self.tam_poblacion/2) ): #Generamos la lista con 0 en las posiciones
					list_asignacion_hijos.append(0)

				hijos_disp = self.tam_poblacion
				while hijos_disp > 0:

					pos_padre = random.randint( 0 , int(self.tam_poblacion/2)-1 ) #A que padre se lo asignamos

					if hijos_disp-1 >= 0:
						list_asignacion_hijos[pos_padre] += 1
					else:
						list_asignacion_hijos[pos_padre] += 1
					
					hijos_disp -= 1

				self.tableros = [] #Vacio todo los tableros y agrego los nuevos
				x=0 #Tablero num x
				for tablero in tablero_mejor_adaptados :
					
					for cant_hijos in range( list_asignacion_hijos[x] ):
						num_random_1 = random.randint( 0,self.tam_tableros-1)
						num_random_2 = random.randint( 0,self.tam_tableros-1)

						pos_aleatoria_1 = tablero["posiciones"][num_random_1]["pos"]
						pos_aleatoria_2 = tablero["posiciones"][num_random_2]["pos"]
						
						tablero_pos_nuevas = self.cambiar_posicion_entre_2_reinas( tablero["posiciones"] , pos_aleatoria_1 , pos_aleatoria_2 )

						self.tableros.append( { "reinas_atacadas_global":0 , "posiciones": tablero_pos_nuevas } )

					x+=1

				for nro_tabero in range( self.tam_poblacion ): #Calculamos para todoos los tableros el danio entre estas
					self.calcula_ataque_local_y_global_entre_reinas( nro_tabero )

				Estados_Recorridos += 1
		
		return Estados_Recorridos


def Crear_CSV( Nombre_Archivo , list_diccionario_datos ):
	
	Nombre_Archivo += ".csv" #Agregamos el CSV
	with open( Nombre_Archivo , 'w') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)

		lista_nombre_columnas = [] #Ingresamos al CSV los nombres de las columnas que son de los diccionarios
		for nombre_columnas in list_diccionario_datos[0]:
			lista_nombre_columnas.append( nombre_columnas )
		spamwriter.writerow(lista_nombre_columnas)

		for dicc in list_diccionario_datos:
			lista_fila = []
			for nombre_columna in lista_nombre_columnas:
				lista_fila.append( dicc[nombre_columna] )
			spamwriter.writerow(lista_fila)

def posicion_fila_reina_aleatorio( tamanio_filas ):
	lista_numeros1 = []
	lista_numeros2 = []
	for x in range( tamanio_filas ):
		lista_numeros1.append(x)
		lista_numeros2.append(x)
	
	lista_par_ordenado = []
	while lista_numeros1 != []:
		num1 = random.randint(0,len(lista_numeros1)-1)
		num2 = random.randint(0,len(lista_numeros2)-1)
		x = lista_numeros1.pop(num1)
		y = lista_numeros2.pop(num2)
		lista_par_ordenado.append( (x,y) )
	return lista_par_ordenado

def Generar_Resultados_CSV_Bruto():

	lista_resultados = []

	for tam_tablero_actual in [4,8,10,12,15]:
		
		#Configuracion ====>>>
		tam_tablero = tam_tablero_actual
		tam_poblacion_AG = 90
		#==================>>>

		for x in range(30):
			
			inicio = time.time()

			lista_posiciones = posicion_fila_reina_aleatorio( tam_tablero )	
			
			tablero = Tablero( tam_tablero )
			agente = Agente( lista_posiciones )

			Estados_Necesarios = agente.Problema_de_las_n_reinas_Hill_Climbing( tablero )
			
			fin = time.time()

			dicc = {
				"Algoritmo":"Hill Climbing",
				'Tam_tablero': tam_tablero ,
				'Estados_recorridos':Estados_Necesarios,
				"Val_minimo": int(agente.reinas_atacadas_global/2),
				'poblacion': "NA",
				"time_seg": fin-inicio
			}

			lista_resultados.append( dicc )

		for x in range(30):
			
			inicio = time.time()

			lista_posiciones = posicion_fila_reina_aleatorio( tam_tablero )

			tablero = Tablero( tam_tablero )
			agente = Agente( lista_posiciones )

			Estados_Necesarios = agente.Problema_de_las_n_reinas_Simulated_Annealing( tablero )
			
			fin = time.time()

			dicc = {
				"Algoritmo":"Simulated Annealing",
				'Tam_tablero': tam_tablero ,
				'Estados_recorridos':Estados_Necesarios,
				"Val_minimo": 0 ,#El algoritmo llega al optimo
				'poblacion': "NA",
				"time_seg": fin-inicio
			}

			lista_resultados.append( dicc )
		
		for x in range(30):

			inicio = time.time()

			lista_pos_tableros = []
			for x in range( tam_poblacion_AG ):
				lista_pos_tableros.append( posicion_fila_reina_aleatorio( tam_tablero ) )

			tablero = Tablero( tam_tablero )
			agente = Agente_Genetico( lista_pos_tableros )

			Estados_Necesarios = agente.Problema_de_las_n_reinas_Genetico()

			fin = time.time()

			dicc = {
				"Algoritmo":"Algoritmo Genetico",
				'Tam_tablero': tam_tablero ,
				'Estados_recorridos':Estados_Necesarios,
				"Val_minimo": 0 , #El algoritmo llega al optimo
				'poblacion': tam_poblacion_AG,
				"time_seg": fin-inicio
			}

			lista_resultados.append( dicc )

	Crear_CSV( "Tabla_Resultados_Bruto" , lista_resultados )

def Generar_Graficos_B():

	with open('Tabla_Resultados_Bruto.csv') as filecsv:
		csv_reader = csv.reader(filecsv, delimiter=',') 
		nombre_columnas = True
		
		diccionario = { "Hill Climbing":[] , "Simulated Annealing":[] , "Algoritmo Genetico":[] }
		for fila in csv_reader:

			if nombre_columnas != True and fila[1]=="15": #Tabla 15
				diccionario[fila[0]].append( float( fila[5] ) ) 
			else:
				nombre_columnas = False
	'''
	print( statistics.mean( diccionario['Hill Climbing'] ) ,' -- ', statistics.stdev( diccionario['Hill Climbing'] ) )
	print( statistics.mean( diccionario['Simulated Annealing'] ) ,' -- ', statistics.stdev( diccionario['Simulated Annealing'] ) )
	print( statistics.mean( diccionario['Algoritmo Genetico'] ) ,' -- ', statistics.stdev( diccionario['Algoritmo Genetico'] ) )
	'''

	data = [ diccionario['Hill Climbing'] , diccionario['Simulated Annealing'] , diccionario['Algoritmo Genetico'] ]
	data = [ diccionario['Hill Climbing'] , diccionario['Simulated Annealing'] ]

	plt.boxplot(data) 
	plt.show()

#Generar_Resultados_CSV_Bruto()

#Generar_Graficos_B()
