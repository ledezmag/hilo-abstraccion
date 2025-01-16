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
fondo1 = pygame.image.load('fondo/fondom.jpg')
fondo1 = pygame.transform.scale(fondo1, (ANCHO, ALTO))
fondo2 = pygame.image.load('fondo/fondo2.png')
fondo2 = pygame.transform.scale(fondo2, (1430, 1200))

# Título de Ventana
pygame.display.set_caption("Hi-Lo (Sube o Baja)")

# Icono
icon = pygame.image.load('cartas/icono.png')
pygame.display.set_icon(icon)

# Fuentes
fuente_grande = pygame.font.Font(None, 50)
fuente_pequena = pygame.font.Font(None, 32)

# Botones
boton_alto = fuente_grande.render("SUBE", True, BLANCO)
boton_alto_rect = boton_alto.get_rect(center=(ANCHO // 3, ALTO - 150))

boton_bajo = fuente_grande.render("BAJA", True, BLANCO)
boton_bajo_rect = boton_bajo.get_rect(center=(2 * ANCHO // 3, ALTO - 150))


class Jugador:
    def __init__(self, nombre, saldo):
        self.nombre = nombre
        self.saldo = saldo

    def calcular_recompensa(self, cartas_restantes):
        if 52 >= cartas_restantes >= 41:
            return 3
        elif 40 >= cartas_restantes >= 31:
            return 3.5
        elif 30 >= cartas_restantes >= 21:
            return 4
        elif 20 >= cartas_restantes >= 11:
            return 4.5
        elif 10 >= cartas_restantes >= 6:
            return 5
        elif 5 >= cartas_restantes >= 4:
            return 6
        elif 3 >= cartas_restantes >= 2:
            return 7
        elif cartas_restantes == 1:
            return 15
        else:
            return 0

    def actualizar_saldo(self, cantidad):
        self.saldo += cantidad
        if self.saldo < 0:
            self.saldo = 0  # Evitar saldo negativo

    def puede_apostar(self, cantidad):
        return self.saldo >= cantidad


class Carta:
    def __init__(self, palo, valor):
        self.palo = palo
        self.valor = valor


palos = ["Espadas", "Corazones", "Treboles", "Diamantes"]
valores = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

valores_cartas = {
    "A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
    "10": 10, "J": 11, "Q": 12, "K": 13
}

mazo = [Carta(palo, valor) for palo in palos for valor in valores]

carta_anterior = pygame.image.load(r'./cartas/cover.png')
carta_anterior = pygame.transform.scale(carta_anterior, (150, 240))

jugador = Jugador('Jugador', 1000)

carta_actual = random.choice(mazo)
mazo.remove(carta_actual)
carta_actual_img = pygame.image.load(r'./cartas/' + carta_actual.valor + carta_actual.palo[0] + '.png')
carta_actual_img = pygame.transform.scale(carta_actual_img, (150, 240))

intentos = 3
puntaje = 0
eleccion = -1
terminado = False

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            quit()

        if not terminado and evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_alto_rect.collidepoint(evento.pos):
                eleccion = 1
            elif boton_bajo_rect.collidepoint(evento.pos):
                eleccion = 0

    if eleccion != -1 and not terminado:
        if not jugador.puede_apostar(10):
            terminado = True
            continue

        jugador.actualizar_saldo(-10)
        carta_previa = carta_actual
        carta_anterior = pygame.image.load(r'./cartas/' + carta_previa.valor + carta_previa.palo[0] + '.png')
        carta_anterior = pygame.transform.scale(carta_anterior, (150, 240))

        carta_actual = random.choice(mazo)
        mazo.remove(carta_actual)
        carta_actual_img = pygame.image.load(r'./cartas/' + carta_actual.valor + carta_actual.palo[0] + '.png')
        carta_actual_img = pygame.transform.scale(carta_actual_img, (150, 240))

        resultado = 1 if valores_cartas[carta_actual.valor] > valores_cartas[carta_previa.valor] else 0

        if resultado == eleccion:
            recompensa = jugador.calcular_recompensa(len(mazo))
            jugador.actualizar_saldo(10 * recompensa)
            puntaje += 1
        else:
            intentos -= 1

        if intentos == 0:
            terminado = True

        eleccion = -1

    pantalla.blit(fondo1, (0, 0))
    pantalla.blit(fondo2, (-75, -400))

    if boton_alto_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(pantalla, VERDE2, boton_alto_rect.inflate(30, 30))
    else:
        pygame.draw.rect(pantalla, VERDE, boton_alto_rect.inflate(30, 30))

    if boton_bajo_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(pantalla, ROJO2, boton_bajo_rect.inflate(30, 30))
    else:
        pygame.draw.rect(pantalla, ROJO, boton_bajo_rect.inflate(30, 30))

    pantalla.blit(boton_alto, boton_alto_rect)
    pantalla.blit(boton_bajo, boton_bajo_rect)

    texto_puntaje = fuente_pequena.render(f"Puntaje = {puntaje}", True, BLANCO)
    pantalla.blit(texto_puntaje, (10, 10))

    texto_intentos = fuente_pequena.render(f"Intentos = {intentos}", True, BLANCO)
    pantalla.blit(texto_intentos, (10, 50))

    texto_saldo = fuente_pequena.render(f"Saldo = {jugador.saldo}", True, BLANCO)
    pantalla.blit(texto_saldo, (10, 90))

    pantalla.blit(carta_anterior, (ANCHO // 2 - 160, ALTO // 2 - 120))
    pantalla.blit(carta_actual_img, (ANCHO // 2 - 40, ALTO // 2 - 120))

    if terminado:
        texto_final = fuente_grande.render(f"Juego Terminado! Puntaje Final: {puntaje}", True, BLANCO)
        pantalla.blit(texto_final, (ANCHO // 2 - texto_final.get_width() // 2, ALTO // 2 - 180))

    pygame.display.update()
