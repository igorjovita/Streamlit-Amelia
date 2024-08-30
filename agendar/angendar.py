import streamlit as st


class Agendar:

    def __init__(self, repository) -> None:
        self.repository = repository

    def pagina_agendar(self):
        
        st.multiselect('Escolha os dias', options=['01', '02', '03', '04', '05'])