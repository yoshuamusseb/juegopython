# ========================================== #
# Nombre: Hansel Morla Concepción            #
# Matrícula: 24-EISN-2-035                   #
# Proyecto: El Reencuentro de Snoppy         #
# ========================================== #

import pygame
import os

TILE_SIZE = 40
TREE_IMG = None 

# --- NIVELES (maze1 y maze2) ---
maze1 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 3, 0, 0, 0, 0, 0, 0, 3, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 3, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

maze2 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 3, 0, 0, 1, 0, 0, 0, 3, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 3, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 3, 0, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 3, 0, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

niveles = [maze1, maze2]

def _limpiar_quirurgico(image):
    """ Filtra píxeles casi blancos (sucios) para transparencia total """
    frame = image.convert_alpha()
    for x in range(frame.get_width()):
        for y in range(frame.get_height()):
            p = frame.get_at((x, y))
            # Si el píxel es muy claro (ruido blanco/gris), lo borramos
            if p.r > 220 and p.g > 220 and p.b > 220:
                frame.set_at((x, y), (0, 0, 0, 0))
    return frame

def draw_maze(screen, current_maze):
    global TREE_IMG
    if TREE_IMG is None:
        ruta = os.path.join("assets", "images", "tree.png")
        if os.path.exists(ruta):
            img_raw = pygame.image.load(ruta)
            img_limpia = _limpiar_quirurgico(img_raw)
            TREE_IMG = pygame.transform.scale(img_limpia, (TILE_SIZE, TILE_SIZE))

    # Colores y Dibujo
    GRASS = (34, 139, 34)
    BONE = (255, 255, 255)
    
    for r in range(len(current_maze)):
        for c in range(len(current_maze[0])):
            x, y = c * TILE_SIZE, r * TILE_SIZE
            pygame.draw.rect(screen, GRASS, (x, y, TILE_SIZE, TILE_SIZE))
            
            val = current_maze[r][c]
            if val == 1 and TREE_IMG:
                screen.blit(TREE_IMG, (x, y))
            elif val == 3: # Hueso detallado
                pygame.draw.circle(screen, BONE, (x+12, y+15), 6)
                pygame.draw.circle(screen, BONE, (x+12, y+25), 6)
                pygame.draw.rect(screen, BONE, (x+12, y+17, 16, 6))
                pygame.draw.circle(screen, BONE, (x+28, y+15), 6)
                pygame.draw.circle(screen, BONE, (x+28, y+25), 6)
            elif val == 2: # Meta
                pygame.draw.rect(screen, (124, 252, 0), (x, y, TILE_SIZE, TILE_SIZE))

def contar_items(maze):
    return sum(fila.count(3) for fila in maze)