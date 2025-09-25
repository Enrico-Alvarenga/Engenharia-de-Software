# tests/test_library.py
from src.library import SistemaBiblioteca

def test_status_inicial_do_sistema():
    """Testa se o sistema é inicializado corretamente."""
    sistema = SistemaBiblioteca()
    assert sistema.status() == "Sistema de Biblioteca Online!"

def test_cadastrar_livro():
    """Testa o Caso de Uso 1: Cadastrar um novo livro."""
    sistema = SistemaBiblioteca()
    sucesso = sistema.cadastrar_livro(titulo="O Senhor dos Anéis", autor="J.R.R. Tolkien", isbn="978-8533613379")
    
    assert sucesso is True
    
    livro = sistema.consultar_livro_por_isbn("978-8533613379")
    assert livro is not None
    assert livro['titulo'] == "O Senhor dos Anéis"
    assert livro['autor'] == "J.R.R. Tolkien"

def test_cadastrar_usuario():
    """Testa o Caso de Uso 2: Cadastrar um novo usuário."""
    sistema = SistemaBiblioteca()
    sucesso = sistema.cadastrar_usuario(nome="Eduardo Cipolaro", ra="168797")
    
    assert sucesso is True
    
    usuario = sistema.consultar_usuario_por_ra("168797")
    assert usuario is not None
    assert usuario['nome'] == "Eduardo Cipolaro"

# --- NOVOS TESTES PARA O CASO DE USO 3: EMPRÉSTIMO ---

def test_emprestimo_livro_sucesso():
    """Testa o 'caminho feliz' do empréstimo de um livro."""
    sistema = SistemaBiblioteca()
    # PREPARAÇÃO: Cadastra o livro e o usuário
    isbn = "978-0321765723"
    ra = "171280"
    sistema.cadastrar_livro(titulo="Clean Code", autor="Robert C. Martin", isbn=isbn)
    sistema.cadastrar_usuario(nome="Enrico Alvarenga", ra=ra)

    # AÇÃO: Realiza o empréstimo
    sucesso = sistema.realizar_emprestimo(ra_usuario=ra, isbn_livro=isbn)

    # VERIFICAÇÃO
    assert sucesso is True
    # Verifica se o livro ficou indisponível
    livro = sistema.consultar_livro_por_isbn(isbn)
    assert livro['disponivel'] is False
    # Verifica se o livro está na lista do usuário
    usuario = sistema.consultar_usuario_por_ra(ra)
    assert isbn in usuario['livros_emprestados']

def test_emprestimo_livro_indisponivel():
    """Testa a tentativa de emprestar um livro que já foi emprestado."""
    sistema = SistemaBiblioteca()
    # PREPARAÇÃO: Cadastra livro e usuários
    isbn = "978-0321765723"
    ra1 = "171280"
    ra2 = "168797"
    sistema.cadastrar_livro(titulo="Clean Code", autor="Robert C. Martin", isbn=isbn)
    sistema.cadastrar_usuario(nome="Enrico Alvarenga", ra=ra1)
    sistema.cadastrar_usuario(nome="Eduardo Cipolaro", ra=ra2)
    # Primeiro empréstimo (deve funcionar)
    sistema.realizar_emprestimo(ra_usuario=ra1, isbn_livro=isbn)

    # AÇÃO: Tenta emprestar o mesmo livro para outro usuário
    sucesso_segunda_tentativa = sistema.realizar_emprestimo(ra_usuario=ra2, isbn_livro=isbn)

    # VERIFICAÇÃO
    assert sucesso_segunda_tentativa is False

def test_emprestimo_livro_inexistente():
    """Testa a tentativa de emprestar um livro que não existe no acervo."""
    sistema = SistemaBiblioteca()
    # PREPARAÇÃO
    ra = "171280"
    sistema.cadastrar_usuario(nome="Enrico Alvarenga", ra=ra)

    # AÇÃO: Tenta emprestar um livro com ISBN que não foi cadastrado
    sucesso = sistema.realizar_emprestimo(ra_usuario=ra, isbn_livro="999-9999999999")

    # VERIFICAÇÃO
    assert sucesso is False
