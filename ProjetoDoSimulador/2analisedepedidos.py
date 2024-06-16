import pandas as pd
import sqlite3

conn = sqlite3.connect('empresa_abc.db')

clientes_df = pd.read_sql_query("SELECT * FROM Clientes", conn)
pedidos_df = pd.read_sql_query("SELECT * FROM Pedidos", conn)
detalhes_pedido_df = pd.read_sql_query("SELECT * FROM DetalhesdoPedido", conn)
produtos_df = pd.read_sql_query("SELECT * FROM Produtos", conn)


# Numero total de pedidos realizado por mes ?

pedidos_df['DatadoPedido'] = pd.to_datetime(pedidos_df['DatadoPedido'])
pedidos_df['Mês'] = pedidos_df['DatadoPedido'].dt.to_period('M')
total_pedidos_por_mes = pedidos_df['Mês'].value_counts().sort_index()

print("\nNúmero total de pedidos realizados por Mês: ")
print(total_pedidos_por_mes)

# qual é o valor medio de um pedido?
valor_pedidos = detalhes_pedido_df.merge(produtos_df, on='IDdoProduto')
valor_pedidos['ValorTotal'] = valor_pedidos['Quantidade']* valor_pedidos['Preço']
averiguacao_do_valor_pedido= valor_pedidos.groupby('IDdoPedido')['ValorTotal'].sum().mean()
print("\nValor médio de um pedido", averiguacao_do_valor_pedido)

# quais são os dias da semana com mais pedidos?
pedidos_df['DiaSemana'] = pedidos_df['DatadoPedido'].dt.day_name()
Pedido_dia_da_semana =  pedidos_df['DiaSemana'].value_counts()
print("\nDias da semana com mais pedidos: ", Pedido_dia_da_semana )



# qual é o pais com maior numero de pedidos?

pedidos_com_clientes = pedidos_df.merge(clientes_df, on='IDdoCliente')
pais_com_maior_numero_de_pedidos = pedidos_com_clientes['País'].value_counts().idxmax()
print("\n País com o maios número de pedidos: ", pais_com_maior_numero_de_pedidos)





conn.close()