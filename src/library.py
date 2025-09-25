# src/library.py

class SistemaBiblioteca:
    def __init__(self):
        # Usaremos o ISBN como chave única para o dicionário de livros
        self.livros = {}
        # Usaremos o RA como chave única para o dicionário de usuários
        self.usuarios = {}

    def status(self):
        """Retorna o status inicial do sistema."""
        return "Sistema de Biblioteca Online!"

    # --- MÉTODOS PARA O CASO DE USO 1: LIVROS ---
    def cadastrar_livro(self, titulo, autor, isbn):
        """
        Cadastra um novo livro no sistema, desde que o ISBN não esteja duplicado.
        """
        if isbn not in self.livros:
            self.livros[isbn] = {
                'titulo': titulo,
                'autor': autor,
                'disponivel': True
            }
            return True  # Retorna sucesso
        return False  # Retorna falha (livro já existe)

    def consultar_livro_por_isbn(self, isbn):
        """
        Consulta e retorna os dados de um livro pelo seu ISBN.
        """
        return self.livros.get(isbn)

    # --- MÉTODOS PARA O CASO DE USO 2: USUÁRIOS ---
    def cadastrar_usuario(self, nome, ra):
        """
        Cadastra um novo usuário no sistema, desde que o RA não esteja duplicado.
        """
        if ra not in self.usuarios:
            self.usuarios[ra] = {'nome': nome, 'livros_emprestados': []}
            return True  # Retorna sucesso
        return False  # Retorna falha (usuário já existe)

    def consultar_usuario_por_ra(self, ra):
        """
        Consulta e retorna os dados de um usuário pelo seu RA.
        """
        return self.usuarios.get(ra)

    # --- MÉTODO PARA O CASO DE USO 3: EMPRÉSTIMO ---
    def realizar_emprestimo(self, ra_usuario, isbn_livro):
        """
        Realiza o empréstimo de um livro para um usuário.
        Retorna True se o empréstimo for bem-sucedido, False caso contrário.
        """
        usuario = self.consultar_usuario_por_ra(ra_usuario)
        livro = self.consultar_livro_por_isbn(isbn_livro)

        # Valida se o usuário e o livro existem e se o livro está disponível
        if usuario and livro and livro['disponivel']:
            # Atualiza o status do livro
            livro['disponivel'] = False
            # Adiciona o livro na lista do usuário
            usuario['livros_emprestados'].append(isbn_livro)
            return True
        
        # Se qualquer uma das condições falhar, retorna False
        return False
