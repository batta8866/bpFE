import sqlite3

data = {
    "36649243": "20366492438",
    "13450606": "27134506062",
    "39499692": "27394996926",
    "32059582": "27320595822",
    "43166176": "20431661765",
    "45215090": "20452150906",
    "27413631": "27274136311",
    "24363017": "27243630172",
    "41931620": "20419316203",
    "34163499": "27341634992",
    "12524932": "27125249324"
}

# Conectar a la base de datos (creará un archivo si no existe)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute('''CREATE TABLE IF NOT EXISTS datos
                  (dni TEXT PRIMARY KEY, cuit TEXT)''')

# Insertar los datos en la base de datos
for dni, cuit in data.items():
    cursor.execute('INSERT INTO datos (dni, cuit) VALUES (?, ?)', (dni, cuit))

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()





