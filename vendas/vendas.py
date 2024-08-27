import streamlit as st
import pandas as pd
from babel.numbers import format_currency

class Vendas:

    def __init__(self, repository) -> None:
        self.repository = repository

    def pagina_vendas(self):
        st.subheader('Vendas')
        self.historico_vendas()
        
        st.write('---')
        
        st.subheader('Lançar Venda')
        self.formulario_vendas()
    
    
    def historico_vendas(self):
        historico = self.repository.select_historico_vendas()
        df = pd.DataFrame(historico, columns=['Data', 'Condominio', 'Quantidade', 'Faturamento', 'Lucro'])

        df['Data'] = pd.to_datetime(df['Data'])
        df['Data'] = df['Data'].dt.strftime('%d/%m/%Y')
        df['Faturamento'] = df['Faturamento'].apply(lambda x:format_currency(x, 'BRL', locale='pt_BR'))
        df['Lucro'] = df['Lucro'].apply(lambda x:format_currency(x, 'BRL', locale='pt_BR'))

        st.data_editor(df, hide_index=True)

    
    def formulario_vendas(self):

        select_info_produto, lista_nome_produto = self.buscar_receita()
        select_condominio, lista_nome_condominio = self.buscar_condominio()

        data = st.date_input('Data', format='DD/MM/YYYY')

        escolha_condominio = st.selectbox('Condominio', lista_nome_condominio, index=None)

        produtos_diferentes = st.text_input('Quantos produtos diferentes foram vendidos', value=0)
        
        if produtos_diferentes != '0':
            with st.form('Formulario Venda'):
                for i in range (int(produtos_diferentes)):
                
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.selectbox('Produto', lista_nome_produto, index=None, key=f'produto_vendido {i}')
                        
                    with col2:
                        st.text_input('Quantidade', key=f'quantidade_vendida {i}')

                    with col3:
                        st.text_input('Valor da venda', key=f'valor_venda {i}')

                if st.form_submit_button('Lançar venda'):
                    
                    id_condominio = select_condominio[lista_nome_condominio.index(escolha_condominio)][0]
                    
                    self.lancar_venda(id_condominio, select_info_produto, lista_nome_produto, produtos_diferentes, data)

                    st.success('Venda registrada com sucesso')



    def buscar_receita(self):
        select_info_produto = self.repository.select_nome_receitas()

        lista_nome_produto = [receita[1] for receita in select_info_produto]

        return select_info_produto, lista_nome_produto
    
    def buscar_condominio(self):

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

            self.repository.insert_vendas(id_produto, id_condominio, quantidade_vendida, valor, custo, float(valor) - float(custo), data)
        
            lista_id_lote = self.obter_lote_e_quantidade(id_produto, quantidade_vendida)

            for info in lista_id_lote:
                self.insert_estoque_produto(id_produto, info[0], info[1], custo)

    
    def obter_lote_e_quantidade(self, id_produto, quantidade_vendida):
        
        lista_id_lote = []

        select_quantidade_lote = self.repository.select_lote_produto(id_produto)

        for lote in select_quantidade_lote:
            quantidade_disponivel_lote = int(lote[1])
            
            if quantidade_disponivel_lote > 0:
                
                if quantidade_disponivel_lote >= quantidade_vendida:
                    lista_id_lote.append((lote[0], quantidade_vendida))
                    break
                
                else:
                    lista_id_lote.append((lote[0], quantidade_disponivel_lote))
                    quantidade_vendida -= quantidade_disponivel_lote 
            

        
        return lista_id_lote


    def insert_estoque_produto(self, id_produto, id_lote, quantidade, custo):
        self.repository.insert_estoque_produto(id_produto, id_lote, 'SAIDA', quantidade, custo)


