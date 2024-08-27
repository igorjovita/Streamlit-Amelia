import streamlit as st
import pandas as pd

class Estoque:

    def __init__(self, repository) -> None:
        self.repository = repository
        
    
    def pagina_estoque(self):
        st.subheader('Estoque')
        self.pagina_pesquisar_estoque()

        st.write('---')

        self.pagina_lancar_producao()
        

    def pagina_lancar_producao(self):

        st.subheader('Lançar Produção')

        select_receitas = self.repository.select_nome_receitas()
        lista_receita = [receita[1] for receita in select_receitas]

        data = st.date_input('Data da produção', format='DD/MM/YYYY')
        
        receita = st.selectbox('Receita', lista_receita)
        
        
        rendimento = st.text_input('Rendimento da producao')

        if st.button('Lançar no sistema'):

            custo_total, custo_unitario = self.preparar_dados_producao(lista_receita, select_receitas, rendimento, data, receita)
            

            st.warning(f'Custo Total : {custo_total} ')
            st.warning(f'Custo Unitario : {custo_unitario}')
            st.success('Produção lançada com sucesso!')

    
    def preparar_dados_producao(self, lista_receita, select_receitas, rendimento, data, receita):

        index = lista_receita.index(receita)
        id_produto = select_receitas[index][0]

        custo_total = self.repository.select_custo_receita_produto(id_produto)[0][0]
        custo_unitario = float(custo_total)/int(rendimento)
        
        st.write(custo_total)
        st.write(custo_unitario)

        id_lote = int(self.repository.select_ultimo_id_lote(id_produto)[0]) + 1
        
        self.registrar_producao(id_produto, id_lote, data, rendimento, custo_total, custo_unitario)

        return custo_total, custo_unitario
            


    def registrar_producao(self, id_produto, id_lote, data, rendimento, custo_total, custo_unitario):
        self.repository.insert_registro_producao(id_produto, id_lote, data, rendimento, custo_total)
        self.repository.insert_estoque_produto( id_produto, id_lote, 'ENTRADA', rendimento, custo_unitario)
        self.repository.update_custos_receita(custo_total, custo_unitario, id_produto)

    
    def pagina_pesquisar_estoque(self):

        st.subheader('Quantidade no estoque')

        st.text('Produtos')

        select_quantidade_produtos = self.repository.select_quantidade_estoque()

        df = pd.DataFrame(select_quantidade_produtos, columns=['Lote', 'Nome', 'Quantidade', 'Custo', 'Produção', 'Validade'])
        df['Produção'] = pd.to_datetime(df['Produção'])
        df['Produção'] = df['Produção'].dt.strftime('%d/%m/%Y')

        df['Validade'] = pd.to_datetime(df['Validade'])
        df['Validade'] = df['Validade'].dt.strftime('%d/%m/%Y')

        df = df[df['Quantidade'] > 0]            

        st.table(df)

        

        




