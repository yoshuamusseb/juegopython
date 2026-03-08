# ========================================== #
# Nombre: Hansel Morla Concepción            #
# Matrícula: 24-EISN-2-035                   #
# Proyecto: El Reencuentro de Snoppy         #
# ========================================== #

import pygame
import sys
from scripts.maze import niveles, TILE_SIZE, draw_maze, contar_items
from scripts.player import Player
from scripts.enemy import Enemy

# --- CONSTANTES DE ESTADO ---
MENU = 0
JUEGO = 1
FIN = 2

def draw_menu(screen):
    screen.fill((30, 30, 30))
    font_titulo = pygame.font.SysFont("Arial", 44, bold=True)
    font_boton = pygame.font.SysFont("Arial", 30, bold=True)
    font_info = pygame.font.SysFont("Arial", 18)

    titulo = font_titulo.render("EL REENCUENTRO DE SNOOPPY", True, (255, 255, 255))
    screen.blit(titulo, (screen.get_width()//2 - titulo.get_width()//2, 80))

    boton_rect = pygame.Rect(screen.get_width()//2 - 100, 220, 200, 60)
    pygame.draw.rect(screen, (0, 150, 0), boton_rect, border_radius=12)
    texto_btn = font_boton.render("EMPEZAR", True, (255, 255, 255))
    screen.blit(texto_btn, (boton_rect.centerx - texto_btn.get_width()//2, 
                            boton_rect.centery - texto_btn.get_height()//2))

    instrucciones = font_info.render("Usa W-A-S-D para moverte. ¡Evita al lobo y recoge los huesos!", True, (180, 180, 180))
    screen.blit(instrucciones, (screen.get_width()//2 - instrucciones.get_width()//2, 320))
    
    pygame.display.flip()
    return boton_rect

def draw_game(screen, player, enemy, total_huesos, maze_actual, nivel):
    # 1. COLOR DE FONDO (Más oscuro si es nivel 2)
    if nivel == 2:
        screen.fill((10, 20, 10)) # Verde petróleo muy oscuro
        grass_detail = (5, 40, 5)
    else:
        screen.fill((34, 139, 34)) # Verde normal
        grass_detail = (20, 100, 20)

    # Dibujar detalles del césped
    for r in range(len(maze_actual)):
        for c in range(len(maze_actual[0])):
            if maze_actual[r][c] != 1:
                pygame.draw.line(screen, grass_detail, (c*TILE_SIZE+5, r*TILE_SIZE+20), (c*TILE_SIZE+10, r*TILE_SIZE+15), 2)

    # Dibujar mapa, jugador y enemigo normalmente
    draw_maze(screen, maze_actual) 
    player.draw(screen, total_huesos, nivel)
    enemy.draw(screen)

    # --- EFECTO DE NOCHE (SOLO NIVEL 2) ---
    if nivel == 2:
        # Capa de oscuridad
        oscurecimiento = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        oscurecimiento.fill((0, 0, 15, 235)) # Más oscuro (Alpha 235)

        # Círculo de luz reducido (80px = ~2 bloques)
        px = player.col * TILE_SIZE + TILE_SIZE // 2
        py = player.row * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(oscurecimiento, (0, 0, 0, 0), (px, py), 80) 
        
        screen.blit(oscurecimiento, (0, 0))

    pygame.display.flip()

def draw_victory(screen):
    screen.fill((10, 10, 10))
    font_fin = pygame.font.SysFont("Arial", 80, bold=True)
    font_boton = pygame.font.SysFont("Arial", 24, bold=True)

    texto = font_fin.render("EL FIN", True, (255, 255, 255))
    screen.blit(texto, (screen.get_width()//2 - texto.get_width()//2, 120))

    boton_rect = pygame.Rect(screen.get_width()//2 - 110, 280, 220, 50)
    pygame.draw.rect(screen, (100, 100, 100), boton_rect, border_radius=10)
    texto_btn = font_boton.render("VOLVER AL INICIO", True, (255, 255, 255))
    screen.blit(texto_btn, (boton_rect.centerx - texto_btn.get_width()//2, 
                            boton_rect.centery - texto_btn.get_height()//2))

    pygame.display.flip()
    return boton_rect

def main():
    pygame.init()
    pygame.mixer.init()
    pygame.joystick.init()
    
    # Inicializar gamepads/joysticks
    joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
    for joystick in joysticks:
        joystick.init()
        print(f"Joystick conectado: {joystick.get_name()}")
    
    WIDTH = len(niveles[0][0]) * TILE_SIZE
    HEIGHT = len(niveles[0]) * TILE_SIZE
    
    # Modo Pantalla Completa
    flags = pygame.FULLSCREEN | pygame.SCALED
    screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
    pygame.display.set_caption("Snooppy: Misión Huesos")
    
    clock = pygame.time.Clock()
    nivel_actual_idx = 0
    game_state = MENU

    player = Player()
    maze_jugable = [fila[:] for fila in niveles[nivel_actual_idx]]
    enemy = Enemy(maze_jugable) 
    huesos_totales = contar_items(maze_jugable)

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # Salir rápido con la tecla ESC
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            
            # Soporte de Gamepad/Control para Iniciar
            joystick_pressed = False
            if event.type == pygame.JOYBUTTONDOWN:
                joystick_pressed = True

            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or joystick_pressed:
                if game_state == MENU:
                    boton_menu = pygame.Rect(WIDTH//2 - 100, 220, 200, 60)
                    if boton_menu.collidepoint(event.pos):
                        nivel_actual_idx = 0
                        player = Player()
                        player.huesos_recolectados = 0
                        maze_jugable = [fila[:] for fila in niveles[nivel_actual_idx]]
                        huesos_totales = contar_items(maze_jugable)
                        enemy = Enemy(maze_jugable)
                        try:
                            pygame.mixer.music.load("assets/music/musica_fondo.mp3")
                            pygame.mixer.music.play(-1)
                        except: pass
                        game_state = JUEGO
                
                elif game_state == FIN:
                    boton_fin = pygame.Rect(WIDTH//2 - 110, 280, 220, 50)
                    if boton_fin.collidepoint(event.pos):
                        game_state = MENU

        if game_state == MENU:
            draw_menu(screen)
            
        elif game_state == JUEGO:
            player.handle_movement(maze_jugable)
            enemy.update(player.get_grid_position(), player.huesos_recolectados, huesos_totales)

            if (player.row, player.col) == (enemy.row, enemy.col):
                pygame.time.delay(500)
                player.row, player.col = 1, 1 
                player.huesos_recolectados = 0
                maze_jugable = [fila[:] for fila in niveles[nivel_actual_idx]]
                enemy = Enemy(maze_jugable) 
                
            if maze_jugable[player.row][player.col] == 2 and player.huesos_recolectados >= huesos_totales:
                if nivel_actual_idx < len(niveles) - 1:
                    nivel_actual_idx += 1
                    maze_jugable = [fila[:] for fila in niveles[nivel_actual_idx]]
                    huesos_totales = contar_items(maze_jugable)
                    player.row, player.col = 1, 1
                    player.huesos_recolectados = 0
                    enemy = Enemy(maze_jugable)
                else:
                    pygame.mixer.music.stop()
                    game_state = FIN
            
            draw_game(screen, player, enemy, huesos_totales, maze_jugable, nivel_actual_idx + 1)

        elif game_state == FIN:
            draw_victory(screen)

if __name__ == "__main__":
    main()