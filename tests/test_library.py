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
