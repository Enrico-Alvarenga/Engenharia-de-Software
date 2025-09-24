class SistemaBiblioteca:
    def __init__(self):
        self.livros = {}
        self.usuarios = {}

    def status(self):
        """Retorna o status inicial do sistema."""
        return "Sistema de Biblioteca Online!"
