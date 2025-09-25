# app.py
from flask import Flask, render_template
from src.library import SistemaBiblioteca

# Cria a aplicação Flask
app = Flask(__name__)

# Cria uma instância única do nosso sistema de biblioteca
# (Por enquanto, os dados são em memória. O banco de dados virá depois)
biblioteca = SistemaBiblioteca()

# --- DADOS DE EXEMPLO PARA COMEÇAR ---
# Vamos cadastrar alguns livros e usuários para popular o sistema
biblioteca.cadastrar_livro(titulo="Clean Code", autor="Robert C. Martin", isbn="978-0132350884")
biblioteca.cadastrar_livro(titulo="O Programador Pragmático", autor="Andrew Hunt", isbn="978-0201616224")
biblioteca.cadastrar_livro(titulo="Engenharia de Software", autor="Ian Sommerville", isbn="978-8576059814")
biblioteca.cadastrar_usuario(nome="Enrico Alvarenga", ra="171280")
biblioteca.cadastrar_usuario(nome="Eduardo Cipolaro", ra="168797")
# ------------------------------------

# Define a rota principal (página inicial)
@app.route('/')
def home():
    """Renderiza a página inicial da aplicação."""
    # O método render_template busca por arquivos na pasta 'templates'
    return render_template('index.html')

# (Futuramente, adicionaremos mais rotas aqui, como /livros, /usuarios, etc.)
