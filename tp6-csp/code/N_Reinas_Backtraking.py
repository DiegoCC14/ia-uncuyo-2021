#Ciencias de la computacion - Facultad de ingenieria - Universidad Nacional de Cuyo
#Diego Rinaldo Cazon Condori
#diego.xmen123@gmail.com

#Problema de la n reinas
#Solucion con Backtraking

#--------------------------------->>>
#--------------------------------->>>
import time 

def Crea_Tabla(fila,columna):
	#retorna una tabla de dimencion fila x columna
	tablero = []
	for i in range(fila):
		lista_columna = [ 0 for x in range(columna) ]
		tablero.append(lista_columna)
	return tablero

def Muestra_Tabla(tablero):
	for i in range(len(tablero)):
		for x in range(len(tablero[0])):
			print(tablero[i][x],end=' ')
		print('')

def Posicionar_Reinas(tablero,Lista_Reinas):
	contador = 0
	for Reina in Lista_Reinas:
		x = Reina[0]
		y = Reina[1]
		tablero[x][y] = 'R'
	return tablero
#--------------------------------->>>
#--------------------------------->>>

def Problema_de_las_8_Reinas(Cant_Reinas,Posicion_Reinas_Solucion,fila):
	#retorna lista con posicion de las reinas ,en otro caso None

	for columna in range(Cant_Reinas):

		Posicion_Actual = [fila,columna]
		
		Colicion = Colicion_Entre_Reinas(Cant_Reinas,Posicion_Reinas_Solucion,Posicion_Actual) #Verificamos que no haya coliciones entre reynas

		if Colicion == False: #No existe colicion

			if fila ==  Cant_Reinas-1: #Se encontraron todas las posiciones solucion
				
				Posicion_Reinas_Solucion.append(Posicion_Actual)
				
				return (Posicion_Reinas_Solucion) #Retornamos la lista
			
			Posicion_Reinas_Solucion.append(Posicion_Actual)

			solucion = Problema_de_las_8_Reinas(Cant_Reinas,Posicion_Reinas_Solucion,fila+1)  
			
			if solucion != None:
				return( solucion )
			
			Posicion_Reinas_Solucion.pop() #No es solucion, lo sacamos de la lista			
		
		#Si existe colicion ,entonces se sigue buscando columna libre 

def Colicion_Entre_Reinas(Cant_Reinas,Posicion_Reinas_Solucion,Posicion_Actual):
	#Si existe colicion entre reinas retorna True , sino retorna False
	x_act = Posicion_Actual[0] 
	y_act = Posicion_Actual[1]

	for posicion_Reina in Posicion_Reinas_Solucion:
		
		x = posicion_Reina[0]
		y = posicion_Reina[1]
		
		diferencia_x = x_act - x 
		
		if (y == y_act): #Calculamos la columna
			return True
		elif y - y_act > 0: #Diagonal negativa 
			if y-diferencia_x >= 0 and y-diferencia_x == y_act: #Calculamos diagonal negatica
				return True
		else: #Diagonal positiva	
			if y+diferencia_x < Cant_Reinas and y+diferencia_x == y_act: #Calculamos diagonal positiva
				return True
	return False

#--------------------------------->>>
#--------------------------------->>>

#--------------------------------->>>
#--------------------------------->>>

for reinas in [ 4 , 8 , 10 , 12 , 15 ,20 , 25 ,26,27]:

	tablero = Crea_Tabla(reinas,reinas) #9 filas y 9 columnas

	inicio = time.time()

	Lista_Reinas = Problema_de_las_8_Reinas(reinas,[],0) #Retorna lista con las posiciones de las reinas

	fin = time.time()

	print(reinas ,": " , fin-inicio)


if Lista_Reinas != None: #Verificasmo que exista la lista solucion
	Posicionar_Reinas(tablero,Lista_Reinas) #Posicionamos las reinas en el tablero
	Muestra_Tabla(tablero) #Mostramos tablero
else:
	print('No solucion') #No existe la lista de posibles posiciones de la reina

