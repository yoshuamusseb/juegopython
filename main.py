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
PAUSA = 3

def draw_menu(screen):
    screen.fill((30, 30, 30))
    # Tamaño de la fuente ajustado para que no sea muy grande
    font_titulo = pygame.font.SysFont("Arial", 32, bold=True)
    font_boton = pygame.font.SysFont("Arial", 28, bold=True)
    font_info = pygame.font.SysFont("Arial", 18)

    titulo = font_titulo.render("EL REENCUENTRO DE SNOOPPY", True, (255, 255, 255))
    screen.blit(titulo, (screen.get_width()//2 - titulo.get_width()//2, 80))

    boton_jugar = pygame.Rect(screen.get_width()//2 - 100, 180, 200, 60)
    pygame.draw.rect(screen, (0, 150, 0), boton_jugar, border_radius=12)
    texto_jugar = font_boton.render("INICIAR JUEGO", True, (255, 255, 255))
    screen.blit(texto_jugar, (boton_jugar.centerx - texto_jugar.get_width()//2, 
                              boton_jugar.centery - texto_jugar.get_height()//2))

    boton_salir = pygame.Rect(screen.get_width()//2 - 100, 260, 200, 60)
    pygame.draw.rect(screen, (200, 0, 0), boton_salir, border_radius=12)
    texto_salir = font_boton.render("SALIR", True, (255, 255, 255))
    screen.blit(texto_salir, (boton_salir.centerx - texto_salir.get_width()//2, 
                              boton_salir.centery - texto_salir.get_height()//2))

    instrucciones = font_info.render("Usa W-A-S-D para moverte. ¡Evita al lobo y recoge los huesos!", True, (180, 180, 180))
    screen.blit(instrucciones, (screen.get_width()//2 - instrucciones.get_width()//2, 360))
    
    pygame.display.flip()
    return boton_jugar, boton_salir

def draw_pause(screen):
    # Capa semitransparente sobre el juego
    overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))
    
    font_titulo = pygame.font.SysFont("Arial", 50, bold=True)
    font_boton = pygame.font.SysFont("Arial", 28, bold=True)

    titulo = font_titulo.render("PAUSA", True, (255, 255, 255))
    screen.blit(titulo, (screen.get_width()//2 - titulo.get_width()//2, 100))

    boton_reanudar = pygame.Rect(screen.get_width()//2 - 100, 220, 200, 60)
    pygame.draw.rect(screen, (0, 150, 0), boton_reanudar, border_radius=12)
    texto_reanudar = font_boton.render("REANUDAR", True, (255, 255, 255))
    screen.blit(texto_reanudar, (boton_reanudar.centerx - texto_reanudar.get_width()//2, 
                                 boton_reanudar.centery - texto_reanudar.get_height()//2))

    boton_salir = pygame.Rect(screen.get_width()//2 - 100, 300, 200, 60)
    pygame.draw.rect(screen, (200, 0, 0), boton_salir, border_radius=12)
    texto_salir = font_boton.render("SALIR", True, (255, 255, 255))
    screen.blit(texto_salir, (boton_salir.centerx - texto_salir.get_width()//2, 
                              boton_salir.centery - texto_salir.get_height()//2))

    pygame.display.flip()
    return boton_reanudar, boton_salir

def draw_game(screen, player, enemy, total_huesos, maze_actual, nivel, is_paused=False):
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

    if not is_paused:
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
                
            # Salir rápido o pausar con la tecla ESC
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if game_state == JUEGO:
                    game_state = PAUSA
                elif game_state == PAUSA:
                    game_state = JUEGO
                else:
                    pygame.quit()
                    sys.exit()
            
            # Soporte de Gamepad/Control para Iniciar
            joystick_pressed = False
            if event.type == pygame.JOYBUTTONDOWN:
                joystick_pressed = True

            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or joystick_pressed:
                pos_clic = getattr(event, 'pos', (WIDTH//2, 190))
                
                if game_state == MENU:
                    boton_jugar = pygame.Rect(WIDTH//2 - 100, 180, 200, 60)
                    boton_salir = pygame.Rect(WIDTH//2 - 100, 260, 200, 60)
                    
                    if boton_jugar.collidepoint(pos_clic) or joystick_pressed:
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
                    elif boton_salir.collidepoint(pos_clic):
                        pygame.quit()
                        sys.exit()
                
                elif game_state == PAUSA:
                    boton_reanudar = pygame.Rect(WIDTH//2 - 100, 220, 200, 60)
                    boton_salir = pygame.Rect(WIDTH//2 - 100, 300, 200, 60)
                    
                    if boton_reanudar.collidepoint(pos_clic) or joystick_pressed:
                        game_state = JUEGO
                    elif boton_salir.collidepoint(pos_clic):
                        pygame.quit()
                        sys.exit()
                
                elif game_state == FIN:
                    boton_fin = pygame.Rect(WIDTH//2 - 110, 280, 220, 50)
                    if boton_fin.collidepoint(pos_clic) or joystick_pressed:
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
            
        elif game_state == PAUSA:
            draw_game(screen, player, enemy, huesos_totales, maze_jugable, nivel_actual_idx + 1, is_paused=True)
            draw_pause(screen)

        elif game_state == FIN:
            draw_victory(screen)

if __name__ == "__main__":
    main()