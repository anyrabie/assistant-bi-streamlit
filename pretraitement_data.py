import pandas as pd
from datetime import datetime
import sqlite3 as sql

path = './DataSet/Sample - Superstore.csv'
df = pd.read_csv(path, encoding='latin-1')

print(f'Dimensioms initiales : {df.shape}')
print(f'Colonnes : {df.columns}')
print(f'Valeurs manquantes : {df.isnull().sum()}')

df['Order Date'] = pd.to_datetime(df['Order Date'], format='mixed')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='mixed')

# Filtrer les transactions valides
df = df[df['Sales']>0]
df = df[df['Quantity']>0]

# Ajouter des colonnes derivees pour l’analyse
df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.month
df['day'] = df['Order Date'].dt.day

print(f'Dimensions aprés Nettoyage : {df.shape}')

kpi_category = df.groupby('Category').agg({
    'Sales' :['sum', 'mean', 'count'],
    'Profit' :['sum', 'mean'],
    'Quantity' : 'sum'
}).round(2)

kpi_category.columns = ['_'.join(col) for col in kpi_category.columns]
#print(kpi_category.head())

kpi_region_month = df.groupby(['Region', 'Year', 'Month']).agg({
    'Sales' : 'sum',
    'Profit' : 'sum' 
}).reset_index()

df.columns = df.columns.str.replace(' ', '_').str.replace('-', '_')
df.to_csv('./DataSet/superstore_cleaned.csv',index=False)
kpi_category.to_csv('./DataSet/kpi_categories.csv', index=False)

conn = sql.connect('./DataSet/dw_ventes.db')
df.to_sql('ventes',conn, if_exists='replace', index=False)
kpi_category.to_sql('kpi_categories', conn, if_exists='replace', index=False)
kpi_region_month.to_sql('kpi_region_mois', conn, if_exists='replace', index=False)

conn.close()

print('Preprocessing termine avec succes !')
print(df.columns)