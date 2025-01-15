import pygame, sys
from pygame.locals import *

pygame.init()

PANTALLAXDLOL = pygame.display.set_mode((500,600))
pygame.display.set_caption('Hi-Lo (Sube o Baja)')

# colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (110, 110, 110)
VERDE = (0, 255, 0)
VERDE_OSCURO = (0, 120, 0)
ROJO = (255, 0, 0)
ROJO_OSCURO = (120, 0, 0)

PANTALLAXDLOL.fill(BLANCO)

# bucle para que no cierre la ventana
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()