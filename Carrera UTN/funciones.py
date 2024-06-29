import pygame
import json
import time
from constantes import *

def inicializar_pygame(ancho, alto):
    """Inicializa Pygame y configura la ventana del juego.

    Args:
        ancho (int): Ancho de la ventana.
        alto (int): Alto de la ventana.

    Returns:
        pygame.Surface: Superficie de la ventana del juego.
    """
    pygame.init()
    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Carrera UTN")
    return pantalla

def mostrar_imagen(pantalla, ruta_imagen, x, y, nuevo_ancho, nuevo_alto, colorkey=None):
    """Carga y muestra una imagen en la pantalla.

    Args:
        pantalla (pygame.Surface): Superficie en la que se mostrará la imagen.
        ruta_imagen (str): Ruta del archivo de imagen.
        x (int): Coordenada x donde se dibujará la imagen.
        y (int): Coordenada y donde se dibujará la imagen.
        nuevo_ancho (int): Nuevo ancho de la imagen.
        nuevo_alto (int): Nuevo alto de la imagen.
        colorkey (tuple, optional): Color transparente en la imagen. Default es None.
    """
    imagen = pygame.image.load(ruta_imagen).convert()
    if colorkey is not None:
        imagen.set_colorkey(colorkey)
    imagen_redimensionada = pygame.transform.scale(imagen, (nuevo_ancho, nuevo_alto))
    pantalla.blit(imagen_redimensionada, (x, y))

def mostrar_texto(pantalla, texto, x, y, color, fuente):
    """Muestra un texto en la pantalla.

    Args:
        pantalla (pygame.Surface): Superficie en la que se mostrará el texto.
        texto (str): Texto a mostrar.
        x (int): Coordenada x donde se dibujará el texto.
        y (int): Coordenada y donde se dibujará el texto.
        color (tuple): Color del texto.
        fuente (pygame.font.Font): Fuente del texto.
    """
    renderizado = fuente.render(texto, True, color)
    pantalla.blit(renderizado, (x, y))

def mostrar_pregunta_y_opciones(pantalla, pregunta, x, y, ancho, alto, color, fuente):
    """Muestra una pregunta y sus opciones en la pantalla.

    Args:
        pantalla (pygame.Surface): Superficie en la que se mostraran la pregunta y las opciones.
        pregunta (dict): Diccionario con la pregunta y las opciones.
        x (int): Coordenada x donde se dibujara la pregunta.
        y (int): Coordenada y donde se dibujara la pregunta.
        ancho (int): Ancho del area de la pregunta.
        alto (int): Alto del area de la pregunta.
        color (tuple): Color del area de la pregunta.
        fuente (pygame.font.Font): Fuente del texto.
    """

    rectangulo = pygame.Rect(281, 10, 365, alto)
    pygame.draw.rect(pantalla, GREEN3, rectangulo)

    
    lineas_pregunta = ajustar_texto(pregunta['pregunta'], fuente, ancho - 20)
    y_texto = y - 180
    for linea in lineas_pregunta:
        mostrar_texto(pantalla, linea, x + 40, y_texto, (0, 0, 0), fuente)
        y_texto += fuente.get_height() + 5

    
    opciones = ['a', 'b', 'c']
    x_opcion = x + 35  
    for opcion in opciones:
        
        mostrar_texto(pantalla, f"{pregunta[opcion]}", x_opcion, y - 35, (0, 0, 0), fuente)
        x_opcion += 150  

def ajustar_texto(texto, fuente, ancho_maximo):
    """Ajusta el texto para que se ajuste dentro de un ancho maximo.

    Args:
        texto (str): Texto a ajustar.
        fuente (pygame.font.Font): Fuente del texto.
        ancho_maximo (int): Ancho máximo para el texto.

    Returns:
        list: Lista de lineas ajustadas.
    """
    palabras = texto.split(' ')
    lineas = []
    linea_actual = ""

    for palabra in palabras:
        if fuente.size(linea_actual + palabra)[0] <= ancho_maximo:
            linea_actual += palabra + " "
        else:
            lineas.append(linea_actual)
            linea_actual = palabra + " "

    lineas.append(linea_actual)
    return lineas

