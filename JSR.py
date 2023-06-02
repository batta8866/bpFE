import sqlite3
from retiradas_csv import *
lista_datos_pc = []
lista_dni_pc = []
lista_dni_a_nosis = []


# Conexión a la base de datos
conn = sqlite3.connect('database.db')
cursor = conn.cursor()


# Iterar sobre los DNI
for dni in lista_dni:
    # Consulta SQL para obtener el CUIT correspondiente al DNI
    cursor.execute("SELECT CUIT FROM datos WHERE DNI = ?", (dni,))
    result = cursor.fetchone()

    if result:
        cuit_en_pc = result[0]
        lista_datos_pc.append(cuit_en_pc)
        lista_dni_pc.append(dni)
        print(f"DNI: {dni} - {cuit_en_pc}")
    else:
        lista_dni_a_nosis.append(dni)

# Cerrar la conexión a la base de datos
conn.close()

if lista_dni_a_nosis:
    print ("\n DNI",lista_dni_a_nosis,"\n")



ADJ = pd.DataFrame({"CUIT": lista_datos_pc , "DNI" : lista_dni_pc})
ADJ = ADJ.drop_duplicates(subset='DNI')
df1J = df_dni.drop("CUIT" , axis=1).copy()
df_mergedJ = pd.merge(df1J, ADJ[['DNI', 'CUIT']], on='DNI', how='left')
df_mergedJ["CUIT"] = pd.to_numeric(df_mergedJ["CUIT"])   
df = df.drop(df[df.DNI.isin(df_mergedJ.DNI)].index) #elimine las filas donde encuentra un DNI en df igual a un DNI en df_merged (q es el de solo errores)
df["CUIT"] = pd.to_numeric(df["CUIT"])
df = pd.merge(df , df_mergedJ , how = "outer") #mete datos de df_merged con cuit
df = df.sort_values("ID de la Transaccion") #ordena por transaccion