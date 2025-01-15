import pygame
import random

pygame.init()

# COLORES
GRIS = (110, 110, 110)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
VERDE2 = (0, 120, 0)
ROJO = (255, 0, 0)
ROJO2 = (120, 0, 0)

# TAMAÑO DE LA VENTANA
ANCHO = 1280
ALTO = 720

# Pantalla y fondo
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pantalla.fill(GRIS)

# Titulo de Ventana
pygame.display.set_caption("Hi-Lo (Sube o Baja)")

# Cargando Imagen de Icono
icon = pygame.image.load('cartas/icono.png')

# Icono del Juego
pygame.display.set_icon(icon)

# Fuentes
fuente_grande = pygame.font.Font(None, 50)
fuente_pequena = pygame.font.Font(None, 32)

# Botones / rectangulos
boton_alto = fuente_grande.render("SUBE", True, BLANCO)
boton_alto_rect = boton_alto.get_rect(center=(ANCHO // 3, ALTO - 150))

boton_bajo = fuente_grande.render("BAJA", True, BLANCO)
boton_bajo_rect = boton_bajo.get_rect(center=(2 * ANCHO // 3, ALTO - 150))

# CLASE CARTA
class Carta:
    def __init__(self, palo, valor):
        self.palo = palo
        self.valor = valor

# DEFINICIÓN DE PALOS Y VALORES
palos = ["Espadas", "Corazones", "Treboles", "Diamantes"]
valores = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

# VALORES NUMÉRICOS DE LAS CARTAS
valores_cartas = {
    "A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
    "10": 10, "J": 11, "Q": 12, "K": 13
}

# CREACION DEL MAZO
mazo = []
for palo in palos:
    for valor in valores:
        mazo.append(Carta(palo, valor))

# CONFIGURACION DE IMAGENES DE CARTAS
carta_anterior = pygame.image.load(r'./cartas/cover.png')  # Imagen para la carta cubierta
carta_anterior = pygame.transform.scale(carta_anterior, (150, 240))  # Escalado de la carta

# Seleccionar una carta inicial aleatoria del mazo
carta_actual = random.choice(mazo)  # Seleccionar carta al azar

# Cargar imagen de la carta actual
carta_actual_img = pygame.image.load(r'./cartas/' + carta_actual.valor + carta_actual.palo[0] + '.png')

carta_actual_img = pygame.transform.scale(carta_actual_img, (150, 240))  # Escalado de la cartas

# Remover la carta del mazo:
mazo.remove(carta_actual)

# Cargando Cover de Carta
carta_siguiente = pygame.image.load(r'./cartas/cover.png')

# Escalando la imagen de la carta a cargar:
carta_siguiente = pygame.transform.scale(carta_siguiente, (150, 240))

# VARIABLES DE JUEGO
intentos = 3
puntaje = 0
eleccion = -1  # 1: sube, 0: baja
terminado = False

# Bucle principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            quit()

        if not terminado and evento.type == pygame.MOUSEBUTTONDOWN:
            # Verificar si se hace clic en el botón de subir
            if boton_alto_rect.collidepoint(evento.pos):
                eleccion = 1  # Elegir subir
            # Verificar si se hace clic en el botón de bajar
            elif boton_bajo_rect.collidepoint(evento.pos):
                eleccion = 0  # Elegir bajar

    # Lógica del juego
    if eleccion != -1:  # Si se ha hecho una elección
        # Carta previa
        carta_previa = carta_actual
        carta_anterior = pygame.image.load(r'./cartas/' + carta_previa.valor + carta_previa.palo[0] + '.png')
        carta_anterior = pygame.transform.scale(carta_anterior, (150, 240))

        # Nueva carta
        carta_actual = random.choice(mazo)
        mazo.remove(carta_actual)

        carta_actual_img = pygame.image.load(r'./cartas/' + carta_actual.valor + carta_actual.palo[0] + '.png')
        carta_actual_img = pygame.transform.scale(carta_actual_img, (150, 240))

        # Verificar resultado
        if valores_cartas[carta_actual.valor] > valores_cartas[carta_previa.valor]:
            resultado = 1  # La carta es más alta
        elif valores_cartas[carta_actual.valor] < valores_cartas[carta_previa.valor]:
            resultado = 0  # La carta es más baja
        else:
            resultado = -1  # Empate

        # Comprobar si la eleccion fue correcta
        if resultado == -1:
            pass  # Si es empate, no hacer nada
        elif resultado == eleccion:
            puntaje += 1  # Sumar puntaje
        else:
            intentos -= 1  # Restar intentos

        # Terminar el juego si se acaban los intentos
        if intentos == 0:
            terminado = True

        # Restablecer la elección
        eleccion = -1

    # Limpiar anterior intento/punto
    pantalla.fill(GRIS)

    # Dibujar los botones
    if boton_alto_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(pantalla, VERDE2, boton_alto_rect.inflate(30, 30))
    else:
        pygame.draw.rect(pantalla, VERDE, boton_alto_rect.inflate(30, 30))

    if boton_bajo_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(pantalla, ROJO2, boton_bajo_rect.inflate(30, 30))
    else:
        pygame.draw.rect(pantalla, ROJO, boton_bajo_rect.inflate(30, 30))

    # Mostrar los botones
    pantalla.blit(boton_alto, boton_alto_rect)
    pantalla.blit(boton_bajo, boton_bajo_rect)

    # Mostrar el puntaje y los intentos
    texto_puntaje = fuente_pequena.render(f"Puntaje = {puntaje}", True, BLANCO)
    pantalla.blit(texto_puntaje, (10, 10))

    texto_intentos = fuente_pequena.render(f"Intentos = {intentos}", True, BLANCO)
    pantalla.blit(texto_intentos, (10, 50))

    # Mostrar las cartas
    pantalla.blit(carta_anterior, (ANCHO // 2 - 160, ALTO // 2 - 120))
    pantalla.blit(carta_actual_img, (ANCHO // 2 - 40, ALTO // 2 - 120))
    pantalla.blit(carta_siguiente, (ANCHO // 2 + 80, ALTO // 2 - 120))

    # Si el juego ha terminado, mostrar mensaje final
    if terminado:
        texto_final = fuente_grande.render(f"Juego Terminado! Puntaje Final: {puntaje}", True, BLANCO)
        pantalla.blit(texto_final, (ANCHO // 2 - texto_final.get_width() // 2, ALTO // 2 - 180))  # Posicion del texto

    # Actualizar la pantalla
    pygame.display.update()
