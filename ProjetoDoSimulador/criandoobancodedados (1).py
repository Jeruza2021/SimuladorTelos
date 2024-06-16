import sqlite3
import pandas as pd


conn = sqlite3.connect('empresa_abc.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS Clientes (
    IDdoCliente INTEGER PRIMARY KEY,
    Nome TEXT,
    País TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Produtos (
    IDdoProduto INTEGER PRIMARY KEY,
    NomedoProduto TEXT,
    Categoria TEXT,
    Preço REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Pedidos (
    IDdoPedido INTEGER PRIMARY KEY,
    IDdoCliente INTEGER,
    DatadoPedido TEXT,
    FOREIGN KEY(IDdoCliente) REFERENCES Clientes(IDdoCliente)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS DetalhesdoPedido (
    IDdoPedido INTEGER,
    IDdoProduto INTEGER,
    Quantidade INTEGER,
    FOREIGN KEY(IDdoPedido) REFERENCES Pedidos(IDdoPedido),
    FOREIGN KEY(IDdoProduto) REFERENCES Produtos(IDdoProduto)
)
''')


clients_df = pd.read_csv('Clientes.csv')
clients_df.to_sql('Clientes', conn, if_exists='append', index=False)

products_df = pd.read_csv('Produtos.csv')
products_df.to_sql('Produtos', conn, if_exists='append', index=False)

orders_df = pd.read_csv('Pedidos.csv')
orders_df.to_sql('Pedidos', conn, if_exists='append', index=False)

details_df = pd.read_csv('DetalhesdoPedido.csv')
details_df.to_sql('DetalhesdoPedido', conn, if_exists='append', index=False)

conn.commit()
conn.close()