def mostrar_tablero(pantalla, posiciones_casillas, colores_casillas, LLEGADA, casillas_especiales, fuente):
    """Muestra el tablero del juego en la pantalla.

    Args:
        pantalla (pygame.Surface): Superficie en la que se mostrara el tablero.
        posiciones_casillas (list): Lista de posiciones de las casillas.
        colores_casillas (list): Lista de colores de las casillas.
        LLEGADA (int): Índice de la casilla de llegada.
        casillas_especiales (dict): Diccionario de casillas especiales.
        fuente (pygame.font.Font): Fuente del texto.
    """
    for i, (x, y) in enumerate(posiciones_casillas):
        color = colores_casillas[i]
        pygame.draw.rect(pantalla, color, (x, y, 70, 55), border_radius=10)
        if i == LLEGADA:
            mostrar_texto(pantalla, "Llegada", x + 5, y + 10, BLACK, fuente)  
        if i in casillas_especiales:
            mostrar_texto(pantalla, casillas_especiales[i], x - 1, y + 10, (0, 0, 0), pygame.font.Font(None, 18))

def pedir_nombre(pantalla, fuente):
    """Pide al usuario que ingrese su nombre.

    Args:
        pantalla (pygame.Surface): Superficie en la que se mostrara el prompt.
        fuente (pygame.font.Font): Fuente del texto.

    Returns:
        str: Nombre ingresado por el usuario.
    """
    pantalla.fill((30, 144, 255))
    mostrar_texto(pantalla, "Ingrese su nombre:", 250, 200, (255, 255, 255), fuente)
    nombre = ""
    ingresando_nombre = True
    while ingresando_nombre:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return ""
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    ingresando_nombre = False
                elif event.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    nombre += event.unicode
        
        pantalla.fill((30, 144, 255))
        mostrar_texto(pantalla, "Ingrese su nombre:", 250, 200, (255, 255, 255), fuente)
        mostrar_texto(pantalla, nombre, 250, 250, (255, 255, 255), fuente)
        pygame.display.flip()

    return nombre

def guardar_puntaje(nombre, puntaje):
    """Guarda el puntaje del jugador en un archivo JSON.

    Args:
        nombre (str): Nombre del jugador.
        puntaje (int): Puntaje del jugador.
    """
    try:
        with open('puntajes.json', 'r') as archivo:
            puntajes = json.load(archivo)
    except FileNotFoundError:
        puntajes = []

    puntajes.append({"nombre": nombre, "puntaje": puntaje})
    puntajes = sorted(puntajes, key=lambda x: x['puntaje'], reverse=True)[:10]

    with open('puntajes.json', 'w') as archivo:
        json.dump(puntajes, archivo)

