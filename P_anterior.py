import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.keys import Keys

from tkinter import filedialog
import tkinter as tk
import tkinter.filedialog as fd



filename = filedialog.askopenfilename()

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


if dfCBU.notnull().shape[0] > 0:
    print("HAY ERROR EN LARGO DE CBU [Si aparece \ t es un salto]\n" , dfCBU[["CBU","ID de la Transaccion","Apellido 1","DNI"]],"\n")




# **********************************


df_dni = df[df.CUIT.str.len() != 11].copy() # VER COMO ESTABA EN LA VERSION ANTERIOR
lista_dni = df_dni["DNI"].tolist()
print ("\nDNI",lista_dni,"\n")


lista_jugador = df_dni["Jugador"].tolist()





cuit_nosis = [20287956690, 27373963858, 20400543837, 20400543837, 20447774403, 27259100599, 20409710248, 20371550845, 20360085261, 20287956690] 







print("CUIT",cuit_nosis,"\n")


if len(cuit_nosis) != len(lista_dni):

    dfv = df[df.CUIT.str.len() != 11].copy()
    lista_={}

    for cuitt in cuit_nosis:
        cuit_d_dni =str(cuitt)
        cuit_d_dni =int(cuit_d_dni[2:10])
        if cuit_d_dni in lista_ and lista_[(cuit_d_dni)] != cuitt:
            print("DNI:", cuit_d_dni ,"--",cuitt , lista_[(cuit_d_dni)])

            options = webdriver.ChromeOptions()
            options.add_argument("--incognito")
            options.add_experimental_option("detach", True)
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            driver = webdriver.Chrome(options=options)
            driver_service = Service(executable_path="C:/chromedriver.exe")
            driver.get("https://informes.nosis.com/?source")
            driver.find_element(By.ID , "Busqueda_Texto").clear()
            driver.find_element(By.ID , "Busqueda_Texto").send_keys(cuit_d_dni , Keys.ENTER)
        else:
            lista_[cuit_d_dni]=cuitt       
        dfv.loc[(dfv.DNI == cuit_d_dni) , "CUIT" ] = cuitt      
        
    dfv["CUIT"] = pd.to_numeric(dfv["CUIT"])
    #dfv.to_excel ("Santa Fe Errores Mirar CUIT Clonados.xlsx" , index = False) #guarda excel
    print("\nMIRAR QUE HAY CUIT CLONADOS\n")


    file_pathE = filedialog.asksaveasfilename(defaultextension='.xlsx', initialfile='Errores Mirar CUIT Clonados.xlsx')
    # Guardamos el archivo en la ubicación seleccionada
    dfv.to_excel(file_pathE, index=False)
    # Mostramos el texto que se agregó en el programa en una ventana de confirmación

















if len(cuit_nosis) == len(lista_dni):

    ad = pd.DataFrame({"Jugador": lista_jugador , "CUIT": cuit_nosis , "DNI" : lista_dni})
    df1 = df_dni.drop("CUIT" , axis=1).copy()
    df1 = pd.merge (df1 , ad) 
    df = df.drop(index = df[df.CUIT == ""].index)

    df["CUIT"] = pd.to_numeric(df["CUIT"])


    df = pd.merge(df , df1 , how = "outer") #mete datos de df1 con cuit
    df = df.sort_values("ID de la Transaccion") #ordena por transaccion



    #df1.to_excel ("El Excel Erroes para Mandar Sta Fe Elim.xlsx" , index = False)
    #df.to_excel ("Informe Sta Fe Elim.xlsx" , index = False) #guarda excel




    file_path = filedialog.asksaveasfilename(defaultextension='.xlsx', initialfile=' Informe Completo.xlsx')
    # Guardamos el archivo en la ubicación seleccionada
    df.to_excel(file_path, index=False)


    file_path1 = filedialog.asksaveasfilename(defaultextension='.xlsx', initialfile='Erroes para Mandar.xlsx')
    # Guardamos el archivo en la ubicación seleccionada
    df1.to_excel(file_path1, index=False)



