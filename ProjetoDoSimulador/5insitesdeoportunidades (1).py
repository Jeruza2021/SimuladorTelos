import pandas as pd
import sqlite3

conn = sqlite3.connect('empresa_abc.db')

clientes_df = pd.read_sql_query("SELECT * FROM Clientes", conn)
pedidos_df = pd.read_sql_query("SELECT * FROM Pedidos", conn)
detalhes_pedido_df = pd.read_sql_query("SELECT * FROM DetalhesdoPedido", conn)
produtos_df = pd.read_sql_query("SELECT * FROM Produtos", conn)

# 1 produtos que têm alta demanda, mas baixa disponibilidade em estoque


# Agrupar por IDdoProduto e somar as quantidades para obter a demanda total
demand_df = detalhes_pedido_df.groupby('IDdoProduto')['Quantidade'].sum().reset_index()
demand_df.columns = ['IDdoProduto', 'Demanda']

# Mesclar com a tabela de produtos para obter o estoque
merged_df = pd.merge(produtos_df, demand_df, on='IDdoProduto')

# Filtrar produtos com alta demanda e baixa disponibilidade em estoque
alta_demanda_baixo_estoque = merged_df[(merged_df['Demanda'] > 50) & (merged_df['Estoque'] < 20)]
print(alta_demanda_baixo_estoque)

# 2 identificar os países com maior potencial de expansão de mercado?
# Mesclar pedidos com clientes para obter o país
merged_df = pd.merge(pedidos_df, clientes_df, on='IDdoCliente')

# Agrupar por país e contar o número de pedidos
pais_vendas_df = merged_df.groupby('País').IDdoPedido.count().reset_index()
pais_vendas_df.columns = ['País', 'NumeroDePedidos']

# Ordenar por número de pedidos em ordem decrescente
pais_vendas_df = pais_vendas_df.sort_values(by='NumeroDePedidos', ascending=False)
print(pais_vendas_df)


# 3. Eficácia das promoções em termos de aumento no número de pedidos

# Converter a coluna 'DatadoPedido' para datetime
pedidos_df['DatadoPedido'] = pd.to_datetime(pedidos_df['DatadoPedido'])

# Adicionar uma coluna de promoção na tabela Pedidos 
# (1 para pedidos durante a promoção, 0 para fora da promoção nos periodo definido nas variaveis abaixo)
promocao_inicio = pd.to_datetime('2023-02-01')
promocao_fim = pd.to_datetime('2023-07-31')
pedidos_df['Promocoes'] = pedidos_df['DatadoPedido'].apply(lambda x: 1 if promocao_inicio <= x <= promocao_fim else 0)

# Agrupar por promoção e contar o número de pedidos
promocao_eficacia_df = pedidos_df.groupby('Promocoes')['IDdoPedido'].count().reset_index()
promocao_eficacia_df.columns = ['Promocoes', 'NumeroDePedidos']

print("\nNúmero de pedidos durante e fora da promoção:")
print(promocao_eficacia_df)

#4 padrões de compra recorrentes entre clientes?

# Mesclar detalhes do pedido com pedidos para obter o ID do cliente
merged_df = pd.merge(detalhes_pedido_df, pedidos_df, on='IDdoPedido')

# Agrupar por ID do cliente e ID do produto e contar as ocorrências
padroes_df = merged_df.groupby(['IDdoCliente', 'IDdoProduto']).IDdoPedido.count().reset_index()
padroes_df.columns = ['IDdoCliente', 'IDdoProduto', 'Frequencia']

# Filtrar para padrões recorrentes ( frequência maior que 1)
padroes_de_compra_df = padroes_df[padroes_df['Frequencia'] > 1]

print("\nPadrão de compra dos Clientes\n\n",padroes_de_compra_df)

conn.close()