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
    # Crear el esquema
    cursor.execute('CREATE SCHEMA IF NOT EXISTS data;')
    # Cambiar al esquema
    cursor.execute('USE data;')
    # Crear la tablaNombre;Cargo;Celular;Salario;DetalleFunciones
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS `Employees_3` (
            `EmployeeID` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
            `Name` text NOT NULL,
            `Position` text NOT NULL,
            `PhoneNumber` text NOT NULL,
            `Salary` float NOT NULL,
            `Functions` text
        );
    ''')
    connection.commit()
    print("Schema and table created successfully.")
except pymysql.MySQLError as e:
    print(f"Error: {e}")
finally:
    connection.close()

