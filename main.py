import streamlit as st
from database import DataBaseMysql
from ingredientes import Ingredientes
from repository import Repository
from estoque import Estoque
from cadastro import Cadastros
from receitas import Receitas
from vendas import Vendas
from agendar import Agendar

st.set_page_config(layout='wide')

st.write("""
# Sistema de controle de vendas
""")

database_mysql = DataBaseMysql()
repository = Repository(database_mysql)

ingredientes = Ingredientes(repository)

cadastro = Cadastros(repository)

estoque = Estoque(repository)

receitas = Receitas(repository)

vendas = Vendas(repository)

agendamento = Agendar(repository)

st.sidebar.write( """
## Amelia Doces Gourmet
""")

escolha = st.sidebar.radio('Paginas', ['Vendas', 'Compras', 'Agendamentos', 'Cadastros', 'Receitas', 'Estoque'], label_visibility='hidden')

if escolha == 'Compras':
    ingredientes.pagina_compras()

if escolha == 'Estoque':
    estoque.pagina_estoque()

if escolha == 'Agendamentos':
    agendamento.pagina_agendar()

if escolha == 'Cadastros':
    cadastro.pagina_cadastro()

if escolha == 'Receitas':
    receitas.pagina_receitas()

if escolha == 'Vendas':
    vendas.pagina_vendas()

