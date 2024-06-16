import pandas as pd
import sqlite3

conn = sqlite3.connect('empresa_abc.db')
# Quais são os top5 países em número de clientes?

clientes_df = pd.read_sql_query('SELECT * FROM Clientes', conn)

top_5_pais = clientes_df['País'].value_counts().head(5)

print(top_5_pais)
#Quantos clientes únicosrealizarammaisdeumpedido?

orders_df = pd.read_sql_query('SELECT * FROM Pedidos', conn)

clientes_pedidos_conta = orders_df['IDdoCliente'].value_counts()
unique_clientes_multiplos_pedidos = (clientes_pedidos_conta > 1).sum()

print("Clientes únicos que realizaram mais de um pedido. ", unique_clientes_multiplos_pedidos)

#Qualéovalormédiodepedidosporclienteemcadapaís?

# Carregar os dados das tabelas
clientes_df = pd.read_sql_query("SELECT * FROM Clientes", conn)
pedidos_df = pd.read_sql_query("SELECT * FROM Pedidos", conn)
detalhes_pedido_df = pd.read_sql_query("SELECT * FROM DetalhesdoPedido", conn)
produtos_df = pd.read_sql_query("SELECT * FROM Produtos", conn)


# Juntar as tabelas de detalhes do pedido com produtos para obter o valor total dos pedidos
pedidos_valores = pd.merge(detalhes_pedido_df, produtos_df, on='IDdoProduto')
pedidos_valores['ValorTotal'] = pedidos_valores['Quantidade'] * pedidos_valores['Preço']

# Juntar valores dos pedidos com os pedidos
pedidos_com_valores = pd.merge(pedidos_df, pedidos_valores[['IDdoPedido', 'ValorTotal']], on='IDdoPedido')

# Juntar com os clientes para obter o país
pedidos_clientes = pd.merge(clientes_df, pedidos_com_valores, left_on='IDdoCliente', right_on='IDdoCliente')

# Calcular o valor médio dos pedidos por cliente em cada país
valor_medio_pedido_por_pais = pedidos_clientes.groupby('País')['ValorTotal'].mean()

print("Valor médio de pedidos por cliente em cada país:")
print(valor_medio_pedido_por_pais)

# Quais são os 3 principais clientes em termos de valor total de pedidos?
total_valor_por_cliente = pedidos_clientes.groupby('IDdoCliente')['ValorTotal'].sum()
top_3_clientes = total_valor_por_cliente.nlargest(3).index
top_3_clientes_info = clientes_df[clientes_df['IDdoCliente'].isin(top_3_clientes)]

print("\nTop 3 clientes em termos de valor total de pedidos:")
print(top_3_clientes_info)

# Fechar a conexão
conn.close()



