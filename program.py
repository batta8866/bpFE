import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
#from retiradas_csv import *
from nosis import cuit_nosis
from JSR import *


if not cuit_nosis:
        
        file_path = filedialog.asksaveasfilename(defaultextension='.xlsx', initialfile=' Informe Completo.xlsx')
        # Guardamos el archivo en la ubicación seleccionada
        df.to_excel(file_path, index=False)
        

        #df_merged.to_excel ("El Excel Erroes para Mandar Sta Fe Elim.xlsx" , index = False)


        file_path1 = filedialog.asksaveasfilename(defaultextension='.xlsx', initialfile='Erroes para Mandar.xlsx')
        # Guardamos el archivo en la ubicación seleccionada
        df_mergedJ.to_excel(file_path1, index=False)



elif len(cuit_nosis) != len(lista_dni_a_nosis):

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

        if dfv.loc[(dfv.DNI == cuit_d_dni) , "CUIT" ].item() != "":
            print("CLONADOS: ",cuitt)

        else:
            dfv.loc[(dfv.DNI == cuit_d_dni) , "CUIT" ] = cuitt      
        
    dfv["CUIT"] = pd.to_numeric(dfv["CUIT"])
    #print(dfv[["ID de la Transaccion","Jugador","Nombre","Apellido 1","CBU","DNI","CUIT"]])

    file_path1 = filedialog.asksaveasfilename(defaultextension='.xlsx', initialfile='Errores Mirar CUIT Clonados.xlsx')
    # Guardamos el archivo en la ubicación seleccionada
    dfv.to_excel(file_path1, index=False)

    #dfv.to_excel ("Santa Fe Errores Mirar CUIT Clonados.xlsx" , index = False) #guarda excel
    print("\nMIRAR QUE HAY CUIT CLONADOS\n")


elif  len(cuit_nosis) == len(lista_dni_a_nosis):

    ad = pd.DataFrame({"Jugador": lista_jugador , "CUIT": cuit_nosis , "DNI" : lista_dni_a_nosis})
    ad = ad.drop_duplicates(subset='DNI')
    df1 = df_dni.drop("CUIT" , axis=1).copy()
    df_merged = pd.merge(df1, ad[['DNI', 'CUIT']], on='DNI', how='left')
    df_merged["CUIT"] = pd.to_numeric(df_merged["CUIT"])
    

    
    df = df.drop(df[df.DNI.isin(df_merged.DNI)].index) #elimine las filas donde encuentra un DNI en df igual a un DNI en df_merged (q es el de solo errores)
    df["CUIT"] = pd.to_numeric(df["CUIT"])
  


    df = pd.merge(df , df_merged , how = "outer") #mete datos de df_merged con cuit
    df = df.sort_values("ID de la Transaccion") #ordena por transaccion



    #df.to_excel ("Informe Sta Fe Elim.xlsx" , index = False) #guarda excel


    file_path = filedialog.asksaveasfilename(defaultextension='.xlsx', initialfile=' Informe Completo.xlsx')
    # Guardamos el archivo en la ubicación seleccionada
    df.to_excel(file_path, index=False)
    

    #df_merged.to_excel ("El Excel Erroes para Mandar Sta Fe Elim.xlsx" , index = False)


    file_path1 = filedialog.asksaveasfilename(defaultextension='.xlsx', initialfile='Erroes para Mandar.xlsx')
    # Guardamos el archivo en la ubicación seleccionada
    df_merged.to_excel(file_path1, index=False)


