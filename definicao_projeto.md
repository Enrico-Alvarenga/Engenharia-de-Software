### **Definição de Tecnologia e Arquitetura do Projeto**

**Projeto:** Sistema de Controle de Biblioteca  
**Disciplina:** Engenharia de Software  
**Integrantes:**
* Enrico Alvarenga - RA: 171.280
* Eduardo Cipolaro - RA: 168.797

---

#### **1. Stack de Tecnologias**

A stack de tecnologias selecionada para o desenvolvimento do projeto visa utilizar ferramentas modernas, eficientes e amplamente adotadas no mercado, com foco na simplicidade e robustez para o escopo acadêmico.

* **Linguagem de Backend:** **Python (versão 3.11+)**
    * Escolhido por sua sintaxe clara, vasta biblioteca padrão e forte ecossistema para desenvolvimento web e de testes.

* **Framework Web:** **Flask**
    * Um micro-framework leve e flexível, ideal para iniciar o desenvolvimento da camada web. Ele nos permitirá acoplar a interface às regras de negócio já desenvolvidas (`SistemaBiblioteca`) de forma rápida e controlada.

* **Banco de Dados:**
    * **Desenvolvimento:** **SQLite**
        * Um banco de dados serverless, baseado em arquivo e integrado nativamente ao Python. É perfeito para o desenvolvimento local por não exigir configuração de servidor.
    * **Produção:** O projeto será estruturado para ser compatível com bancos de dados mais robustos como **PostgreSQL** ou **MySQL** no ambiente de produção (ex: DigitalOcean).

* **Tecnologia de Frontend:**
    * **Estrutura e Estilo:** **HTML5** e **CSS3** para a estruturação e estilização das páginas.
    * **Interatividade:** **JavaScript (Vanilla)** para pequenas interatividades no lado do cliente, se necessário.
    * **Template Engine:** **Jinja2** (integrado ao Flask) para renderizar páginas HTML dinamicamente com os dados do backend.

* **Servidor de Aplicação (Produção):** **Gunicorn**
    * Um servidor WSGI padrão de mercado para servir aplicações Python/Flask em ambientes de produção, garantindo performance e estabilidade.

* **Testes e Integração Contínua:**
    * **Testes Automatizados:** **Pytest** para a criação e execução de testes unitários.
    * **CI/CD:** **GitHub Actions** para automação da pipeline de testes, garantindo a qualidade e a integridade do código a cada `commit`.

---

#### **2. Arquitetura e Estrutura de Diretórios**

**Arquitetura do Projeto**

A arquitetura do sistema será baseada no padrão **MVC (Model-View-Controller)**, uma abordagem clássica e eficaz para organizar aplicações web.

* **Model (Modelo):** Representa os dados e a lógica de negócio. Em nosso projeto, o "Modelo" é encapsulado pela classe `SistemaBiblioteca` (que futuramente será adaptada para interagir com o banco de dados) e pelas estruturas de dados de livros e usuários.
* **View (Visão):** É a camada de apresentação, responsável por exibir os dados ao usuário. Em nosso caso, serão os arquivos **HTML** renderizados pelo template engine **Jinja2**.
* **Controller (Controlador):** Atua como o intermediário entre o Modelo e a Visão. Ele recebe as requisições do usuário (via navegador), aciona os métodos apropriados no Modelo (ex: `realizar_emprestimo()`) e seleciona qual Visão será exibida como resposta. Esta camada será implementada pelas funções (rotas) em nosso arquivo principal do **Flask** (ex: `app.py`).

**Estrutura de Diretórios**

A estrutura de pastas foi planejada para separar claramente as responsabilidades, seguindo as melhores práticas de projetos Flask:

* **`Engenharia-de-Software/`**
    * **`.github/`**: Configurações do GitHub Actions (CI/CD)
        * **`workflows/`**
            * `ci-cd.yml`
    * **`src/`**: Lógica de negócio principal (nosso "Modelo")
        * `library.py`
    * **`tests/`**: Testes automatizados com Pytest
        * `test_library.py`
    * **`templates/`**: Arquivos HTML (a "Visão")
        * `index.html`
        * `livros.html`
    * **`static/`**: Arquivos estáticos (CSS, JavaScript, imagens)
        * **`css/`**
            * `style.css`
    * `app.py`: Arquivo principal do Flask (o "Controlador")
    * `requirements.txt`: Lista de dependências Python do projeto
    * `README.md`: Documentação geral do projeto
