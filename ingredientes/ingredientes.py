import streamlit as st

class Ingredientes:

    def __init__(self, repository) -> None:
        self.repository = repository

    def buscar_listas(self):
        lista_mercados = self.repository.select_mercado()

        lista_ingredientes = self.repository.select_ingredientes()
        
        nome_id_mercados = []
        nome_id_ingredientes = []

        nome_mercados = []

        nome_ingredientes = []

        for mercado in lista_mercados:
            nome_id_mercados.append((mercado[0], mercado[1]))
            nome_mercados.append(mercado[1])
        
        for ingrediente in lista_ingredientes:

            nome_id_ingredientes.append((ingrediente[0], ingrediente[1]))
            nome_ingredientes.append(ingrediente[1])


        return nome_id_mercados, nome_mercados, nome_id_ingredientes, nome_ingredientes



    def pagina_compras(self):

        st.subheader('Lançar compra')

        nome_id_mercados, nome_mercados, nome_id_ingredientes, nome_ingredientes = self.buscar_listas()


        data = st.date_input('Data da compra', format='DD/MM/YYYY')

        mercado = st.selectbox('Mercado', nome_mercados, index=None)

        itens_comprados = st.text_input('Numero de itens comprados', value=0)

        for numero in range(int(itens_comprados)):

            nome = st.selectbox('Ingrediente', nome_ingredientes, key=f'compra_ing_{numero}', index=None)

            col1, col2 = st.columns()
                
            with col1:
                st.text_input('Marca', key=f'compra_marca_{numero}')
                st.text_input('Gramas ou Ml em cada embalagem', key=f'unidade_{numero}')

            with col2:
                st.text_input('Quantidade comprada', key=f'compra_quantidade_{numero}')
                st.text_input('Preço unitario', key=f'compra_preco_{numero}')

                

        if st.button('Lançar compra'):
            index = nome_mercados.index(mercado)
            id_mercado = nome_id_mercados[index][0]

            self.lancar_compra(data, itens_comprados, id_mercado, nome_id_ingredientes, nome_ingredientes)

            st.success('Compra registrada com sucesso!!')


    def lancar_compra(self, data, itens_comprados, id_mercado, nome_id_ingredientes, nome_ingredientes):
        

        for numero in range(int(itens_comprados)):
            nome = st.session_state[f'compra_ing_{numero}']
            marca = st.session_state[f'compra_marca_{numero}']
            quantidade = st.session_state[f'compra_quantidade_{numero}']
            preco = st.session_state[f'compra_preco_{numero}']
            custo_medida = float(preco)/int(quantidade)
            embalagem = st.session_state[f'unidade_{numero}']
            
            index = nome_ingredientes.index(nome)
            id_ingrediente = nome_id_ingredientes[index][0]
            
            self.repository.insert_compra_ingredientes(id_ingrediente, id_mercado, marca, preco, quantidade, data, custo_medida)
            self.repository.update_custo_ingrediente(custo_medida, id_ingrediente)


    def tela_precos(self):
            nome_id_mercados, nome_mercados, nome_id_ingredientes, nome_ingredientes = self.buscar_listas()

            ingrediente = st.selectbox('Ingrediente', nome_ingredientes, index=None)

            if st.button('Pesquiar'):
                self.pesquisar_preco()

    def pesquisar_preco(self):
        self.repository.select_precos