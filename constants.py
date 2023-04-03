# pantalla
BORDE_ANCHURA = 200 # 450
BORDE_ALTURA = 50   # 80
TAMAÑO_CUADRADO = 80
ANCHURA = 8*TAMAÑO_CUADRADO + 2*BORDE_ANCHURA
ALTURA = 8*TAMAÑO_CUADRADO + 2*BORDE_ALTURA
FPS = 5 # frames per second
MAIN_PATH = "imagenes"

# botones
DIMENSION_EXIT = (300, 100)
COORDENADA_EXIT = (int(ANCHURA/2) - int(DIMENSION_EXIT[0]/2), int(ALTURA/2) - int(DIMENSION_EXIT[1]/2)) 
DIMENSION_CAMBIO_COLOR = (160, TAMAÑO_CUADRADO)
COORDENADAS_CAMBIO_COLOR = (ANCHURA - int(0.9*BORDE_ANCHURA), BORDE_ALTURA + 10)

# etiquetas
COORDENADA_CONTADOR = (BORDE_ANCHURA + 3*TAMAÑO_CUADRADO, ALTURA - BORDE_ALTURA + 10)
COORDENADA_TURNO = (BORDE_ANCHURA + int(2.5*TAMAÑO_CUADRADO), 10)

# fondo
DIMENSION_FONDO_MADERA = (ANCHURA, ALTURA)

# colores en código RGB
BLANCO = (255, 255, 255) 
GRIS = (130, 130, 130)
NEGRO = (0,0,0)
COLOR_FONDO = GRIS
COLOR_ETIQUETAS = BLANCO
COLOR_BOTONES = BLANCO

# fichas
COLOR_FICHA = ["blanco", "negro"]
DIMENSION_FICHA = (75, 75)
NOMBRES_OUTPUT = ["peon", "caballo", "torre", "alfil", "reina", "rey"]

# training codes 
DIR_CODES = {"N":0,"NE":1,"E":2,"SE":3,"S":4,"SW":5,"W":6,"NW":7}
DIR_CODES_INV = {0:"N",1:"NE",2:"E",3:"SE",4:"S",5:"SW",6:"W",7:"NW"}
CHIP_CODES = {"bishop":1, "knight":2, "rook":3}
CHIP_CODES_INV = {1:"bishop", 2:"knight", 3:"rook"}