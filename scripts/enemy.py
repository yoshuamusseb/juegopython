# ========================================== #
# Nombre: Hansel Morla Concepción            #
# Matrícula: 24-EISN-2-035                   #
# Proyecto: El Reencuentro de Snoppy         #
# ========================================== #

import pygame
import os
import random
from scripts.pathfinding import a_star
from scripts.maze import TILE_SIZE
from scripts.behavior_tree import build_enemy_behavior_tree

class Enemy:
    def __init__(self, maze_data):
        # --- POSICIÓN Y CONFIGURACIÓN ---
        self.row, self.col = self._spawn_logic(maze_data)
        self.maze_data = maze_data
        
        # --- CARGAR IMAGEN DEL LOBO ---
        try:
            ruta = os.path.join("assets", "images", "enemy.png")
            sheet_raw = pygame.image.load(ruta).convert_alpha()
            
            # 1. Tamaño original de un frame
            raw_w = sheet_raw.get_width() // 4
            raw_h = sheet_raw.get_height()
            
            # 2. ESCALA MANUAL: 
            # Si se ve pequeño, sube este número (ej. 2.5). 
            # Si se ve grande, bájalo (ej. 1.5).
            escala_lobo = 0.4
            
            self.sprite_w = int(raw_w * escala_lobo)
            self.sprite_h = int(raw_h * escala_lobo)
            
            # 3. Escalamos la hoja completa
            sheet_scaled = pygame.transform.scale(sheet_raw, (self.sprite_w * 4, self.sprite_h))
            
            self.sprites = {
                "ARRIBA":    self._get_frame(sheet_scaled, 0),          
                "ABAJO":     self._get_frame(sheet_scaled, self.sprite_w),      
                "IZQUIERDA": self._get_frame(sheet_scaled, self.sprite_w * 2),  
                "DERECHA":   self._get_frame(sheet_scaled, self.sprite_w * 3)   
            }
            self.image = self.sprites["ABAJO"]
        except Exception as e:
            print(f"Error cargando enemigo: {e}")
            self.image = None
            self.sprite_w, self.sprite_h = TILE_SIZE, TILE_SIZE

        # --- TU IA (AHORA CON ÁRBOL DE COMPORTAMIENTO) ---
        self.move_delay = 25  
        self.move_counter = 0
        self.vision_range = 7
        self.state = "PATRULLA"
        self.persistence_timer = 0
        self.persistence_duration = 9 * 60 
        self.direction = (0, 1)
        
        # Instanciar el árbol de comportamiento
        self.behavior_tree = build_enemy_behavior_tree()

    def _get_frame(self, sheet, x_pos):
        frame = pygame.Surface((self.sprite_w, self.sprite_h), pygame.SRCALPHA)
        frame.blit(sheet, (0, 0), (x_pos, 0, self.sprite_w, self.sprite_h))
        # Quita el fondo usando el color del primer píxel si no es transparente
        color_fondo = frame.get_at((0, 0))
        frame.set_colorkey(color_fondo)
        return frame

    def _spawn_logic(self, maze):
        for r in range(len(maze)-2, 0, -1):
            for c in range(len(maze[0])-2, 0, -1):
                if maze[r][c] == 0: return r, c
        return 1, 1

    def tiene_linea_de_vision(self, player_pos, maze):
        r0, c0 = self.row, self.col
        r1, c1 = player_pos
        diff_r, diff_c = r1 - r0, c1 - c0
        pasos = max(abs(diff_r), abs(diff_c))
        if pasos == 0: return True
        for i in range(1, pasos):
            check_r = int(r0 + (diff_r * i / pasos))
            check_c = int(c0 + (diff_c * i / pasos))
            if maze[check_r][check_c] == 1: return False
        return True

    def update(self, player_pos, huesos_recolectados=0, huesos_totales=1): 
        # Modificamos para aceptar estado de huesos (para decidir huir)
        self.move_counter += 1
        if self.persistence_timer > 0: self.persistence_timer -= 1

        if self.move_counter >= self.move_delay:
            dist = abs(self.row - player_pos[0]) + abs(self.col - player_pos[1])
            lo_ve = dist <= self.vision_range and self.tiene_linea_de_vision(player_pos, self.maze_data)

            if lo_ve: self.persistence_timer = self.persistence_duration
            
            # Contexto para el árbol de comportamiento
            context = {
                'player_visible': self.persistence_timer > 0,
                'should_flee': False,
                'state': self.state
            }
            
            # Lógica para decidir si el lobo debe Huir: si el jugador casi termina de recoger huesos
            if huesos_recolectados >= huesos_totales - 1 and huesos_totales > 1:
                context['should_flee'] = True

            # Ejecutar el árbol de comportamiento que actualiza context['state']
            self.behavior_tree.tick(context)
            self.state = context['state']
            
            if self.state == "HUIR":
                # Lógica del estado HUIR: alejarse del jugador
                posibles = []
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = self.row + dr, self.col + dc
                    if 0 <= nr < len(self.maze_data) and 0 <= nc < len(self.maze_data[0]) and self.maze_data[nr][nc] != 1:
                        # Sólo añadir direcciones que incrementan la distancia
                        ndist = abs(nr - player_pos[0]) + abs(nc - player_pos[1])
                        if ndist > dist:
                            posibles.append((dr, dc))
                
                # Si está acorralado y no puede alejarse más, se mueve a cualquier lado válido
                if not posibles:
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = self.row + dr, self.col + dc
                        if 0 <= nr < len(self.maze_data) and 0 <= nc < len(self.maze_data[0]) and self.maze_data[nr][nc] != 1:
                            posibles.append((dr, dc))

                if posibles:
                    self.direction = random.choice(posibles)
                    self.row += self.direction[0]
                    self.col += self.direction[1]
                    self._update_sprite(self.direction[0], self.direction[1])
                    
            elif self.state == "PERSECUCION":
                path = a_star((self.row, self.col), player_pos, self.maze_data)
                if path and len(path) > 1:
                    next_s = path[1]
                    self._update_sprite(next_s[0] - self.row, next_s[1] - self.col)
                    self.row, self.col = next_s
            else:
                self.state = "PATRULLA"
                posibles = []
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = self.row + dr, self.col + dc
                    if 0 <= nr < len(self.maze_data) and 0 <= nc < len(self.maze_data[0]) and self.maze_data[nr][nc] != 1:
                        posibles.append((dr, dc))
                if posibles:
                    atras = (-self.direction[0], -self.direction[1])
                    opciones = [c for c in posibles if c != atras]
                    self.direction = random.choice(opciones) if opciones else random.choice(posibles)
                    self.row += self.direction[0]
                    self.col += self.direction[1]
                    self._update_sprite(self.direction[0], self.direction[1])
            self.move_counter = 0

    def _update_sprite(self, dr, dc):
        if not self.image: return
        if dr > 0: self.image = self.sprites["ABAJO"]
        elif dr < 0: self.image = self.sprites["ARRIBA"]
        elif dc > 0: self.image = self.sprites["DERECHA"]
        elif dc < 0: self.image = self.sprites["IZQUIERDA"]

    def draw(self, screen):
        if self.image:
            # Centramos el lobo respecto al punto de la IA
            offset_x = (self.sprite_w - TILE_SIZE) // 2
            offset_y = (self.sprite_h - TILE_SIZE) // 2
            screen.blit(self.image, (self.col * TILE_SIZE - offset_x, self.row * TILE_SIZE - offset_y))
        else:
            if self.state == "PERSECUCION":
                color = (255, 0, 0) # Rojo
            elif self.state == "HUIR":
                color = (255, 255, 0) # Amarillo 
            else:
                color = (0, 100, 255) # Azul patrulla
            pygame.draw.rect(screen, color, (self.col * TILE_SIZE, self.row * TILE_SIZE, TILE_SIZE, TILE_SIZE))