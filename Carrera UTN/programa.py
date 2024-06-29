import pygame
from datos import lista
from constantes import *
from funciones import *
from os import system
system("cls")

# Configuración de la pantalla
ANCHO, ALTO = 800, 600
pantalla = inicializar_pygame(ANCHO, ALTO)

# Fuentes
fuente = pygame.font.Font(None, 36)
fuente_pregunta = pygame.font.Font(None, 35)

# Posiciones de las casillas en el tablero
posiciones_casillas = [
    (128, 320), (203, 320), (278, 320), (353, 320), (428, 320), (503, 320), (578, 320), (653, 320),
    (653, 420), (578, 420), (503, 420), (428, 420), (353, 420), (278, 420), (203, 420), (128, 420)
]

# Colores de las casillas
colores_casillas = [
    (ORANGE), (GREEN), (YELLOW1), (CYAN2), (RED1),
    (VIOLET), (YELLOW2), (GREEN), (GREEN), (YELLOW2), (VIOLET), (RED1), (CYAN2),
    (YELLOW1), (GREEN), (ORANGE)
]

# Casillas especiales
casillas_especiales = {
    5: "Avanza 1",
    12: "Retrocede 1"
}

# Configuración del juego
LLEGADA = 17

# Iniciar el juego
personaje_rect = pygame.Rect(72, 223, 40, 100)  # Define la posición inicial del personaje
pantalla_inicial(pantalla, 5, 0, 0, fuente, posiciones_casillas, colores_casillas, LLEGADA, casillas_especiales, personaje_rect)
juego(pantalla, fuente, fuente_pregunta, lista, LLEGADA, posiciones_casillas, colores_casillas, casillas_especiales)













