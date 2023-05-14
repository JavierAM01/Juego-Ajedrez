# Ajedrez

<div style="text-align:center;">
  <image src="https://github.com/JavierAM01/Machine-Learnig-in-Games/blob/main/images/ajedrez.gif" style="width:100%; height:12cm;">
</div>

Para crear el tablero de ajedrez primero creamos clases para las fichas del juego. Cada una de ellas tiene una función **available_moves()** que 
nos devuelve las posiciones a las que nos podemos mover desde la posición actual, teniendo en cuenta las demás fichas del tablero. Por último creamos
la clase **Game** en la que guardará toda información del juego. Guardamos 3 diccionarios principales:

```python
self.colors  = {0:"white", 1:"black"}
self.names   = {0:"pawn", 1:"bishop", 2:"knight", 3:"rook", 4:"queen", 5:"king"}
self.chips   = {0:Pawn(), 1:Bishop(), 2:Knight(), 3:Rook(), 4:Queen(), 5:King()}
```

para el manejo de las fichas. El tablero se representará como un conjunto de tuplas de tipo (int, int), donde el primer elemento representará el color 
y el segundo el tipo de ficha. Por ejemplo (0,2) representa un caballo blanco (se descodifica através de los diccionarios mencionados anteriormente. 
Por último, una casilla vacía se representa como (-1,-1).
  
```python
self.empty   = (-1,-1)
self.board = [[self.empty for _ in range(8)] for _ in range(8)]
# aquí inicializamos las posiciones de la casillas
```

### Distribución de archivos
  
 - constants.py: constantes globales del juego.
 - game.py: objetos del juego, como las fichas y el Game.
 - display.py: interfaz en pygame para la visualización. 
 - main.py: programa principal para ejecutar el juego. 
