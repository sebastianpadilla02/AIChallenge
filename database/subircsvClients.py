import pandas as pd
import pymysql

# Configuración de la conexión
timeout = 10
connection = pymysql.connect(
    charset="utf8mb4",
    connect_timeout=timeout,
    cursorclass=pymysql.cursors.DictCursor,
    db="defaultdb",
    host="mysql-luthymakeup-luthymakeup.i.aivencloud.com",
    password="AVNS_fOnqMRAe1yWi236icem",
    read_timeout=timeout,
    port=13214,
    user="avnadmin",
    write_timeout=timeout,
)

# Leer el archivo CSV, asumiendo que la primera fila contiene los nombres de las columnas
csv_file_path = 'Clientes.csv'
df = pd.read_csv(csv_file_path, sep=';', skiprows=0)
# Convertir el formato de fecha al formato esperado por MySQL
df['Birthdate'] = pd.to_datetime(df['Birthdate'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')


# Insertar los datos en la tabla MySQL
try:
    cursor = connection.cursor()
    for index, row in df.iterrows():
        cursor.execute('''
            INSERT INTO data.Clients (Name, Birthdate, City, Address, PhoneNumber)
            VALUES (%s, %s, %s, %s, %s);
        ''', (row['Name'], row['Birthdate'], row['City'], row['Address'], row['PhoneNumber']))
    connection.commit()
    print("Data inserted successfully.")
except pymysql.MySQLError as e:
    print(f"Error: {e}")
finally:
    connection.close()
