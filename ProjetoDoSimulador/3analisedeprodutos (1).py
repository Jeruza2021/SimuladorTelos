import sqlite3
import pandas as pd


conn = sqlite3.connect('empresa_abc.db')

clientes_df = pd.read_sql_query("SELECT * FROM Clientes", conn)
pedidos_df = pd.read_sql_query("SELECT * FROM Pedidos", conn)
detalhes_pedido_df = pd.read_sql_query("SELECT * FROM DetalhesdoPedido", conn)
produtos_df = pd.read_sql_query("SELECT * FROM Produtos", conn)

# top 5 dos produtos mais vendidos
categoria_vendas= detalhes_pedido_df.merge(produtos_df, on='IDdoProduto')
top_5_categorias = categoria_vendas['Categoria'].value_counts().head(5)
print("top 5 categorias de produtos mais vendidos : ")
print(top_5_categorias)

# qual o produto mais caro

produto_mais_caro = produtos_df.loc[produtos_df['Preço'].idxmax()]
print("\nProduto mais caro que foi vendio: ")
print(produto_mais_caro)

# Qual Categoria de produto que gera mais receita
categoria_vendas['Receita'] = categoria_vendas['Quantidade']* categoria_vendas['Preço']
categoria_rev = categoria_vendas.groupby('Categoria')['Receita'].sum()
top_rev_categoria = categoria_rev.idxmax()
print("\nCategoria de produto que gera a maior receita: ")
print(f"{top_rev_categoria}: {categoria_rev[top_rev_categoria]}")

# quais são os top 3 dos produtos mais vendidos ?

top_3_produtos = categoria_vendas.groupby("NomedoProduto")['Quantidade'].sum().nlargest(3)
print("\nTop 3 de produtos mais vendidos")
print(top_3_produtos)