import pygame
import os
import copy

from constants import *
from game import Game


class Display:

    def __init__(self, game=None):
        
        self.game = Game() if game == None else game
        self.cursor = Cursor()

        self.PANTALLA = pygame.display.set_mode((ANCHURA, ALTURA), pygame.RESIZABLE)  # ventana principal
        pygame.display.set_caption("Ajedrez. Creado por: Javier Abollado")  # titulo 
        
        self.MADERA_FONDO = pygame.transform.scale(pygame.image.load(os.path.join(MAIN_PATH, "fondo_madera.jpg")), DIMENSION_FONDO_MADERA)
        self.descargar_imagenes()
        self.descargar_botones()


    # PASAR LAS COORDENADAS DEL TABLERO DE 8x8 BLOQUES A LAS DIMENSIONES DEL GRAFICO Y VICEVERSA, PARA PODER MOVER
    # LAS FICHAS CORRECTAMENTE
    def posicion_del_tablero_al_grafico(self,x,y): 
        return x*TAMAÑO_CUADRADO + BORDE_ANCHURA, y*TAMAÑO_CUADRADO + BORDE_ALTURA

    def posicion_del_grafico_al_tablero(self,x,y):
        return int((x - BORDE_ANCHURA)/TAMAÑO_CUADRADO), int((y - BORDE_ALTURA)/TAMAÑO_CUADRADO)


    # CREAR UNA FUENTE DE TEXTO
    def crear_texto(self, tamaño, color, texto):
        fuente = pygame.font.SysFont("Arial", tamaño)
        return fuente.render(texto, 0, color)


    # DESCARGAS DE LAS IMAGENES Y LOS BOTONES DE TODAS LAS FICHAS, HACIENDO QUE VAYAN SIGUIENDO SU MOVIMIENTO
    def descargar_imagenes(self):

        self.IMAGENES = {}

        # cargamos por ultimo el tablero de ajedrez, punto rojo de selector de opciones, el exit y el play
        self.IMAGENES["tablero_marron"] = pygame.transform.scale(
            pygame.image.load(os.path.join(MAIN_PATH, "tablero_marron.jpg")), (ANCHURA - 2*BORDE_ANCHURA, ALTURA - 2*BORDE_ALTURA))
        self.IMAGENES["tablero_negro"] = pygame.transform.scale(
            pygame.image.load(os.path.join(MAIN_PATH, "tablero_gris.png")), (ANCHURA - 2*BORDE_ANCHURA, ALTURA - 2*BORDE_ALTURA))
        self.IMAGENES["exit"] = pygame.transform.scale(
            pygame.image.load(os.path.join(MAIN_PATH, "exit.png")), DIMENSION_EXIT)
        self.IMAGENES["puntero"] = pygame.transform.scale(
            pygame.image.load(os.path.join(MAIN_PATH, "puntero.png")), DIMENSION_FICHA)
        self.IMAGENES["fondo_boton"] = pygame.transform.scale(
            pygame.image.load(os.path.join(MAIN_PATH, "background_boton.png")), DIMENSION_CAMBIO_COLOR)
        
        def load_image(color, nombre):
            nombre_fichero = f"{self.game.colors[color]}_{self.game.names[nombre]}.png"
            self.IMAGENES[f"{self.game.colors[color]}_{self.game.names[nombre]}"] = pygame.transform.scale(
                pygame.image.load(os.path.join(MAIN_PATH, nombre_fichero)), DIMENSION_FICHA)

        for color in range(2):
            for ficha in range(6):
                load_image(color, ficha)

    def descargar_botones(self):

        self.boton_fondo = Boton(self.PANTALLA, COORDENADAS_CAMBIO_COLOR, self.IMAGENES["fondo_boton"])
        self.boton_exit = Boton(self.PANTALLA, COORDENADA_EXIT, self.IMAGENES["exit"])

        self.botones = {}
        for i in range(8):
            for j in range(8):
                color, nombre = self.game.board[i][j]
                imagen = self.IMAGENES[f"{self.game.colors[color]}_{self.game.names[nombre]}"] if not self.game.pos_empty((i,j)) else None
                posicion = self.posicion_del_tablero_al_grafico(i,j)
                self.botones[(i,j)] = Boton(self.PANTALLA, posicion, imagen)


    # CREAR PUNTEROS NEGROS EN CADA POSIBLE MOVIMIENTO DE LA FICHA SELECCIONADA (BOTONES) Y DIBUJARLOS EN LA VENTANA
    def punteros_de_posibilidades(self, posibles):
        punteros = {}
        for (i,j) in posibles:
            posicion = self.posicion_del_tablero_al_grafico(i,j)
            punteros[(i,j)] = Boton(self.PANTALLA, posicion, self.IMAGENES["puntero"])
        return punteros

    def move_chips(self, pos, target): 
        image = self.botones[pos].imagen
        self.botones[target].change_image(image)
        self.botones[pos].change_image(None)


    def reset_game(self):
        self.game.reset_game()
        self.descargar_botones()


    # DIBUJAR Y ACTUALIR EL TABLERO Y LAS RESPECTIVAS FICHAS (NO COMIDAS) TODO EL RATO EN LA PANTALLA SIEMPRE QUE 
    # NO HAY TERMINADO EL JUEGO
    def update(self):

        self.PANTALLA.fill(COLOR_FONDO)
        self.PANTALLA.blit(self.MADERA_FONDO, (0,0)) #(0, int(0.9*BORDE_ALTURA))
        self.PANTALLA.blit(self.IMAGENES[(f"tablero_{self.color_tablero}")],(BORDE_ANCHURA, BORDE_ALTURA))
        for nombre in self.botones: 
            self.botones[nombre].update()

        # si tenemos bordes añadimos una serie de información
        if BORDE_ANCHURA > 0 and BORDE_ALTURA > 0:

            # de quién es el turno?
            texto = f"Next move: {self.game.colors[self.game.player]}'s"
            turno = self.crear_texto(30, COLOR_ETIQUETAS, texto)
            self.PANTALLA.blit(turno, COORDENADA_TURNO)

            # cronómetro
            tiempo = self.tiempo - self.tiempo_init
            segundos, minutos = tiempo % 60, tiempo // 60
            if segundos >= 10 and minutos >= 10:
                texto = f"Tiempo - {minutos}:{segundos}"
            if segundos < 10 and minutos >= 10:
                texto = f"Tiempo - {minutos}:0{segundos}"
            if segundos >= 10 and minutos < 10:
                texto = f"Tiempo - 0{minutos}:{segundos}"
            if segundos < 10 and minutos < 10:
                texto = f"Tiempo - 0{minutos}:0{segundos}"
            contador = self.crear_texto(30, COLOR_ETIQUETAS, texto)
            self.PANTALLA.blit(contador, COORDENADA_CONTADOR)

            # Boton: cambiar color de tablero
            self.boton_fondo.update()
            texto = "Cambiar Fondo"
            cambiar_color = self.crear_texto(25, COLOR_BOTONES, texto)
            self.PANTALLA.blit(cambiar_color, (COORDENADAS_CAMBIO_COLOR[0] + 10, COORDENADAS_CAMBIO_COLOR[1] + 25))

            # mostrar número de movimientos
            texto = f"movimientos : {self.game.depth}"
            movimientos_texto = self.crear_texto(20, COLOR_ETIQUETAS, texto)
            self.PANTALLA.blit(movimientos_texto, (ANCHURA - int(0.8*BORDE_ANCHURA), ALTURA - int(0.6*BORDE_ALTURA)))

        for key in self.punteros: 
            self.punteros[key].update()
            
        # if not self.game.end_game:
        self.cursor.update()        
        pygame.display.update() 


    def play(self):

        # inicio
        pygame.init()
        reloj = pygame.time.Clock()

        # variables por defecto
        self.tiempo_init = pygame.time.get_ticks() // 1000
        self.punteros = {}
        self.color_tablero = "marron"
        self.run = True
        self.posicion_actual = (-1,-1)

        while self.run:

            reloj.tick(FPS)
            self.tiempo = pygame.time.get_ticks() // 1000

            # por si nos da algun fallo poder salir
            teclas_utilizadas = pygame.key.get_pressed()
            if teclas_utilizadas[pygame.K_SPACE]: 
                self.run = False

            # eventos 
            for event in pygame.event.get():

                if event.type == pygame.QUIT: 
                    self.run = False

                if self.game.end_game:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.cursor.colliderect(self.boton_exit): 
                            self.run = False
                            
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:

                        # cambiar de color el tablero
                        if self.cursor.colliderect(self.boton_fondo): 
                            self.color_tablero = "marron" if self.color_tablero == "negro" else "negro"

                        # si presionamos una ficha, nos salen las opciones para mover (siempre que sea su turno)
                        for i in range(8):
                            for j in range(8):
                                boton = self.botones[(i,j)]
                                if self.cursor.colliderect(boton):
                                    ficha = self.game.board[i][j]
                                    if ficha[0] == self.game.player:
                                        self.posicion_actual = (i,j)
                                        posibilidades = self.game.chips[ficha[1]].available_moves(self.game, (i,j))
                                        self.punteros = self.punteros_de_posibilidades(posibilidades)

                        # si los punteros estan activados...
                        for (i,j) in self.punteros:
                            if self.cursor.colliderect(self.punteros[(i,j)]): 
                                (ia,ja) = self.posicion_actual
                                pos = (ia,ja)
                                target = (i,j)
                                self.game.move(pos, target)
                                self.move_chips(pos, target)
                                self.punteros = {}
                                break

            if self.game.end_game:
                self.boton_exit.update()
                self.cursor.update()        
                pygame.display.update()
            else:
                self.update()

        print("Número de movimientos: ", self.game.depth)
        pygame.quit()


DEFAULT_RECT = pygame.transform.scale(pygame.image.load("imagenes/black_pawn.png"), DIMENSION_FICHA).get_rect()

class Cursor(pygame.Rect):

    def __init__(self):
        pygame.Rect.__init__(self, 0,0,1,1)

    def update(self):
        self.left, self.top = pygame.mouse.get_pos()

class Boton(pygame.sprite.Sprite):

    def __init__(self, pantalla, posicion, imagen=None):
        x, y = posicion[0], posicion[1]
        self.pantalla = pantalla
        self.imagen = imagen
        self.rect = imagen.get_rect() if imagen != None else copy.deepcopy(DEFAULT_RECT)
        self.rect.left, self.rect.top = x, y

    def change_image(self, imagen):
        self.imagen = imagen

    def update(self):
        if self.imagen != None:
            self.pantalla.blit(self.imagen, self.rect)


