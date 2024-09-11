import streamlit as st
import datetime
import pandas as pd
import locale
import mysql.connector
from mysql.connector import Error
class Agendar:

    def __init__(self, repository) -> None:
        self.repository = repository

    def pagina_agendar(self):

        st.subheader('Agendamentos')
        self.buscar_agendamentos()

        st.write('---')

        st.subheader('Agendar')

        self.agendar_condominio()
        
    
    def agendar_condominio(self):
        select_condominio, lista_nome_condominio =  self.buscar_condominio()
        
        dias_agendar = st.multiselect('Escolha os dias', options=['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31'])
        
        mes = st.selectbox('Escolha o mês', options=['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'], index=None)

        ano = st.selectbox('Escolha o ano', options=['2024', '2025', '2026'], index=None)

        condominio = st.selectbox('Condominio', lista_nome_condominio, index=None)

        if st.button('Agendar'):
            id_condominio = select_condominio[lista_nome_condominio.index(condominio)][0]

            for dia in dias_agendar:
                data = datetime.date(int(ano), int(mes), int(dia))
                dia_da_semana = data.strftime('%A')
                dia_da_semana_br = self.converte_dia(dia_da_semana)
                
                try:
                    self.repository.insert_agendamento_condominio(data, dia_da_semana_br, id_condominio)
                except mysql.connector.Error as err:
                    if err.errno == 1062:
                        print("Erro: Entrada duplicada.")
                    else:
                        print(f"Erro: {err}")
            st.success('Datas agendadas com sucesso!')

    
    def converte_dia(self, dia_da_semana):
        dicionario_dias = {
            'Monday': 'Segunda-Feira',
            'Tuesday': 'Terça-Feira',
            'Wednesday': 'Quarta-Feira',
            'Thursday': 'Quinta-Feira',
            'Friday': 'Sexta-Feira',
            'Saturday': 'Sábado',
            'Sunday': 'Domingo'}
        
        return dicionario_dias.get(dia_da_semana, 'Dia Invalido')




    def buscar_condominio(self):

        select_condominio = self.repository.select_condominio()

        lista_nome_condominio = [condominio[1] for condominio in select_condominio]

        return select_condominio, lista_nome_condominio
        
    
    def buscar_agendamentos(self):
        select_agendamentos = self.repository.select_agendamento_condominio()

        df = pd.DataFrame(select_agendamentos, columns=['Data', 'Dia', 'Condominio'])

        df['Data'] = pd.to_datetime(df['Data'])

        df['Data'] = df['Data'].dt.strftime('%d/%m/%Y')


        st.dataframe(df, hide_index=True, use_container_width=True)