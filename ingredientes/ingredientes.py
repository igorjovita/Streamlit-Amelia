import streamlit as st
from babel.numbers import format_currency
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
        self.tela_compra()

        st.write('---')

        self.tela_precos()


    def tela_compra(self):
        
        st.subheader('Lançar compra')

        nome_id_mercados, nome_mercados, nome_id_ingredientes, nome_ingredientes = self.buscar_listas()


        data = st.date_input('Data da compra', format='DD/MM/YYYY')

        mercado = st.selectbox('Mercado', nome_mercados, index=None)

        itens_comprados = st.text_input('Numero de itens comprados', value=0)

        if itens_comprados != '0':

            for numero in range(int(itens_comprados)):

                nome = st.selectbox('Ingrediente', nome_ingredientes, key=f'compra_ing_{numero}', index=None)

                col1, col2 = st.columns(2)
                    
                with col1:
                    st.text_input('Marca', key=f'compra_marca_{numero}')
                    st.text_input('Gramas ou Ml em cada embalagem', key=f'unidade_{numero}', help='Se o produto for registrado em unidade ou caixa coloque 1 neste campo')

                with col2:
                    st.text_input('Quantidade comprada', key=f'compra_quantidade_{numero}')
                    st.text_input('Valor pago', key=f'compra_preco_{numero}')
                
                st.write('---')

                    

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
            embalagem = st.session_state[f'unidade_{numero}']
            
            custo_medida = float(preco)/(int(embalagem) * int(quantidade))
            
            index = nome_ingredientes.index(nome)
            id_ingrediente = nome_id_ingredientes[index][0]
            
            self.repository.insert_compra_ingredientes(id_ingrediente, id_mercado, marca, preco, quantidade, data, custo_medida, embalagem)
            self.repository.update_custo_ingrediente(custo_medida, id_ingrediente)


    def tela_precos(self):
            st.subheader('Historico de preços')
            _, _, nome_id_ingredientes, nome_ingredientes = self.buscar_listas()

            ingrediente = st.selectbox('Ingrediente', nome_ingredientes, index=None)

            if st.button('Pesquisar'):
                
                id_ingrediente = nome_id_ingredientes[nome_ingredientes.index(ingrediente)][0]
                
                select_preco = self.pesquisar_preco(id_ingrediente)

                st.write(id_ingrediente)

                self.exibir_precos(select_preco)

    def pesquisar_preco(self, id_ingrediente):
        return self.repository.select_preco_ingrediente(id_ingrediente)

    def exibir_precos(self, select_preco):
        for item in select_preco:
            marca = item[1]
            quantidade = item[2]
            embalagem = item[3]
            unidade = item[4]
            preco = item[5]
            mercado = item[6]


            if int(quantidade) > 1 and item[0] != 'Maracujá':
                valor_unitario = float(preco)/int(quantidade)

            else:
                valor_unitario = float(preco)

            valor_unitario = format_currency(valor_unitario, 'BRL', locale='pt_BR')

            if unidade == 'caixa' or unidade == 'Unidade':

                st.text(f'{int(quantidade)} {unidade} por {valor_unitario} cada \nda marca {marca} no mercado {mercado}')
            
            else:

                st.text(f'{int(quantidade)} unidade de {embalagem} {unidade} por {valor_unitario} cada \nda marca {marca} no mercado {mercado}')