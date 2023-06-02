import pandas as pd
from tkinter import filedialog
import json

#df = pd.read_csv("D:/Python/Bplay Errores Sta Fe/Retiradas.csv", skiprows=1, names= ["ID de la Transaccion","Jugador","Alias","Nombre","Apellido 1","Apellido2","Direccion","Municipio","Provincia","Pais","Partner","Fecha creacion","Fecha aprobacion","Estado","Pasarela","Fecha envio","Descripcion","Confirmacion","Cantidad","Cuenta","CBU","Codigo postal","Telefono","Correo","DNI","Sexo","Fecha nacimiento","CUIT"])
filename = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
df = pd.read_csv(filename, skiprows=1, names=["ID de la Transaccion","Jugador","Alias","Nombre","Apellido 1","Apellido2","Direccion","Municipio","Provincia","Pais","Partner","Fecha creacion","Fecha aprobacion","Estado","Pasarela","Fecha envio","Descripcion","Confirmacion","Cantidad","Cuenta","CBU","Codigo postal","Telefono","Correo","DNI","Sexo","Fecha nacimiento","CUIT"])


df["CUIT"] = df.CUIT.str.replace("-" , "" , regex=True)
df["CUIT"] = df.CUIT.str.replace("." , "" , regex=True)


# CODIGO POSTAL **********************************

df["Codigo postal"] = pd.to_numeric(df["Codigo postal"] , errors = "coerce")
df["Codigo postal"] = df["Codigo postal"].fillna(value=3000)
df["Codigo postal"] = df["Codigo postal"].astype(int)

df.rename(columns={"Codigo postal" : "Codigo_postal"} , inplace= True)

filtro_cpm = (df.Codigo_postal<2000)
df.loc[filtro_cpm , "Codigo_postal" ] = 3000
filtro_cpg = (df.Codigo_postal>7000)
df.loc[filtro_cpg , "Codigo_postal" ] = 3000

df.rename(columns={"Codigo_postal" : "Codigo postal"} , inplace= True)

# **********************************

# CBU - CAMBIA O X 0 / ELIMINA [.] DEVUELVE ERRORES DE LARGOS  **********************************

df["CBU"] = df.CBU.str.replace("-" , "" , regex=True)
df["CBU"] = df.CBU.str.replace("." , "" , regex=True)
df["CBU"] = df.CBU.str.replace("o" , "0" , regex=True)
df["CBU"] = df.CBU.str.replace("O" , "0" , regex=True)
dfCBU = df[df.CBU.str.len() != 22]

dfCBU = df[df.CBU.str.len() != 22]
if dfCBU.notnull().shape[0] > 0:
    print("HAY ERROR EN LARGO DE CBU [Si aparece \ t es un salto]\n" , dfCBU[["CBU","ID de la Transaccion","Apellido 1","DNI"]],"\n")

# **********************************


df_dni = df[df.CUIT.str.len() != 11].copy() # VER COMO ESTABA EN LA VERSION ANTERIOR
lista_dni = df_dni["DNI"].tolist()
#print ("\n DNI",lista_dni,"\n")

# LISTA PARA USAR EN PROGRAMA ---> ad = pd.DataFrame({"Jugador": lista_jugador , "CUIT": cuit_nosis , "DNI" : lista_dni})

lista_jugador = df_dni["Jugador"].tolist()
