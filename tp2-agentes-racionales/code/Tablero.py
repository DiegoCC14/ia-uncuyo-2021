import os , time , random
#Nombre: Diego Rinaldo Cazon Condori
#Leg: 12947

'''
IMPORTANTE -----------<<<>>>
=> Linea 156 a 159 se encuentran las configuraciones de los agentes reflexivo , aleatorio y Tablero
----------------------<<<>>>
'''

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

class Tablero_Aspiradora(MatrizNew):
	
	def __init__(self,tamanio_tablero):
		MatrizNew.__init__(self,tamanio_tablero,tamanio_tablero)
		self.tablero = self.matriz
		self.size = tamanio_tablero
		self.casillas_sucias = []

	def quitar_suciedad_tablero(self,posicion):
		for casilla in self.casillas_sucias:
			if casilla['Pos'] == posicion :
				casilla['Estado'] = 'L'
				return True
		return False

	def ingresa_suciedad_tablero( self , list_casillas_sucias ):
		for coordenada in list_casillas_sucias:
			self.ingresa_objeto_tablero(coordenada,'S')
			self.casillas_sucias.append({'Pos':coordenada,'Estado':'S'})
	
	def casilla_sucia(self,posicion):
		for casilla in self.casillas_sucias:
			if casilla['Pos'] == posicion :
				return casilla['Estado'] == 'S'
		return False

	def get_casilla(self,posicion):
		return self.tablero[posicion[0]][posicion[1]]
	def ingresa_objeto_tablero( self , posicion ,simbolo):
		simbolo = '['+simbolo+']'
		self.tablero[ posicion[0] ][ posicion[1] ] = simbolo

	def borrar_casilla_tablero( self , posicion ):
		self.tablero[posicion[0]][posicion[1]] = '[ ]'

class Aspiradora():
	
	def mover( self , posicion_actual ,posicion_mover , tablero ):
		tablero.borrar_casilla_tablero( posicion_actual )
		tablero.ingresa_objeto_tablero( posicion_mover ,'A')

	def limpiar(self, posicion_actual , tablero ):
		tablero.quitar_suciedad_tablero( posicion_actual )

class Agente():
	
	def __init__(self , vida_agente ,posicion_inicial ,Aspiradora , tablero):
		self.Aspiradora = Aspiradora
		self.posicion_actual = posicion_inicial
		
		self.mov_posibles_Aspiradora = []
		self.set_mov_posibles_Aspiradora( tablero )
		
		self.vida_agente = vida_agente

	def set_mov_posibles_Aspiradora( self , tablero ):
		tamanio_tablero = tablero.size
		fila = self.posicion_actual[0]
		columna = self.posicion_actual[1]
		posibles_movimientos = []
		if fila+1 < tamanio_tablero:
			posibles_movimientos.append( (fila+1,columna) )
		if columna+1 < tamanio_tablero:
			posibles_movimientos.append( (fila,columna+1) )
		if fila-1 >= 0:
			posibles_movimientos.append( (fila-1,columna) )
		if columna-1 >= 0:
			posibles_movimientos.append( (fila,columna-1) )
		self.mov_posibles_Aspiradora = posibles_movimientos
		#print(self.mov_posibles_Aspiradora)

class Agente_reflexivo( Agente ):
	def __init__(self , vida_agente ,posicion_inicial ,Aspiradora , tablero):
		Agente.__init__(self, vida_agente ,posicion_inicial ,Aspiradora , tablero)
		self.casillas_limpias = 0

	def casilla_actual_sucia(self,tablero):
		return (tablero.casilla_sucia( self.posicion_actual ) == True) #Solo para que se entienda mejor

	def accion_a_realizar_aspiradora( self , tablero ):
		if self.casilla_actual_sucia( tablero ): #Si la casilla esta sucia limpiamos
			self.Aspiradora.limpiar( self.posicion_actual , tablero )
			self.casillas_limpias += 1
			self.vida_agente -= 1
		else:
			num = random.randint( 0,len(self.mov_posibles_Aspiradora )-1)
			sig_casilla = self.mov_posibles_Aspiradora[ num ]
			
			self.Aspiradora.mover( self.posicion_actual , sig_casilla , tablero )
			self.posicion_actual = sig_casilla
			
			self.set_mov_posibles_Aspiradora( tablero )
			self.vida_agente -= 1
			# Nos movemos a otra casilla 

