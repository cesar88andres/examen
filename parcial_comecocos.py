import pygame
import random
import sys
import tkinter as tk
from tkinter import messagebox

# Inicializar pygame
pygame.init()

# Definir constantes
MAPA_ANCHO = 20
MAPA_ALTO = 9
ANCHO, ALTO = 1200, 800
TAMANO_CELDA = min(ANCHO // MAPA_ANCHO, ALTO // MAPA_ALTO)

pantalla = pygame.display.set_mode((MAPA_ANCHO * TAMANO_CELDA, MAPA_ALTO * TAMANO_CELDA), pygame.RESIZABLE)
pygame.display.set_caption("Comecocos")

# Definir colores
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
ROJO = (255, 0, 0)  # Fantasmas

# Mapa del juego
mapa = [
    "####################",
    "#........#.........#",
    "#.###.##.#.#####.#.#",
    "#...#....#.....#...#",
    "###.#.######.#.###.#",
    "#....#...#...#.....#",
    "#.######.#.#####.#.#",
    "#.................#",
    "####################"
]

# Variables del juego
pac_x, pac_y = 1, 1
fan_x, fan_y = 10, 5
fan2_x, fan2_y = 15, 3  # Nuevo enemigo
puntos = 0

# Control continuo del movimiento del Pac-Man
direccion_pacman = (0, 0)  # Movimiento manual como antes

# Función para dibujar el mapa

def dibujar_mapa():
    pantalla.fill(NEGRO)
    for y, fila in enumerate(mapa):
        for x, celda in enumerate(fila):
            if celda == "#":
                pygame.draw.rect(pantalla, AZUL, (x * TAMANO_CELDA, y * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))
            elif celda == ".":
                pygame.draw.circle(pantalla, BLANCO, (x * TAMANO_CELDA + TAMANO_CELDA // 2, y * TAMANO_CELDA + TAMANO_CELDA // 2), 5)
    pygame.draw.circle(pantalla, AMARILLO, (pac_x * TAMANO_CELDA + TAMANO_CELDA // 2, pac_y * TAMANO_CELDA + TAMANO_CELDA // 2), TAMANO_CELDA // 2)
    pygame.draw.circle(pantalla, ROJO, (fan_x * TAMANO_CELDA + TAMANO_CELDA // 2, fan_y * TAMANO_CELDA + TAMANO_CELDA // 2), TAMANO_CELDA // 2)
    pygame.draw.circle(pantalla, ROJO, (fan2_x * TAMANO_CELDA + TAMANO_CELDA // 2, fan2_y * TAMANO_CELDA + TAMANO_CELDA // 2), TAMANO_CELDA // 2)


def mover_pacman():
    global pac_x, pac_y, puntos
    nuevo_x, nuevo_y = pac_x + direccion_pacman[0], pac_y + direccion_pacman[1]
    if mapa[nuevo_y][nuevo_x] != "#":
        pac_x, pac_y = nuevo_x, nuevo_y
        if mapa[pac_y][pac_x] == ".":
            puntos += 10
            mapa[pac_y] = mapa[pac_y][:pac_x] + " " + mapa[pac_y][pac_x + 1:]


def mover_fantasma(fan_x, fan_y):
    direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    random.shuffle(direcciones)
    for dx, dy in direcciones:
        nuevo_x, nuevo_y = fan_x + dx, fan_y + dy
        if mapa[nuevo_y][nuevo_x] != "#":
            return nuevo_x, nuevo_y
    return fan_x, fan_y


def mostrar_game_over():
    root = tk.Tk()
    root.withdraw()
    respuesta = messagebox.askquestion("Game Over", f"¡Perdiste! Puntos: {puntos}. ¿Quieres jugar de nuevo?")
    if respuesta == 'yes':
        reiniciar_juego()
    else:
        pygame.quit()
        sys.exit()

def reiniciar_juego():
    global pac_x, pac_y, fan_x, fan_y, fan2_x, fan2_y, puntos, mapa
    pac_x, pac_y = 1, 1
    fan_x, fan_y = 10, 5
    fan2_x, fan2_y = 15, 3
    puntos = 0

reloj = pygame.time.Clock()

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                direccion_pacman = (0, -1)
            elif evento.key == pygame.K_DOWN:
                direccion_pacman = (0, 1)
            elif evento.key == pygame.K_LEFT:
                direccion_pacman = (-1, 0)
            elif evento.key == pygame.K_RIGHT:
                direccion_pacman = (1, 0)

    mover_pacman()
    fan_x, fan_y = mover_fantasma(fan_x, fan_y)
    fan2_x, fan2_y = mover_fantasma(fan2_x, fan2_y)

    dibujar_mapa()
    pygame.display.flip()

    if (pac_x, pac_y) in [(fan_x, fan_y), (fan2_x, fan2_y)]:
        mostrar_game_over()

    reloj.tick(5)  # Los fantasmas se mueven más lento