def mostrar_puntajes(pantalla, fuente):
    """Muestra los mejores puntajes en la pantalla.

    Args:
        pantalla (pygame.Surface): Superficie en la que se mostraran los puntajes.
        fuente (pygame.font.Font): Fuente del texto.
    """
    personaje = pygame.image.load('personaje.png')  

    pantalla.fill((30, 144, 255))  # Fondo azul

    
    pantalla.blit(personaje, (207, 267))  
    mostrar_imagen(pantalla, "carrera_utn.png", 25, 11, 250, 200)

    
    titulo = fuente.render("Mejores Puntajes", True, (255, 255, 255))
    rect_titulo = titulo.get_rect(center=(ANCHO_VENTANA // 2, 50))
    pantalla.blit(titulo, rect_titulo)

    
    try:
        with open('puntajes.json', 'r') as archivo:
            puntajes = json.load(archivo)
    except FileNotFoundError:
        puntajes = []

    y_pos = 100
    for i, puntaje in enumerate(puntajes):
        texto_puntaje = f"{i+1}. {puntaje['nombre']} - {puntaje['puntaje']}"
        mostrar_texto(pantalla, texto_puntaje, 300, y_pos, (255, 255, 255), fuente)
        y_pos += 30

    
    boton_salir = pygame.Rect(644, 495, 100, 50)  
    pygame.draw.rect(pantalla, (173, 216, 230), boton_salir, border_radius=10)
    texto_salir = fuente.render("Salir", True, (0, 0, 0))
    rect_texto_salir = texto_salir.get_rect(center=boton_salir.center)
    pantalla.blit(texto_salir, rect_texto_salir)

    pygame.display.flip()

    
    mostrando_puntajes = True
    while mostrando_puntajes:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if boton_salir.collidepoint(x, y):
                    mostrando_puntajes = False

    


def mostrar_interfaz(pantalla, tiempo_restante, puntaje, casillas, fuente, posiciones_casillas, colores_casillas, LLEGADA, casillas_especiales, personaje_imagen):
    """Muestra la interfaz del juego en la pantalla.

    Args:
        pantalla: La superficie de Pygame donde se muestra la interfaz.
        tiempo_restante: El tiempo restante para el jugador.
        puntaje: El puntaje actual del jugador.
        casillas: La cantidad de casillas avanzadas.
        fuente: La fuente utilizada para mostrar texto.
        posiciones_casillas: Lista de posiciones de las casillas en el tablero.
        colores_casillas: Lista de colores de las casillas en el tablero.
        LLEGADA: La casilla de llegada en el tablero.
        casillas_especiales: Diccionario de casillas especiales con acciones.
        personaje_imagen: Rectangulo que representa la imagen del personaje.
    Returns:
        Tuple: Botón de comenzar y botón de terminar.
    """
    pantalla.fill((30, 144, 255))  # Fondo azul
    mostrar_tablero(pantalla, posiciones_casillas, colores_casillas, LLEGADA, casillas_especiales, fuente)
    mostrar_imagen(pantalla, "personaje.png", personaje_imagen.x, personaje_imagen.y, personaje_imagen.width, personaje_imagen.height) 
    mostrar_imagen(pantalla, "carrera_utn.png", 25, 11, 250, 200)
    mostrar_imagen(pantalla, "utn.png", 10, 408, 100, 50)
    mostrar_imagen(pantalla, "flecha_vertical.png", 731, 366, 50, 100)
    mostrar_imagen(pantalla, "salida.png", 48, 330, 75, 50)
    mostrar_texto(pantalla, "Llegada", 18, 464, BLACK, fuente)
    mostrar_texto(pantalla, f"Tiempo: {tiempo_restante}", 650, 50, (0, 0, 0), fuente)
    mostrar_texto(pantalla, f"Puntaje: {puntaje}", 650, 100, (0, 0, 0), fuente)
    mostrar_texto(pantalla, f"Casillas: {casillas}", 650, 150, (0, 0, 0), fuente)
    boton_comenzar = pygame.Rect(177, 499, 200, 50)
    pygame.draw.rect(pantalla, (173, 216, 230), boton_comenzar, border_radius=10)
    mostrar_texto(pantalla, "Comenzar", 190, 517, (0, 0, 0), fuente)
    boton_terminar = pygame.Rect(451, 499, 200, 50)
    pygame.draw.rect(pantalla, (173, 216, 230), boton_terminar, border_radius=10)
    mostrar_texto(pantalla, "Terminar", 469, 517, (0, 0, 0), fuente)
    return boton_comenzar, boton_terminar

def pantalla_inicial(pantalla, tiempo_restante, puntaje, casillas, fuente, posiciones_casillas, colores_casillas, LLEGADA, casillas_especiales, personaje_imagen):
    """Muestra la pantalla inicial del juego.

    Args:
        pantalla: La superficie de Pygame donde se muestra la interfaz.
        tiempo_restante: El tiempo restante para el jugador.
        puntaje: El puntaje actual del jugador.
        casillas: La cantidad de casillas avanzadas.
        fuente: La fuente utilizada para mostrar texto.
        posiciones_casillas: Lista de posiciones de las casillas en el tablero.
        colores_casillas: Lista de colores de las casillas en el tablero.
        LLEGADA: La casilla de llegada en el tablero.
        casillas_especiales: Diccionario de casillas especiales con acciones.
        personaje_imagen: Rectangulo que representa la imagen del personaje.
    """
    mostrar_interfaz(pantalla, tiempo_restante, puntaje, casillas, fuente, posiciones_casillas, colores_casillas, LLEGADA, casillas_especiales, personaje_imagen)
    pygame.display.flip()

def mover_personaje(casillas, posiciones_casillas, personaje_imagen):
    """Mueve el personaje a una nueva posición basada en las casillas avanzadas.

    Args:
        casillas: La cantidad de casillas avanzadas.
        posiciones_casillas: Lista de posiciones de las casillas en el tablero.
        personaje_imagen: Rectángulo que representa la imagen del personaje.
    """
    if casillas < len(posiciones_casillas):
        personaje_imagen.x, personaje_imagen.y = posiciones_casillas[casillas]

def reiniciar_tiempo():
    """
    Reinicia los tiempos de inicio y última acción al tiempo actual.

    Returns:
        tuple: Simplemente devuelve el tiempo actual 
    """
    return time.time(), time.time()

def avanzar_pregunta(pregunta_actual, lista):
    """
    Avanza a la siguiente pregunta y reinicia los tiempos.

    Args:
        pregunta_actual (int): El índice de la pregunta actual en la lista.
        lista (list): Lista de preguntas del juego.

    Returns:
        tuple: Nuevo indice de pregunta, tiempo actual dos veces.
    """
    pregunta_actual += 1
    if pregunta_actual >= len(lista):
        pregunta_actual = 0  
    return pregunta_actual, *reiniciar_tiempo()


def juego(pantalla, fuente, fuente_pregunta, lista, LLEGADA, posiciones_casillas, colores_casillas, casillas_especiales):
    """Ejecuta el bucle principal del juego.

    Args:
        pantalla: La superficie de Pygame donde se muestra la interfaz.
        fuente: La fuente utilizada para mostrar texto.
        fuente_pregunta: La fuente utilizada para mostrar preguntas.
        lista: Lista de preguntas del juego.
        LLEGADA: La casilla de llegada en el tablero.
        posiciones_casillas: Lista de posiciones de las casillas en el tablero.
        colores_casillas: Lista de colores de las casillas en el tablero.
        casillas_especiales: Diccionario de casillas especiales con acciones.
    """
    casillas = 0
    puntaje = 0
    pregunta_actual = 0
    tiempo_restante = 5
    nombre_jugador = ""
    juego_iniciado = False
    corriendo = True
    tiempo_inicio, tiempo_ultima_accion = reiniciar_tiempo()

    
    personaje_imagen = pygame.Rect(72, 223, 40, 100)  

    while corriendo:
        boton_comenzar, boton_terminar = mostrar_interfaz(pantalla, tiempo_restante, puntaje, casillas, fuente, posiciones_casillas, colores_casillas, LLEGADA, casillas_especiales, personaje_imagen)
        tiempo_actual = time.time()
        
        if juego_iniciado:
            
            tiempo_transcurrido = int(tiempo_actual - tiempo_inicio)
            tiempo_restante = 5 - tiempo_transcurrido
            
            if tiempo_restante <= 0:
                tiempo_restante = 0

            
            if pregunta_actual < len(lista):
                pregunta = lista[pregunta_actual]
                mostrar_pregunta_y_opciones(pantalla, pregunta, 250, 200, 300, 200, (34, 139, 34), fuente_pregunta)
            
            
            if casillas >= LLEGADA:
                juego_iniciado = False
                nombre_jugador = pedir_nombre(pantalla, fuente)
                guardar_puntaje(nombre_jugador, puntaje)
                mostrar_puntajes(pantalla, fuente)
                corriendo = False

            
            mover_personaje(casillas, posiciones_casillas, personaje_imagen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                print(f"Coordenadas del clic: ({x}, {y})")
                if not juego_iniciado:
                    if boton_comenzar.collidepoint(x, y):
                        juego_iniciado = True
                        tiempo_inicio, tiempo_ultima_accion = reiniciar_tiempo()
                if juego_iniciado:
                    if boton_terminar.collidepoint(x, y):
                        juego_iniciado = False
                        nombre_jugador = pedir_nombre(pantalla, fuente)
                        guardar_puntaje(nombre_jugador, puntaje)
                        mostrar_puntajes(pantalla, fuente)
                        corriendo = False
                    else:
                        if 290 < x < 370 and 150 < y < 199:
                            respuesta = 'a'
                        elif 390 < x < 490 and 150 < y < 199:
                            respuesta = 'b'
                        elif 510 < x < 610 and 150 < y < 199:
                            respuesta = 'c'
                        else:
                            respuesta = None

                        if respuesta and pregunta_actual < len(lista):
                            pregunta = lista[pregunta_actual]
                            if respuesta == pregunta['correcta']:
                                casillas += 2
                                puntaje += 10
                                if casillas in casillas_especiales:
                                    if casillas_especiales[casillas] == "Avanza 1":
                                        casillas += 1
                                    elif casillas_especiales[casillas] == "Retrocede 1":
                                        casillas -= 1
                                pregunta_actual, tiempo_inicio, tiempo_ultima_accion = avanzar_pregunta(pregunta_actual, lista)
                            else:
                                casillas = max(0, casillas - 1)
                                pregunta_actual, tiempo_inicio, tiempo_ultima_accion = avanzar_pregunta(pregunta_actual, lista)

        
        tiempo_inactivo = int(tiempo_actual - tiempo_ultima_accion)
        if tiempo_inactivo >= 5 and juego_iniciado:
            pregunta_actual, tiempo_inicio, tiempo_ultima_accion = avanzar_pregunta(pregunta_actual, lista)
        
        pygame.display.flip()

        













