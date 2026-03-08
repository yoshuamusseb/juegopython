# ========================================== #
# Nombre: Hansel Morla Concepción            #
# Matrícula: 24-EISN-2-035                   #
# Proyecto: El Reencuentro de Snoppy         #
# ========================================== #

import pygame
from scripts.maze import TILE_SIZE

class Player:
    def __init__(self):
        self.row = 1
        self.col = 1
        self.size = TILE_SIZE

        # --- CARGAR Y LIMPIAR EL FONDO MAGENTA ---
        try:
            ruta_imagen = "assets/images/player.png"
            # 1. Cargamos la imagen original con convert_alpha para poder manipular el canal invisible
            sheet_raw = pygame.image.load(ruta_imagen).convert_alpha()
            
            # 2. Escalamos la tira completa (4 cuadros de 40px)
            sheet_scaled = pygame.transform.scale(sheet_raw, (TILE_SIZE * 4, TILE_SIZE))
            
            # 3. Extraemos los cuadros aplicando la limpieza de píxeles
            self.sprites = {
                "ARRIBA":    self._get_frame(sheet_scaled, 0),          
                "ABAJO":     self._get_frame(sheet_scaled, TILE_SIZE),      
                "IZQUIERDA": self._get_frame(sheet_scaled, TILE_SIZE * 2),  
                "DERECHA":   self._get_frame(sheet_scaled, TILE_SIZE * 3)   
            }
            
            self.image = self.sprites["ABAJO"]
            
        except Exception as e:
            print(f"⚠️ Error: {e}")
            self.image = None
            self.color = (0, 0, 255) 

        # Configuración de movimiento y fuente
        self.huesos_recolectados = 0
        self.move_delay = 12  
        self.move_counter = 0
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 22, bold=True)

    def _get_frame(self, sheet, x_pos):
        """ Crea un cuadro individual y elimina quirúrgicamente el color magenta """
        # Creamos una superficie de 40x40 con soporte para transparencia (SRCALPHA)
        frame = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        
        # Copiamos la parte correspondiente de la tira escalada
        frame.blit(sheet, (0, 0), (x_pos, 0, TILE_SIZE, TILE_SIZE))
        
        # --- ELIMINACIÓN DE PÍXELES MAGENTA ---
        # Recorremos cada píxel del cuadro para detectar el fondo rosa
        for x in range(frame.get_width()):
            for y in range(frame.get_height()):
                pixel = frame.get_at((x, y))
                # Filtro: Si tiene mucho Rojo, mucho Azul y poco Verde, es el fondo magenta
                if pixel.r > 200 and pixel.b > 200 and pixel.g < 100:
                    # Lo convertimos en transparente total (0,0,0,0)
                    frame.set_at((x, y), (0, 0, 0, 0))
        
        return frame

    def handle_movement(self, current_maze):
        keys = pygame.key.get_pressed()
        self.move_counter += 1
        if self.move_counter < self.move_delay: return False

        new_row, new_col = self.row, self.col
        moved = False

        # --- SOPORTE PARA GAMEPAD ---
        joy_x, joy_y = 0, 0
        if pygame.joystick.get_count() > 0:
            joystick = pygame.joystick.Joystick(0)
            # Leer ejes analógicos si los hay
            if joystick.get_numaxes() >= 2:
                joy_x = joystick.get_axis(0)
                joy_y = joystick.get_axis(1)
            # Leer cruceta (D-PAD) si la hay
            dpad = (0, 0)
            if joystick.get_numhats() > 0:
                dpad = joystick.get_hat(0)
            joy_x = joy_x if abs(joy_x) > 0.5 else dpad[0]
            joy_y = joy_y if abs(joy_y) > 0.5 else -dpad[1] 

        if keys[pygame.K_w] or keys[pygame.K_UP] or joy_y < -0.5: 
            new_row -= 1; moved = True
            self.image = self.sprites["ARRIBA"]
        elif keys[pygame.K_s] or keys[pygame.K_DOWN] or joy_y > 0.5: 
            new_row += 1; moved = True
            self.image = self.sprites["ABAJO"]
        elif keys[pygame.K_a] or keys[pygame.K_LEFT] or joy_x < -0.5: 
            new_col -= 1; moved = True
            self.image = self.sprites["IZQUIERDA"]
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT] or joy_x > 0.5: 
            new_col += 1; moved = True
            self.image = self.sprites["DERECHA"]

        if moved:
            if 0 <= new_row < len(current_maze) and 0 <= new_col < len(current_maze[0]):
                if current_maze[new_row][new_col] != 1:
                    self.row, self.col = new_row, new_col
                    self.move_counter = 0 
                    if current_maze[new_row][new_col] == 3:
                        current_maze[new_row][new_col] = 0 
                        self.huesos_recolectados += 1
                    return True 
        return False

    def draw(self, screen, total_huesos, nivel_actual):
        if self.image:
            screen.blit(self.image, (self.col * TILE_SIZE, self.row * TILE_SIZE))
        else:
            pygame.draw.rect(screen, (0,0,255), (self.col * TILE_SIZE, self.row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        # Marcador de huesos
        texto = f"HUESOS: {self.huesos_recolectados} / {total_huesos}"
        surf = self.font.render(texto, True, (0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), (5, 5, surf.get_width() + 10, 30))
        screen.blit(surf, (10, 10))

    def get_grid_position(self):
        return (self.row, self.col)