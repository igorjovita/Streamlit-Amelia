import streamlit as st
import pandas as pd
from babel.numbers import format_currency

class Vendas:

    def __init__(self, repository) -> None:
        self.repository = repository

    def pagina_vendas(self):
        # Exibição de itens na tela de vendas

        st.subheader('Vendas')
        self.historico_vendas()
        
        st.write('---')
        
        st.subheader('Lançar Venda')
        self.formulario_vendas()

        st.write('---')

        st.subheader('Editar Registros')

        self.mostrar_ultimas_vendas()
    
    
    def historico_vendas(self):
        # Exibe uma tabela com o historico de vendas contendo data, nome do lugar, numero de vendas, faturamento e lucro

        historico = self.repository.select_historico_vendas()
        df = pd.DataFrame(historico, columns=['Data', 'Condominio', 'Vendas', 'Faturamento', 'Lucro'])

        df['Data'] = pd.to_datetime(df['Data'])
        df['Data'] = df['Data'].dt.strftime('%d/%m')
        df['Faturamento'] = df['Faturamento'].apply(lambda x:format_currency(x, 'BRL', locale='pt_BR'))
        df['Lucro'] = df['Lucro'].apply(lambda x:format_currency(x, 'BRL', locale='pt_BR'))

        st.dataframe(df, hide_index=True, use_container_width=True)

    
    def formulario_vendas(self):

        # Exibe os campos para o usuario lançar as vendas no sistema

        st.write('''<style>
        [data-testid="column"] {
            width: calc(33.3333% - 1rem) !important;
            flex: 1 1 calc(33.3333% - 1rem) !important;
            min-width: calc(33% - 1rem) !important;
        }

        </style>''', unsafe_allow_html=True)

        select_info_produto, lista_nome_produto = self.buscar_receita()
        select_condominio, lista_nome_condominio = self.buscar_condominio()

        data = st.date_input('Data', format='DD/MM/YYYY')

        escolha_condominio = st.selectbox('Condominio', lista_nome_condominio, index=None)

        produtos_diferentes = st.text_input('Quantos produtos diferentes foram vendidos', value=0, key='produtos_diferentes')
        
        if produtos_diferentes != '0':
            with st.form('Formulario Venda'):
                for i in range (int(produtos_diferentes)):
                    
                    st.selectbox('Produto', lista_nome_produto, index=None, key=f'produto_vendido {i}')
                   
                    col1, col2 = st.columns(2)
    
                    with col1:
                        st.text_input('Quantidade', key=f'quantidade_vendida {i}')

                    with col2:
                        st.text_input('Valor da venda', key=f'valor_venda {i}')
                    
                    st.write('---')

                if st.form_submit_button('Lançar venda'):
                    
                    id_condominio = select_condominio[lista_nome_condominio.index(escolha_condominio)][0]
                    
                    self.lancar_venda(id_condominio, select_info_produto, lista_nome_produto, produtos_diferentes, data)

                    st.success('Venda registrada com sucesso')

                    self.resetar_formulario()

    
    def resetar_formulario(self):
        
        # Reseta o valor do campo de produtos diferentes pra 0 consequentemente resetando os demais campos

        st.session_state['produtos_diferentes'] = 0


    def buscar_receita(self):

        # Busca no sistema os nomes das receitas e retorna uma lista dos nomes e das informações

        select_info_produto = self.repository.select_nome_receitas()

        lista_nome_produto = [receita[1] for receita in select_info_produto]

        return select_info_produto, lista_nome_produto
    
    def buscar_condominio(self):

        # Busca no sistema os condominios cadastrados e retorna uma lista dos nomes e das informações

        select_condominio = self.repository.select_condominio()

        lista_nome_condominio = [condominio[1] for condominio in select_condominio]

        return select_condominio, lista_nome_condominio

        
    def lancar_venda(self, id_condominio, select_info_produto, lista_nome_produto, produtos_diferentes, data):

        for i in range(int(produtos_diferentes)):

            produto = st.session_state[f'produto_vendido {i}']
            quantidade_vendida = int(st.session_state[f'quantidade_vendida {i}'])
            valor = st.session_state[f'valor_venda {i}']
            index_produto = lista_nome_produto.index(produto)
            id_produto = select_info_produto[index_produto][0]
            custo = float(select_info_produto[index_produto][2]) * quantidade_vendida

            if valor == '':
                valor = 0

            id_venda = self.repository.insert_vendas(id_produto, id_condominio, quantidade_vendida, valor, custo, float(valor) - float(custo), data)
        
            self.insert_estoque_produto(id_produto, quantidade_vendida, custo, data, id_venda)


    def insert_estoque_produto(self, id_produto, quantidade, custo, data, id_venda):
        self.repository.insert_estoque_produto(id_produto, 'SAIDA', quantidade, custo, data, id_venda)
    


    def mostrar_ultimas_vendas(self):

        select_ultimas_vendas = self.repository.select_ultimas_vendas()

        if 'df_status' not in st.session_state:
            st.session_state.df_status = None
       
        df = pd.DataFrame(select_ultimas_vendas, columns=['Id', 'Data', 'Lugar', 'Produto', 'Qtd', 'Preço'])
        lista_id = df['Id'].to_list()
        
        df = df.drop(columns='Id')
        
        df.insert(0, '#', [False] * len(df))

        st.session_state.df_status = st.data_editor(df, hide_index=True)

        if len(st.session_state.df_status.loc[st.session_state.df_status['#']]) > 0:
            lista_datas = st.session_state.df_status.loc[st.session_state.df_status['#'], 'Data'].to_list()
            lista_lugar = st.session_state.df_status.loc[st.session_state.df_status['#'], 'Lugar'].to_list()
            lista_produtos = st.session_state.df_status.loc[st.session_state.df_status['#'], 'Produto'].to_list()
            lista_quantidades = st.session_state.df_status.loc[st.session_state.df_status['#'], 'Qtd'].to_list()
            lista_preco = st.session_state.df_status.loc[st.session_state.df_status['#'], 'Preço'].to_list()
            index_selecionado = st.session_state.df_status.loc[st.session_state.df_status['#']].index.to_list()
            select_info_produto, lista_nome_produto = self.buscar_receita()
            select_condominio, lista_nome_condominio = self.buscar_condominio()

            contador = 0
            for data, lugar,  nome_produto, quantidade, preco, index in zip(lista_datas, lista_lugar, lista_produtos, lista_quantidades, lista_preco, index_selecionado):
                contador += 1
                st.write(lista_id[index])
                index_produto = lista_nome_produto.index(nome_produto)
                index_lugar = lista_nome_condominio.index(lugar)

                st.date_input('Data', value=data, key=f'data_editar{contador}')
                
                st.selectbox('Lugar', lista_nome_condominio, index=index_lugar, key=f'lugar_editar{contador}')

                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.selectbox('Produto', lista_nome_produto, index=index_produto, key=f'produto_editar{contador}')
                
                with col2:
                    st.text_input('Quantidade', value=quantidade, key=f'quantidade_editar{contador}')
                
                with col3:
                    st.text_input('Preco', value=preco, key=f'preco_editar{contador}')
                
                st.text_input('Id', lista_id[index], key=f'id {contador}', disabled=True)

                st.write('---')

            coluna1, coluna2 = st.columns(2)

            with coluna1:
                if st.button('Exluir'):
                    
                    for i in range(contador):
                        id_venda = st.session_state[f'id {i + 1}']

                        self.repository.detele_venda(id_venda)
                        self.repository.delete_estoque_produtos(id_venda)

                    st.success('Dados excluidos com sucesso!')

            with coluna2:
                if st.button('Atualizar'):

                    for i in range(contador):
                        data_editada = st.session_state[f'data_editar{i + 1}']
                        produto_editado = st.session_state[f'produto_editar{i + 1}']
                        quantidade_editada = st.session_state[f'quantidade_editar{i + 1}']
                        preco_editado = st.session_state[f'preco_editar{i + 1}']
                        id_venda = st.session_state[f'id {i + 1}']
                        id_produto = select_info_produto[lista_produtos.index(produto_editado)][0]
                        custo = float(select_info_produto[index_produto][2]) * int(quantidade_editada)
                        lucro = float(preco_editado) - float(custo)
                        st.write(produto_editado)
                        st.write(select_info_produto)
                        st.write(lista_produtos.index(produto_editado))
                        st.write(id_produto)
                        #self.repository.update_venda(data_editada, id_produto, quantidade_editada, preco_editado, custo, lucro, id_venda)
                        #self.repository.update_estoque_produtos(id_produto, quantidade, data, custo, id_venda)

                    st.success('Dados alterados com sucesso')


