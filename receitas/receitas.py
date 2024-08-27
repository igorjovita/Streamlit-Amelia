import streamlit as st
import pandas as pd


class Receitas:

    def __init__(self, repository) -> None:
        self.repository = repository

    def pagina_receitas(self):
        st.subheader('Receitas')

        select_receitas = self.repository.select_receitas()

        lista_receitas = []

        for receita in select_receitas:
            if receita[0] not in lista_receitas:
                lista_receitas.append(receita[0])
        
        receita_escolhida = st.selectbox('Escolha a receita', lista_receitas, index=None)

        if st.button('Selecionar'):
            st.write('')
            st.write('')
            st.text(receita_escolhida)
            id_produto = ''
            for item in select_receitas:
                if receita_escolhida == item[0]:
                    id_produto = item[4]
                    st.write(f'- {item[1]} - {int(item[2])} {item[3]}')
            
            st.write('Modo de Preparo')

            try:
                select_modo_preparo = self.repository.select_modo_preparo(id_produto)[0]

                st.write(select_modo_preparo[0])

                st.write(f'Rende {select_modo_preparo[1]} unidades')

            except:
                st.write('Modo de Preparo nao informado, receita incompleta')