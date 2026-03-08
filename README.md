# El Reencuentro de Snooppy 🐾

Un juego desarrollado exclusivamente en **Python** utilizando **Pygame**, que implementa Inteligencia Artificial pura (A-Star y Behavior Trees) sin uso de librerías externas para la lógica.

## 👨‍💻 Autor
- **Nombre:** Hansel Morla Concepción
- **Matrícula:** 24-EISN-2-035
- **Materia:** Inteligencia Artificial / Desarrollo
- **Examen:** Parcial 

## 🎮 Acerca del Juego
El jugador controla a Snoopy en un laberinto en busca de huesos perdidos. Sin embargo, no está solo. Un feroz lobo deambula por el escenario. 
El lobo utiliza un **Árbol de Comportamiento (Behavior Tree)** para tomar decisiones dinámicas (Patrullar, Perseguir o Huir) y el algoritmo **A-Estrella (A*)** basado en la distancia Manhattan para trazar la ruta más corta y atrapar al jugador si este entra en su rango de visión.

### Controles
- **W, A, S, D** o **Flechas Direccionales**: Moverse
- **Esc**: Pausar / Salir
- **Gamepad / Joystick**: Soportado nativamente

## ⚙️ Requisitos Técnicos e Instalación (Windows)
1. Instalar Python (3.9 o superior) asegurándose de añadirlo al PATH.
2. Clonar el repositorio.
3. Crear un entorno virtual: `python -m venv .venv`
4. Activar el entorno: `.venv\Scripts\activate`
5. Instalar dependencias: `pip install -r requirements.txt`
6. Ejecutar: `python main.py`

## 🧩 Estructura Principal
- `main.py`: Bucle principal y control de estados (Menú, Juego, Pausa).
- `scripts/pathfinding.py`: Lógica original del algoritmo A* y heurísticas.
- `scripts/behavior_tree.py`: Árbol jerárquico de comportamiento del enemigo.
- `scripts/enemy.py`: Clase del enemigo que integra su IA y movimientos.
- `scripts/player.py`: Clase del jugador y mecánicas de recolección.
