from src.library import SistemaBiblioteca


def test_status_inicial_do_sistema():
    """Testa se o sistema é inicializado corretamente."""
    sistema = SistemaBiblioteca()
    assert sistema.status() == "Sistema de Biblioteca Online!"


def test_cadastrar_usuario():
    """Testa o Caso de Uso 2: Cadastrar um novo usuário."""
    sistema = SistemaBiblioteca()
    sucesso = sistema.cadastrar_usuario(nome="Eduardo Cipolaro", ra="168797")
    
    assert sucesso is True
    
    usuario = sistema.consultar_usuario_por_ra("168797")
    assert usuario is not None
    assert usuario['nome'] == "Eduardo Cipolaro"
