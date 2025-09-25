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
    isbn = "978-0321765723"
    ra = "171280"
    sistema.cadastrar_livro(titulo="Clean Code", autor="Robert C. Martin", isbn=isbn)
    sistema.cadastrar_usuario(nome="Enrico Alvarenga", ra=ra)
    sucesso = sistema.realizar_emprestimo(ra_usuario=ra, isbn_livro=isbn)
    assert sucesso is True
    livro = sistema.consultar_livro_por_isbn(isbn)
    assert livro['disponivel'] is False
    usuario = sistema.consultar_usuario_por_ra(ra)
    assert isbn in usuario['livros_emprestados']

def test_emprestimo_livro_indisponivel():
    """Testa a tentativa de emprestar um livro que já foi emprestado."""
    sistema = SistemaBiblioteca()
    isbn = "978-0321765723"
    ra1 = "171280"
    ra2 = "168797"
    sistema.cadastrar_livro(titulo="Clean Code", autor="Robert C. Martin", isbn=isbn)
    sistema.cadastrar_usuario(nome="Enrico Alvarenga", ra=ra1)
    sistema.cadastrar_usuario(nome="Eduardo Cipolaro", ra=ra2)
    sistema.realizar_emprestimo(ra_usuario=ra1, isbn_livro=isbn)
    sucesso_segunda_tentativa = sistema.realizar_emprestimo(ra_usuario=ra2, isbn_livro=isbn)
    assert sucesso_segunda_tentativa is False

def test_emprestimo_livro_inexistente():
    """Testa a tentativa de emprestar um livro que não existe no acervo."""
    sistema = SistemaBiblioteca()
    ra = "171280"
    sistema.cadastrar_usuario(nome="Enrico Alvarenga", ra=ra)
    sucesso = sistema.realizar_emprestimo(ra_usuario=ra, isbn_livro="999-9999999999")
    assert sucesso is False

# --- TESTES PARA O CASO DE USO 4: DEVOLUÇÃO ---
def test_devolucao_livro_sucesso():
    """Testa o 'caminho feliz' da devolução de um livro."""
    sistema = SistemaBiblioteca()
    isbn = "978-0321765723"
    ra = "171280"
    sistema.cadastrar_livro(titulo="Clean Code", autor="Robert C. Martin", isbn=isbn)
    sistema.cadastrar_usuario(nome="Enrico Alvarenga", ra=ra)
    sistema.realizar_emprestimo(ra_usuario=ra, isbn_livro=isbn)
    sucesso = sistema.realizar_devolucao(ra_usuario=ra, isbn_livro=isbn)
    assert sucesso is True
    livro = sistema.consultar_livro_por_isbn(isbn)
    assert livro['disponivel'] is True
    usuario = sistema.consultar_usuario_por_ra(ra)
    assert isbn not in usuario['livros_emprestados']

def test_devolucao_livro_nao_emprestado():
    """Testa a tentativa de devolver um livro que não foi emprestado pelo usuário."""
    sistema = SistemaBiblioteca()
    isbn = "978-0321765723"
    ra = "171280"
    sistema.cadastrar_livro(titulo="Clean Code", autor="Robert C. Martin", isbn=isbn)
    sistema.cadastrar_usuario(nome="Enrico Alvarenga", ra=ra)
    sucesso = sistema.realizar_devolucao(ra_usuario=ra, isbn_livro=isbn)
    assert sucesso is False

# --- TESTES PARA CONSULTAS / RELATÓRIOS ---
def test_listar_livros_disponiveis():
    """Testa a listagem de livros disponíveis."""
    sistema = SistemaBiblioteca()
    isbn1, isbn2, isbn3 = "111", "222", "333"
    ra = "171280"
    sistema.cadastrar_livro(titulo="Livro A", autor="Autor A", isbn=isbn1)
    sistema.cadastrar_livro(titulo="Livro B", autor="Autor B", isbn=isbn2)
    sistema.cadastrar_livro(titulo="Livro C (Emprestado)", autor="Autor C", isbn=isbn3)
    sistema.cadastrar_usuario(nome="Enrico Alvarenga", ra=ra)
    sistema.realizar_emprestimo(ra_usuario=ra, isbn_livro=isbn3)
    livros_disponiveis = sistema.listar_livros_disponiveis()
    assert len(livros_disponiveis) == 2
    titulos_disponiveis = [livro['titulo'] for livro in livros_disponiveis]
    assert "Livro A" in titulos_disponiveis
    assert "Livro C (Emprestado)" not in titulos_disponiveis

def test_consultar_livros_de_um_usuario():
    """Testa a consulta de livros emprestados por um usuário específico."""
    sistema = SistemaBiblioteca()
    isbn1, isbn2, isbn3 = "111", "222", "333"
    ra = "171280"
    sistema.cadastrar_livro(titulo="Livro A", autor="Autor A", isbn=isbn1)
    sistema.cadastrar_livro(titulo="Livro B", autor="Autor B", isbn=isbn2)
    sistema.cadastrar_livro(titulo="Livro C", autor="Autor C", isbn=isbn3)
    sistema.cadastrar_usuario(nome="Enrico Alvarenga", ra=ra)
    sistema.realizar_emprestimo(ra_usuario=ra, isbn_livro=isbn1)
    sistema.realizar_emprestimo(ra_usuario=ra, isbn_livro=isbn2)
    livros_do_usuario = sistema.consultar_livros_do_usuario(ra_usuario=ra)
    assert len(livros_do_usuario) == 2
    titulos_emprestados = [livro['titulo'] for livro in livros_do_usuario]
    assert "Livro A" in titulos_emprestados
    assert "Livro C" not in titulos_emprestados

def test_consultar_livros_de_usuario_inexistente():
    """Testa a consulta de livros para um usuário que não existe."""
    sistema = SistemaBiblioteca()
    livros_do_usuario = sistema.consultar_livros_do_usuario(ra_usuario="999999")
    assert livros_do_usuario is None

# --- NOVOS TESTES PARA LISTAGENS GERAIS ---

def test_listar_todos_os_livros():
    """Testa a listagem de todos os livros, disponíveis ou não."""
    sistema = SistemaBiblioteca()
    sistema.cadastrar_livro(titulo="Livro A", autor="Autor A", isbn="111")
    sistema.cadastrar_livro(titulo="Livro B", autor="Autor B", isbn="222")
    
    livros = sistema.listar_todos_os_livros()
    assert len(livros) == 2

def test_listar_todos_os_usuarios():
    """Testa a listagem de todos os usuários."""
    sistema = SistemaBiblioteca()
    sistema.cadastrar_usuario(nome="Enrico Alvarenga", ra="171280")
    sistema.cadastrar_usuario(nome="Eduardo Cipolaro", ra="168797")
    
    usuarios = sistema.listar_todos_os_usuarios()
    assert len(usuarios) == 2
    nomes = [user['nome'] for user in usuarios]
    assert "Enrico Alvarenga" in nomes
    assert "Eduardo Cipolaro" in nomes
