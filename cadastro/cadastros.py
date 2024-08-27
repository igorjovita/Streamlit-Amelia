import streamlit as st


class Cadastros:

    def __init__(self, repository) -> None:
        self.repository = repository


    def pagina_cadastro(self):

        st.header('Cadastros')

        self.cadastro_de_ingrediente()

        st.write('---')

        self.cadastro_de_mercado()

        st.write('---')
        
        self.cadastro_de_receita()

        st.write('---')
        
        self.cadastro_condominio()


    def cadastro_de_ingrediente(self):

        st.subheader('Cadastro de Ingredientes')

        nome_ingrediente = st.text_input('Nome do ingrediente')
        medida_ingrediente = st.selectbox('Selecione a unidade de medida', ['g', 'Kg', 'ml', 'L', 'Unidade', 'caixa'], index=None)

        if st.button('Cadastrar ingrediente'):
            self.insert_ingrediente(nome_ingrediente, medida_ingrediente)



    def insert_ingrediente(self,nome_ingrediente, medida_ingrediente):

        try:
            self.repository.insert_ingrediente(nome_ingrediente, medida_ingrediente)
            return st.success('Ingrediente cadastrado com sucesso!')

        except KeyError as e:
            return st.error(f'Produto Não Cadastrado {e}')
        

    def cadastro_de_mercado(self):
         
         st.subheader('Cadastro de Mercado')
         
         nome_mercado = st.text_input('Nome do Mercado')

         if st.button('Cadastrar mercado'):
            try:
                self.repository.insert_mercado(nome_mercado)
                return st.success('Mercado Cadastrado')
            
            except KeyError as e:
                return st.error(f'Mercado Não Cadastrado {e}')
            
    def inicializar_session_state(self):

        if 'ingredientes_formulario' not in st.session_state:
            st.session_state.ingredientes_formulario = False
            
    def cadastro_de_receita(self):

        self.inicializar_session_state()

        st.subheader('Cadastro de Receitas')

        nome_receita = st.text_input('Nome da receita', key='nome_da_receita')
        numero_ingredientes = int(st.text_input('Numero de ingredientes', value=0))

        if st.button('Cadastrar receita'):
            st.session_state.ingredientes_formulario = True
           
        
        if st.session_state.ingredientes_formulario:

            self.formulario_receita(numero_ingredientes)

    def formulario_receita(self, numero_ingredientes):

        select_ingredientes = self.repository.select_ingredientes()
        lista_ingredientes = [ingrediente[1] for ingrediente in select_ingredientes]

        with st.form('Formulario'):
            col1, col2 = st.columns(2)
            for numero in range(numero_ingredientes):
                with col1:
                    ingrediente = st.selectbox(f'Ingrediente {numero + 1}', lista_ingredientes, index=None, key=f'ingrediente_{numero}')

                with col2:
                    quantidade = st.text_input(f'Quantidade ingrediente {numero + 1}', key=f'quantidade {numero}')
            
            modo_preparo = st.text_area('Modo de preparo')
            rendimento = st.text_input('Rendimento da receita')

            if st.form_submit_button('Finalizar cadastro'):
                self.insercao_receita(numero_ingredientes, select_ingredientes, lista_ingredientes, modo_preparo, rendimento)
                    

    def insercao_receita(self, numero_ingredientes, select_ingredientes, lista_ingredientes, modo_preparo, rendimento):
        id_produto = self.repository.insert_produto(st.session_state['nome_da_receita'])
        for numero in range(numero_ingredientes):
            nome_ingrediente = st.session_state[f'ingrediente_{numero}']
            quantidade_do_produto = st.session_state[f'quantidade {numero}']

            id_ingrediente = select_ingredientes[lista_ingredientes.index(nome_ingrediente)][0]

            self.repository.insert_ingredientes_receita(id_produto, id_ingrediente, quantidade_do_produto)
            
        self.repository.insert_modo_preparo(id_produto, modo_preparo, rendimento)
        st.success('Dados registrados com sucesso!')
        st.session_state.ingredientes_formulario = False 

    def cadastro_condominio(self):

        st.subheader('Cadastro Condominio')

        nome_condominio = st.text_input('Nome do condominio')
        endereco = st.text_input('Endereço do condominio')
        nome_administrador = st.text_input('Nome do Administrador do condominio')
        telefone_administrador = st.text_input('Telefone do Administrador')

        if st.button('Cadastrar'):
            try:
                self.repository.insert_condominio(nome_condominio, endereco, nome_administrador, telefone_administrador)
                st.success('Condomio cadastrado com sucesso')
            
            except:
                st.error('Erro no sistema, condominio não cadastrado')



    