class Agente_simple( Agente ):
	def __init__(self , vida_agente ,posicion_inicial ,Aspiradora , tablero):
		Agente.__init__(self, vida_agente ,posicion_inicial ,Aspiradora , tablero)

	def accion_a_realizar_aspiradora( self , tablero ):

		num = random.randint( 0, len(self.mov_posibles_Aspiradora )+1 )

		if num == len(self.mov_posibles_Aspiradora ) :#Limpiar 
			self.Aspiradora.limpiar( self.posicion_actual , tablero )

		elif num == len(self.mov_posibles_Aspiradora )+1: #No hacer nada
			pass

		else: #Moverse a siguiente casillas
			sig_casilla = self.mov_posibles_Aspiradora[ num ]
			
			self.Aspiradora.mover( self.posicion_actual , sig_casilla , tablero )
			self.posicion_actual = sig_casilla
			
			self.set_mov_posibles_Aspiradora( tablero )
		
		self.vida_agente -= 1
		# Nos movemos a otra casilla 


def lista_par_ordanado_aleatorio( cant_pares_ordenados , tamanio_tablero ):
	lista = []
	for x in range( cant_pares_ordenados ):
		x = random.randint(0,tamanio_tablero-1)
		y = random.randint(0,tamanio_tablero-1)
		lista.append( (x,y) )
	return lista

#----------------->>>>
#Conf. Agente Aleatorio , Reflexivo y Tablero----<<>>
tamanio_tablero = 4 # Tamanio 4x4, son matrices cuadradas
casillas_sucias = 3
vida_agente = 1000
#-----------------<<>>
#----------------->>>>

PROMEDIO_REFLEXIVO = 0
PROMEDIO_ALEATORIO = 0

for m in range(3):
	casillas_simple = 0
	casillas_refl = 0
	casillas_sucias_refl = 0
	casillas_sucias_simpl = 0
	for x in range(40):
		

		#------------->>> AGENTE REFLEXIVO -------->>>
		tablero = Tablero_Aspiradora( tamanio_tablero )
		
		lista_suciedad = lista_par_ordanado_aleatorio( casillas_sucias , tamanio_tablero)

		tablero.ingresa_suciedad_tablero( lista_suciedad )

		x = random.randint(0,tamanio_tablero-1)
		y = random.randint(0,tamanio_tablero-1)

		Asp = Aspiradora()
		tablero.ingresa_objeto_tablero( (x,y) ,'A') #Ingresando aspiradora a tablero
		Agente_Reflex = Agente_reflexivo( vida_agente , (x,y) , Asp , tablero )

		#print('Agente Reflexivo')
		while Agente_Reflex.vida_agente != 0:
			Agente_Reflex.accion_a_realizar_aspiradora( tablero )
			#tablero.mostrarMatriz()

		casillas_refl += Agente_Reflex.casillas_limpias #Contamos casillas limpias

		#------------->>> AGENTE ALEATORIO -------->>>
		tablero = Tablero_Aspiradora( tamanio_tablero )
		tablero.ingresa_suciedad_tablero( lista_suciedad )

		Asp = Aspiradora()
		Agente_Simpl = Agente_simple( vida_agente , (x,y) , Asp , tablero )

		#print('Agente Simple')
		while Agente_Simpl.vida_agente != 0:
			Agente_Simpl.accion_a_realizar_aspiradora( tablero )
			#tablero.mostrarMatriz()

		for casilla in tablero.casillas_sucias:
			if casilla['Estado']!='S':
				casillas_simple+=1 #Contamos casillas limpias


	print('Iteracion: ', m ,' ----------->>')
	print('Porcentaje Reflexivo:')
	promedio_refl_iteracion = (casillas_refl/40)*100/casillas_sucias 
	print( promedio_refl_iteracion )
	print('Porcentaje Aleatorio:')
	promedio_refl_iteracion = (casillas_simple/40)*100/casillas_sucias
	print( promedio_refl_iteracion )
	print('-------------------------------->>')

	PROMEDIO_REFLEXIVO += promedio_refl_iteracion
	PROMEDIO_ALEATORIO += promedio_refl_iteracion

print('PROMEDIO PORCENTUAL REFLEXIVO ')
print(PROMEDIO_REFLEXIVO/3)
print('PROMEDIO PORCENTUAL ALEATORIO ')
print(PROMEDIO_ALEATORIO/3)
