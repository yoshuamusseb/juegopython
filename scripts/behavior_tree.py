# ========================================== #
# Nombre: Hansel Morla Concepción            #
# Matrícula: 24-EISN-2-035                   #
# Proyecto: El Reencuentro de Snoppy         #
# ========================================== #

class Node:
    """Clase base para los nodos del árbol de comportamiento (Behavior Tree)."""
    def tick(self, context):
        raise NotImplementedError("El método tick debe ser implementado")

class Selector(Node):
    """
    Evalúa sus hijos secuencialmente. 
    Devuelve SUCCESS si alguno tiene éxito, FAILURE si todos fallan.
    """
    def __init__(self, children):
        self.children = children

    def tick(self, context):
        for child in self.children:
            status = child.tick(context)
            if status == "SUCCESS":
                return "SUCCESS"
            elif status == "RUNNING":
                return "RUNNING"
        return "FAILURE"

class Sequence(Node):
    """
    Evalúa sus hijos secuencialmente. 
    Devuelve FAILURE si alguno falla, SUCCESS si todos tienen éxito.
    """
    def __init__(self, children):
        self.children = children

    def tick(self, context):
        for child in self.children:
            status = child.tick(context)
            if status == "FAILURE":
                return "FAILURE"
            elif status == "RUNNING":
                return "RUNNING"
        return "SUCCESS"

class CheckPlayerVisible(Node):
    """Nodo de condición: Comprueba si el jugador está dentro del rango de visión."""
    def tick(self, context):
        if context.get('player_visible', False):
            return "SUCCESS"
        return "FAILURE"

class CheckHealthStats(Node):
    """Nodo de condición: Simula comprobar si el enemigo debe huir en lugar de perseguir."""
    def tick(self, context):
        # Si tiene miedo (por ejemplo, Snoopy recogió un powerup temporal o comportamiento scriptado)
        # Por ahora lo controlaremos con una variable en el contexto
        if context.get('should_flee', False):
            return "SUCCESS"
        return "FAILURE"

class ActionFlee(Node):
    """Nodo de acción: Cambiar el estado del enemigo a HUIR."""
    def tick(self, context):
        context['state'] = "HUIR"
        return "SUCCESS"

class ActionChase(Node):
    """Nodo de acción: Cambiar el estado del enemigo a PERSECUCION."""
    def tick(self, context):
        context['state'] = "PERSECUCION"
        return "SUCCESS"

class ActionPatrol(Node):
    """Nodo de acción: Cambiar el estado del enemigo a PATRULLA."""
    def tick(self, context):
        context['state'] = "PATRULLA"
        return "SUCCESS"

# --- Construcción del Árbol para el Enemigo ---

def build_enemy_behavior_tree():
    """Construye y devuelve el árbol de comportamiento principal del enemigo (Lobo)."""
    
    # Comportamiento de Huida
    flee_sequence = Sequence([
        CheckPlayerVisible(),
        CheckHealthStats(), # ¿Debería huir?
        ActionFlee()
    ])
    
    # Comportamiento de Persecución
    chase_sequence = Sequence([
        CheckPlayerVisible(),
        ActionChase()
    ])
    
    # Comportamiento por defecto (Patrulla)
    patrol_action = ActionPatrol()
    
    # El árbol evalúa: 1. ¿Debo huir?, 2. ¿Debo perseguir?, 3. Entonces patrullo
    root = Selector([
        flee_sequence,
        chase_sequence,
        patrol_action
    ])
    
    return root
