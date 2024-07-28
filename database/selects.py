import pymysql

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

try:
    cursor = connection.cursor()
    # Cambiar al esquema
    cursor.execute('USE data;')
    # Seleccionar todos los datos de la tabla Clients
    cursor.execute('SELECT * FROM Orders_2;')
    # Obtener todos los resultados
    results = cursor.fetchall()
    
    # Imprimir los resultados
    for row in results:
        print(row)
except pymysql.MySQLError as e:
    print(f"Error: {e}")
finally:
    connection.close()

