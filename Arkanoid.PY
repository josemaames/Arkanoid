import pygame
import random

# Inicializa pygame
pygame.init()

# Dimensiones de la ventana
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Breakout Game")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)

# Dimensiones de la barra y de la pelota
ANCHO_BARRA = 100
ALTO_BARRA = 10
ANCHO_PELOTA = 10
ALTO_PELOTA = 10

# Posición inicial de la barra y la pelota
barra_x = ANCHO // 2 - ANCHO_BARRA // 2
barra_y = ALTO - 30
pelota_x = ANCHO // 2 - ANCHO_PELOTA // 2
pelota_y = ALTO // 2 - ALTO_PELOTA // 2

# Velocidades de la pelota
pelota_dx = 4
pelota_dy = 4

# Lista de bloques
bloques = []
ANCHO_BLOQUE = 60
ALTO_BLOQUE = 20
for i in range(7):
    for j in range(5):
        bloque = pygame.Rect(i * (ANCHO_BLOQUE + 10) + 35, j * (ALTO_BLOQUE + 10) + 50, ANCHO_BLOQUE, ALTO_BLOQUE)
        bloques.append(bloque)

# Control de FPS
reloj = pygame.time.Clock()

# Bucle principal del juego
jugando = True
while jugando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False

    # Movimiento de la barra
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and barra_x > 0:
        barra_x -= 7
    if teclas[pygame.K_RIGHT] and barra_x < ANCHO - ANCHO_BARRA:
        barra_x += 7

    # Movimiento de la pelota
    pelota_x += pelota_dx
    pelota_y += pelota_dy

    # Rebote de la pelota en los bordes
    if pelota_x <= 0 or pelota_x >= ANCHO - ANCHO_PELOTA:
        pelota_dx = -pelota_dx
    if pelota_y <= 0:
        pelota_dy = -pelota_dy

    # Rebote de la pelota en la barra
    if pelota_y + ALTO_PELOTA >= barra_y and barra_x <= pelota_x <= barra_x + ANCHO_BARRA:
        pelota_dy = -pelota_dy

    # Rebote de la pelota en los bloques
    for bloque in bloques[:]:
        if bloque.collidepoint(pelota_x, pelota_y):
            bloques.remove(bloque)
            pelota_dy = -pelota_dy
            break

    # Si la pelota cae
    if pelota_y > ALTO:
        jugando = False

    # Dibujar en la pantalla
    ventana.fill(NEGRO)
    pygame.draw.rect(ventana, BLANCO, (barra_x, barra_y, ANCHO_BARRA, ALTO_BARRA))
    pygame.draw.ellipse(ventana, ROJO, (pelota_x, pelota_y, ANCHO_PELOTA, ALTO_PELOTA))

    for bloque in bloques:
        pygame.draw.rect(ventana, AZUL, bloque)

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
