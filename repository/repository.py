from database import DataBaseMysql
import streamlit as st


class Repository:

    def __init__(self, db) -> None:
       self.db = db

    # INSERTS

    def insert_ingrediente(self, nome_ingrediente, medida_ingrediente):
        cursor = self.db.connect()
        cursor.execute("INSERT INTO ingredientes (nome, unidade) VALUES (%s, %s)", (nome_ingrediente, medida_ingrediente))

        self.db.disconnect()

    def insert_mercado(self, nome_mercado):
        cursor = self.db.connect()
        cursor.execute("INSERT INTO mercado (nome) VALUES (%s)", (nome_mercado, ))

        self.db.disconnect()

    def insert_compra_ingredientes(self, id_ingrediente, id_mercado, marca, preco, quantidade, data, custo_medida):

        cursor = self.db.connect()

        cursor.execute('INSERT INTO compra_ingredientes (id_ingrediente, id_mercado, marca, preco, quantidade, data_compra, preço_unidade) VALUES (%s, %s, %s, %s, %s, %s, %s)', (id_ingrediente, id_mercado, marca, preco, quantidade, data, custo_medida))

        self.db.disconnect()

    def insert_produto(self, nome_produto):

        cursor = self.db.connect()
        cursor.execute("INSERT INTO produtos (nome) VALUES (%s)", (nome_produto, ))
        id_produto = cursor.lastrowid

        self.db.disconnect()

        return id_produto
    
    def insert_ingredientes_receita(self, id_produto, id_ingrediente, quantidade):

        cursor = self.db.connect()
        cursor.execute('INSERT INTO ingredientes_receita (id_produto, id_ingrediente, quantidade) VALUES (%s, %s, %s)', (id_produto, id_ingrediente, quantidade))
        self.db.disconnect()

    def insert_modo_preparo(self, id_produto, modo_preparo, rendimento):

        cursor = self.db.connect()
        cursor.execute('INSERT INTO modo_preparo (id_produto, preparo, rendimento) VALUES (%s, %s, %s)', (id_produto, modo_preparo, rendimento))
        self.db.disconnect()

    def insert_condominio(self, nome, endereco, nome_administrador, telefone_administrador):
        cursor = self.db.connect()
        cursor.execute('INSERT INTO condominio (nome, endereco, administrador, tel_administrador) VALUES (%s, %s, %s, %s)',(nome, endereco, nome_administrador, telefone_administrador))
        self.db.disconnect()

    def insert_estoque_produto(self, id_produto, id_lote, tipo_movimento, quantidade, custo_unitario):
        cursor = self.db.connect()
        cursor.execute("INSERT INTO estoque_produtos (id_produto, id_lote, tipo_movimento, quantidade, custo_unitario) VALUES (%s, %s, %s, %s, %s)", (id_produto, id_lote, tipo_movimento, quantidade, custo_unitario))

        self.db.disconnect()

    def insert_registro_producao(self, id_produto, id_lote, data, rendimento, custo_total):
        cursor = self.db.connect()
        cursor.execute("INSERT INTO registro_producao (id_produto, id_lote, data_producao, data_validade, rendimento, custo_total) VALUES (%s, %s, %s, CURDATE() + INTERVAL 30 DAY, %s, %s)", (id_produto, id_lote, data, rendimento, custo_total))
        self.db.disconnect()

    def insert_vendas(self, id_produto, id_condominio, quantidade, valor, custo, lucro, data):

        cursor = self.db.connect()
        cursor.execute("""
        INSERT INTO vendas 
            (id_produto, id_condominio, quantidade, preco_unitario, custo_unitario, lucro, data_venda) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)""",(id_produto, id_condominio, quantidade, valor, custo, lucro, data))

        self.db.disconnect()

    
    def insert_agendamento_condominio(self, data, dia_da_semana, id_condominio):
        cursor = self.db.connect()

        cursor.execute("INSERT INTO agendamento_condominios (data_agendamento, dia_da_semana, id_condominio) VALUES (%s, %s, %s)", (data, dia_da_semana, id_condominio))

    # SELECTS
    def select_ingredientes(_self):
        cursor = _self.db.connect()
        cursor.execute('SELECT id, nome, unidade FROM ingredientes')
        resultado = cursor.fetchall()
        _self.db.disconnect()
        return resultado
    
    def select_mercado(_self):
        cursor = _self.db.connect()
        cursor.execute('SELECT id, nome FROM mercado')
        resultado = cursor.fetchall()
        _self.db.disconnect()
        return resultado
    
    def select_condominio(self):
        
        cursor = self.db.connect()
        cursor.execute("SELECT id, nome FROM condominio")
        resultado = cursor.fetchall()
        self.db.disconnect()
        return resultado
    
    def select_receitas(self):
        cursor = self.db.connect()
        cursor.execute("""
        SELECT 
            p.nome, 
            i.nome, 
            ir.quantidade,
            i.unidade,
            ir.id_produto
        from ingredientes_receita as ir
        join ingredientes as i ON i.id =  ir.id_ingrediente
        join produtos as p on p.id = ir.id_produto
        """)

        resultado = cursor.fetchall()
        self.db.disconnect()
        return resultado

    def select_nome_receitas(self):
        cursor = self.db.connect()
        cursor.execute("SELECT id, nome, custo_unidade, custo_receita FROM produtos")

        resultado = cursor.fetchall()
        self.db.disconnect()
        return resultado
    
    def select_modo_preparo(self, id_produto):
        cursor = self.db.connect()
        cursor.execute("""
        SELECT 
            preparo,
            rendimento
        from modo_preparo
        where id_produto = %s
        """, (id_produto, ))

        resultado = cursor.fetchall()
        self.db.disconnect()
        return resultado
    

    def select_receita_estoque_por_id(self):

        cursor = self.db.connect()

        cursor.execute("""
        SELECT 
            p.id,
            p.nome,
            COALESCE(SUM(CASE WHEN e.tipo_movimento = 'entrada' THEN e.quantidade ELSE -e.quantidade END), 0) AS quantidade_estoque,
            p.custo_unitario
        FROM 
            produtos p
        LEFT JOIN 
            estoque_produtos e ON p.id = e.id_produto
        GROUP BY 
            p.id, p.nome""")
        
        resultado = cursor.fetchall()
        self.db.disconnect()
        return resultado
        
    
    def select_ultimo_id_lote(self, id_produto):

        cursor = self.db.connect()

        cursor.execute("SELECT COALESCE(MAX(id_lote),0) FROM registro_producao WHERE id_produto = %s", (id_produto, ))

        resultado = cursor.fetchone()
        self.db.disconnect()
        return resultado
    

    def select_quantidade_estoque(self):
        cursor = self.db.connect()

        cursor.execute("""
        SELECT
            subquery.id_lote,
            p.nome,
            subquery.quantidade,
            p.custo_unidade,
            rp.data_producao,
            rp.data_validade
        FROM (
            SELECT
                rp.id_lote,
                rp.id_produto,
                SUM(CASE WHEN e.tipo_movimento = 'ENTRADA' THEN e.quantidade ELSE -e.quantidade END) as quantidade
            FROM registro_producao as rp
            JOIN estoque_produtos as e ON e.id_produto = rp.id_produto AND e.id_lote = rp.id_lote
            GROUP BY rp.id_lote, rp.id_produto
        ) AS subquery
        JOIN produtos as p ON p.id = subquery.id_produto
        JOIN registro_producao as rp ON rp.id_lote = subquery.id_lote AND rp.id_produto = subquery.id_produto
        ORDER BY subquery.id_produto;

        """)

        resultado = cursor.fetchall()
        self.db.disconnect()
        return resultado
    
    def select_estoque(self):
        cursor = self.db.connect()
        cursor.execute("""
        SELECT
            p.nome,
            SUM(CASE WHEN e.tipo_movimento = 'ENTRADA' THEN e.quantidade ELSE -e.quantidade END) as quantidade,
            p.custo_unidade
        FROM produtos as p 
        JOIN estoque_produtos as e ON p.id = e.id_produto 
        group by p.nome              
                       
        """)

        resultado = cursor.fetchall()
        self.db.disconnect()
        return resultado
    
    def select_custo_receita_produto(self, id_produto):
        cursor = self.db.connect()

        cursor.execute("""
        SELECT 
            SUM(r.quantidade * i.custo_medio_por_medida) as custo_receita
        from ingredientes_receita as r
        join ingredientes as i ON r.id_ingrediente = i.id
        where r.id_produto = %s""", (id_produto, ))
        
        resultado = cursor.fetchall()
        self.db.disconnect()
        return resultado
    

    def select_lote_produto(self, id_produto):
        cursor = self.db.connect()
        cursor.execute("""
        SELECT 
            id_lote,
            CASE WHEN tipo_movimento = 'ENTRADA' THEN quantidade ELSE -quantidade END as quantidade
        FROM estoque_produtos 
        WHERE id_produto = %s""", (id_produto, ))
        
        resultado = cursor.fetchall()
        self.db.disconnect()
        return resultado
    

    def select_historico_vendas(self):
        cursor = self.db.connect()

        cursor.execute("""
        SELECT
            v.data_venda,
            c.nome,
            SUM(v.quantidade),
            SUM(v.preco_unitario),
            SUM(v.lucro)
        FROM vendas as v
        JOIN condominio as c ON c.id = v.id_condominio
        GROUP BY v.data_venda and c.nome """)

        resultado = cursor.fetchall()
        self.db.disconnect()
        return resultado
    

    def select_ultimas_vendas(self):
        cursor = self.db.connect()

        cursor.execute("""
        select
            v.id,
            v.data_venda,
            p.nome,
            v.quantidade,
            v.preco_unitario
        from vendas as v
        join produtos as p ON p.id = v.id_produto
        order by v.data_venda desc limit 15""")

        resultado = cursor.fetchall()
        self.db.disconnect()
        return resultado
    

    def select_agendamento_condominio(self):
        cursor = self.db.connect()

        cursor.execute("""
        SELECT
            a.data_agendamento,
            c.nome
        FROM agendamento_condominios as a
        JOIN condominio as c ON c.id = a.id_condominio""")

        resultado = cursor.fetchall()
        self.db.disconnect()
        return resultado
            

    def update_custos_receita(self, custo_total, custo_unitario, id_produto):

        cursor = self.db.connect()
        cursor.execute("UPDATE produtos SET custo_receita = %s, custo_unidade = %s WHERE id = %s",(custo_total, custo_unitario, id_produto))

    
    def update_custo_ingrediente(self, custo_medida, id_ingrediente):
        cursor = self.db.connect()
        cursor.execute("UPDATE ingredientes SET custo_medio_por_medida = %s where id = %s", (custo_medida, id_ingrediente))

    def update_venda(self, data_editada, id_produto, quantidade_editada, preco_editado, id_venda):
        cursor = self.db.connect()
        cursor.execute('UPDATE vendas SET data_venda = %s, id_produto = %s, quantidade = %s, preco_unitario = %s where id = %s', (data_editada, id_produto, quantidade_editada, preco_editado, id_venda))
    
 

        