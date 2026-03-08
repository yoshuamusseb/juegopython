# ========================================== #
# Nombre: Hansel Morla Concepción            #
# Matrícula: 24-EISN-2-035                   #
# Proyecto: El Reencuentro de Snoppy         #
# ========================================== #

import heapq

def heuristic(a, b):
    """
    Calcula la 'distancia Manhattan' entre dos puntos (a y b).
    Es la suma de las diferencias absolutas de sus coordenadas.
    Ideal para juegos de cuadrícula donde no hay movimientos diagonales.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(start, goal, maze):
    """
    Algoritmo A* (A-Estrella).
    Encuentra el camino más corto desde 'start' hasta 'goal' evitando obstáculos.
    """
    rows = len(maze)
    cols = len(maze[0])

    # Verificación de seguridad: si el inicio o fin están fuera del mapa, salimos
    if not (0 <= start[0] < rows and 0 <= start[1] < cols) or \
       not (0 <= goal[0] < rows and 0 <= goal[1] < cols):
        return None

    # open_set: Lista de nodos por explorar, priorizada por el costo total (f_score)
    open_set = []
    # Usamos heapq para que el nodo con el costo más bajo siempre esté al principio
    heapq.heappush(open_set, (0, start))

    # came_from: Diccionario para reconstruir el camino al final (rastrea el origen de cada paso)
    came_from = {}
    
    # g_score: El costo real de ir desde el inicio hasta un nodo específico
    g_score = {start: 0}
    
    while open_set:
        # Extraemos el nodo con el f_score más bajo (el que parece estar más cerca de la meta)
        current = heapq.heappop(open_set)[1]

        # Si llegamos a la posición de Snooppy (goal), reconstruimos el camino
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse() # Invertimos la lista para que vaya del inicio al fin
            return path

        row, col = current
        # Explorar vecinos: Abajo, Arriba, Derecha, Izquierda
        for r, c in [(row+1, col), (row-1, col), (row, col+1), (row, col-1)]:
            # Comprobar que el vecino esté dentro de los límites del mapa
            if 0 <= r < rows and 0 <= c < cols:
                
                # --- LÓGICA DE COLISIÓN DEL ENEMIGO ---
                # El enemigo solo ignora la celda si es una pared (1).
                # Puede atravesar pasillos (0), metas (2) y huesos (3).
                if maze[r][c] == 1:
                    continue

                # El costo de moverse a un vecino es siempre +1 casilla
                tentative_g = g_score[current] + 1
                neighbor = (r, c)

                # Si encontramos un camino más corto hacia este vecino, lo guardamos
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    # f = g (esfuerzo realizado) + h (esfuerzo estimado hasta la meta)
                    f = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f, neighbor))

    # Si el bucle termina sin encontrar el 'goal', no hay camino posible
    return None