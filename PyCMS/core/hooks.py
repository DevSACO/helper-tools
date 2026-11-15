from collections import defaultdict

class HookManager:
    def __init__(self):
        # Estructura: { 'nombre_hook': { prioridad: [funciones] } }
        self.actions = defaultdict(lambda: defaultdict(list))
        self.filters = defaultdict(lambda: defaultdict(list))

    def add_action(self, tag, func, priority=10):
        """Registra una función para ejecutarse en un evento."""
        self.actions[tag][priority].append(func)

    def do_action(self, tag, *args, **kwargs):
        """Ejecuta todas las funciones registradas en un evento."""
        if tag in self.actions:
            for priority in sorted(self.actions[tag].keys()):
                for func in self.actions[tag][priority]:
                    func(*args, **kwargs)

    def add_filter(self, tag, func, priority=10):
        """Registra una función para modificar un valor."""
        self.filters[tag][priority].append(func)

    def do_action_to_string(self, tag, *args, **kwargs) -> str:
        """
        Ejecuta las funciones registradas en un evento y concatena
        los strings que devuelvan. Ideal para inyectar HTML.
        """
        html_output = []
        if tag in self.actions:
            for priority in sorted(self.actions[tag].keys()):
                for func in self.actions[tag][priority]:
                    resultado = func(*args, **kwargs)
                    if isinstance(resultado, str):
                        html_output.append(resultado)
        return "\n".join(html_output)

    def apply_filters(self, tag, value, *args, **kwargs):
        """Pasa un valor por todas las funciones registradas y devuelve el resultado."""
        if tag in self.filters:
            for priority in sorted(self.filters[tag].keys()):
                for func in self.filters[tag][priority]:
                    # El valor se va reescribiendo en cascada
                    value = func(value, *args, **kwargs)
        return value

# Instancia global para ser importada por el Core y los Plugins
hooks = HookManager()
