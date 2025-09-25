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

        if usuario and livro and livro['disponivel']:
            livro['disponivel'] = False
            usuario['livros_emprestados'].append(isbn_livro)
            return True
        
        return False

    # --- MÉTODO PARA O CASO DE USO 4: DEVOLUÇÃO ---
    def realizar_devolucao(self, ra_usuario, isbn_livro):
        """
        Registra a devolução de um livro por um usuário.
        Retorna True se a devolução for bem-sucedida, False caso contrário.
        """
        usuario = self.consultar_usuario_por_ra(ra_usuario)
        livro = self.consultar_livro_por_isbn(isbn_livro)

        if usuario and livro and isbn_livro in usuario['livros_emprestados']:
            livro['disponivel'] = True
            usuario['livros_emprestados'].remove(isbn_livro)
            return True
            
        return False

    # --- MÉTODO PARA O CASO DE USO 5: CONSULTAS / RELATÓRIOS ---
    def listar_livros_disponiveis(self):
        """
        Retorna uma lista de todos os livros com status 'disponivel'.
        """
        return [livro for livro in self.livros.values() if livro['disponivel']]
