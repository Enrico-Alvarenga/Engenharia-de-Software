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

# --- TESTES PARA O CASO DE USO 3: EMPRÉSTIMO ---

def test_emprestimo_livro_sucesso():
    """Testa o 'caminho feliz' do empréstimo de um livro."""
    sistema = SistemaBiblioteca()
    # PREPARAÇÃO
    isbn = "978-0321765723"
    ra = "171280"
    sistema.cadastrar_livro(titulo="Clean Code", autor="Robert C. Martin", isbn=isbn)
    sistema.cadastrar_usuario(nome="Enrico Alvarenga", ra=ra)

    # AÇÃO
    sucesso = sistema.realizar_emprestimo(ra_usuario=ra, isbn_livro=isbn)

    # VERIFICAÇÃO
    assert sucesso is True
    livro = sistema.consultar_livro_por_isbn(isbn)
    assert livro['disponivel'] is False
    usuario = sistema.consultar_usuario_por_ra(ra)
    assert isbn in usuario['livros_emprestados']

def test_emprestimo_livro_indisponivel():
    """Testa a tentativa de emprestar um livro que já foi emprestado."""
    sistema = SistemaBiblioteca()
    # PREPARAÇÃO
    isbn = "978-0321765723"
    ra1 = "171280"
    ra2 = "168797"
    sistema.cadastrar_livro(titulo="Clean Code", autor="Robert C. Martin", isbn=isbn)
    sistema.cadastrar_usuario(nome="Enrico Alvarenga", ra=ra1)
    sistema.cadastrar_usuario(nome="Eduardo Cipolaro", ra=ra2)
    sistema.realizar_emprestimo(ra_usuario=ra1, isbn_livro=isbn)

    # AÇÃO
    sucesso_segunda_tentativa = sistema.realizar_emprestimo(ra_usuario=ra2, isbn_livro=isbn)

    # VERIFICAÇÃO
    assert sucesso_segunda_tentativa is False

def test_emprestimo_livro_inexistente():
    """Testa a tentativa de emprestar um livro que não existe no acervo."""
    sistema = SistemaBiblioteca()
    # PREPARAÇÃO
    ra = "171280"
    sistema.cadastrar_usuario(nome="Enrico Alvarenga", ra=ra)

    # AÇÃO
    sucesso = sistema.realizar_emprestimo(ra_usuario=ra, isbn_livro="999-9999999999")

    # VERIFICAÇÃO
    assert sucesso is False

# --- TESTES PARA O CASO DE USO 4: DEVOLUÇÃO ---

def test_devolucao_livro_sucesso():
    """Testa o 'caminho feliz' da devolução de um livro."""
    sistema = SistemaBiblioteca()
    # PREPARAÇÃO
    isbn = "978-0321765723"
    ra = "171280"
    sistema.cadastrar_livro(titulo="Clean Code", autor="Robert C. Martin", isbn=isbn)
    sistema.cadastrar_usuario(nome="Enrico Alvarenga", ra=ra)
    sistema.realizar_emprestimo(ra_usuario=ra, isbn_livro=isbn)

    # AÇÃO
    sucesso = sistema.realizar_devolucao(ra_usuario=ra, isbn_livro=isbn)

    # VERIFICAÇÃO
    assert sucesso is True
    livro = sistema.consultar_livro_por_isbn(isbn)
    assert livro['disponivel'] is True
    usuario = sistema.consultar_usuario_por_ra(ra)
    assert isbn not in usuario['livros_emprestados']

def test_devolucao_livro_nao_emprestado():
    """Testa a tentativa de devolver um livro que não foi emprestado pelo usuário."""
    sistema = SistemaBiblioteca()
    # PREPARAÇÃO
    isbn = "978-0321765723"
    ra = "171280"
    sistema.cadastrar_livro(titulo="Clean Code", autor="Robert C. Martin", isbn=isbn)
    sistema.cadastrar_usuario(nome="Enrico Alvarenga", ra=ra)

    # AÇÃO
    sucesso = sistema.realizar_devolucao(ra_usuario=ra, isbn_livro=isbn)

    # VERIFICAÇÃO
    assert sucesso is False

# --- NOVO TESTE PARA O CASO DE USO 5: CONSULTAS / RELATÓRIOS ---

def test_listar_livros_disponiveis():
    """Testa a listagem de livros disponíveis, incluindo um livro que foi emprestado."""
    sistema = SistemaBiblioteca()
    # PREPARAÇÃO
    isbn1 = "111-1111111111"
    isbn2 = "222-2222222222"
    isbn3 = "333-3333333333"
    ra = "171280"
    sistema.cadastrar_livro(titulo="Livro A", autor="Autor A", isbn=isbn1)
    sistema.cadastrar_livro(titulo="Livro B", autor="Autor B", isbn=isbn2)
    sistema.cadastrar_livro(titulo="Livro C (Emprestado)", autor="Autor C", isbn=isbn3)
    sistema.cadastrar_usuario(nome="Enrico Alvarenga", ra=ra)
    sistema.realizar_emprestimo(ra_usuario=ra, isbn_livro=isbn3)

    # AÇÃO
    livros_disponiveis = sistema.listar_livros_disponiveis()

    # VERIFICAÇÃO
    assert len(livros_disponiveis) == 2
    titulos_disponiveis = [livro['titulo'] for livro in livros_disponiveis]
    assert "Livro A" in titulos_disponiveis
    assert "Livro B" in titulos_disponiveis
    assert "Livro C (Emprestado)" not in titulos_disponiveis
