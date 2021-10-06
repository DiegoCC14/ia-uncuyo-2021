import networkx as nx
import time
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

class Tablero(MatrizNew):
    def __init__(self,tamanio_tablero):
        MatrizNew.__init__(self,tamanio_tablero,tamanio_tablero)
        self.tablero = self.matriz
        self.size = tamanio_tablero
        self.casillas_sucias = []

    def ingresar_reina( self , pos_reina ):
        self.ingresa_objeto_tablero( pos_reina ,'R')

    def get_casilla(self,posicion):
        return self.tablero[posicion[0]][posicion[1]]

    def ingresa_objeto_tablero( self , posicion ,simbolo):
        simbolo = '['+simbolo+']'
        self.tablero[ posicion[0] ][ posicion[1] ] = simbolo
    
    def borrar_casilla_tablero( self , posicion ):
        self.tablero[posicion[0]][posicion[1]] = '[ ]'

class agente():
    def __init__( self ):
        self.pos_reinas = []

    def pos_disponibles( self , columna_actual , tablero ):
        #para cada pos indica cuantas posiciones posibles tiene
        pos_validas = []
        for x in range( tablero.size ):
            if tablero.get_casilla( (x,columna_actual) ) == "[ ]":
                pos_validas.append( (x,columna_actual) )
        return pos_validas

    def rellena_diagonales_filas_posibles( self , posicion , tablero ):
        #Dada una posicion esta rellena sus diagonales filas desde la posicion en adelante siempre que esten vacias
        pos_marcadas = []
        for x in range( 1 , tablero.size-posicion[1] ): #Diagonal positiva , negativa y fila 
            
            if tablero.get_casilla( (posicion[0],posicion[1]+x) ) == "[ ]":
                tablero.ingresa_objeto_tablero( (posicion[0],posicion[1]+x) , "X")
                pos_marcadas.append( (posicion[0],posicion[1]+x) )
            
            if posicion[0]+x < tablero.size and posicion[1]+x < tablero.size and tablero.get_casilla( (posicion[0]+x,posicion[1]+x) ) == "[ ]":
                tablero.ingresa_objeto_tablero( (posicion[0]+x,posicion[1]+x) , "X")
                pos_marcadas.append( (posicion[0]+x,posicion[1]+x) )

            if posicion[0]-x > -1 and posicion[1]+x < tablero.size and tablero.get_casilla( (posicion[0]-x,posicion[1]+x) ) == "[ ]" :
                tablero.ingresa_objeto_tablero( (posicion[0]-x,posicion[1]+x) , "X")
                pos_marcadas.append( (posicion[0]-x,posicion[1]+x) )

        return pos_marcadas
    
    def borras_diagonales_marcadas( self , pos_marcadas ):
        for pos in pos_marcadas:
            tablero.ingresa_objeto_tablero( pos , ' ')

    def Chequeo_adelante_N_Reinas( self , pos_actual , posiciones_validas , tablero ):

        for pos_valida in posiciones_validas:
            
            tablero.ingresar_reina( pos_valida )

            pos_marcadas = self.rellena_diagonales_filas_posibles( pos_valida , tablero )
            if pos_actual+1 < tablero.size:
                
                for x in range( pos_actual+1 , tablero.size ): #Verificando que las demas reinas tienen casillas posibles
                    if len( self.pos_disponibles( x , tablero ) ) == 0:
                        
                        self.borras_diagonales_marcadas( pos_marcadas ) #Borramos las posiciones marcadas incluyendo la reina
                        tablero.borrar_casilla_tablero( pos_valida )
                        
                        return False #Las reina no tiene posiciones posibles

                posiciones_validas = self.pos_disponibles( pos_actual+1 , tablero )
                
                respuesta = self.Chequeo_adelante_N_Reinas( pos_actual+1 , posiciones_validas , tablero )
                
                if respuesta == True:
                    return True
                else:
                    self.borras_diagonales_marcadas( pos_marcadas ) #Borramos las posiciones marcadas incluyendo la reina
                    tablero.borrar_casilla_tablero( pos_valida )
            else:
                print("Tablero Resuelto --->>>")
                #tablero.mostrarMatriz()
                return True


#--------------->>>>>>>>>>
#Configuracion Inicial:
tam_tablero = 4
#--------------->>>>>>>>>>

tiempo_adelante = []
for tam_tablero in [ 4 , 8 , 10 , 12 , 15 ,20 , 25 ,26,27]:
    
    tablero = Tablero( tam_tablero )
    ag = agente()

    pos_validas_comienzo = ag.pos_disponibles(0,tablero)
    
    inicio = time.time()
    ag.Chequeo_adelante_N_Reinas( 0 , pos_validas_comienzo , tablero )
    fin = time.time()

    print(tam_tablero ,": " , fin-inicio)
    tiempo_adelante.append( fin-inicio )
    





tiempo_backtraquing = [ 2.2649765014648438e-05 , 0.0006353855133056641 , 0.0007965564727783203 , 0.0031070709228515625 , 0.02448558807373047,5.265101432800293,1.8251631259918213,16.491975784301758,19.753431797027588]
plt.figure(figsize=(10,20))
plt.scatter( [ 4 , 8 , 10 , 12 , 15 ,20 , 25 ,26,27] , tiempo_adelante , label='chequeo hacia adelante')
plt.scatter( [ 4 , 8 , 10 , 12 , 15 ,20 , 25 ,26,27] , tiempo_backtraquing , label='backtraking')
plt.legend()
plt.xlabel("Tamanio tablero")
plt.ylabel("tiempo")
plt.show()