import pandas as pd
import sqlite3
import random

# Connect to the SQLite database
conn = sqlite3.connect('empresa_abc.db')
cursor = conn.cursor()

# Create the "Estoque" column with default value 100 (if it doesn't exist)
try:
    cursor.execute('ALTER TABLE Produtos ADD COLUMN Estoque INTEGER DEFAULT 100;')
except sqlite3.OperationalError:
    pass  # Assuming the column already exists

# Create the "Promocoes" column with default value 50 (if it doesn't exist)
try:
    cursor.execute('ALTER TABLE Produtos ADD COLUMN Promocoes INTEGER DEFAULT 50;')
except sqlite3.OperationalError:
    pass  # Assuming the column already exists

# Read data from the "Produtos.csv" file (assuming it's correctly formatted and has no duplicates)
products_df = pd.read_csv('Produtos.csv')

# Add the "Estoque" and "Promocoes" columns to the DataFrame (if not already present)
if 'Estoque' not in products_df.columns:
    products_df['Estoque'] = 100
if 'Promocoes' not in products_df.columns:
    products_df['Promocoes'] = 50

# Update the "Estoque" column with random values (1-20)
products_df['Estoque'] = products_df['Estoque'].apply(lambda x: random.randint(1, 20))

# Generate alternating values for "Promocoes" based on product ID (assuming logic from Snippet 3)
def get_promocao(row):
    product_id = row['IDdoProduto']
    if product_id % 2 == 0:
        return 1
    else:
        return 0
products_df['Promocoes'] = products_df.apply(get_promocao, axis=1)

# Update the "Produtos" table with the modified data from the DataFrame
products_df.to_sql('Produtos', conn, if_exists='replace', index=False)

# Commit changes and close the database connection
conn.commit()
conn.close()
