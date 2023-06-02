import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.keys import Keys
import sqlite3
from tkinter import filedialog
import tkinter as tk
import tkinter.filedialog as fd


try:
    filename = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])

    try:
        df = pd.read_csv(filename, skiprows=1, names=["ID de la Transaccion", "Jugador", "Alias", "Nombre", "Apellido 1",
                                                    "Apellido2", "Direccion", "Municipio", "Provincia", "Pais",
                                                    "Partner", "Fecha creacion", "Fecha aprobacion", "Estado", "Pasarela",
                                                    "Fecha envio", "Descripcion", "Confirmacion", "Cantidad", "Cuenta",
                                                    "CBU", "Codigo postal", "Telefono", "Correo", "DNI", "Sexo",
                                                    "Fecha nacimiento", "CUIT"])

    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")

    df["CUIT"] = df.CUIT.str.replace("-", "", regex=True)
    df["CUIT"] = df.CUIT.str.replace(".", "", regex=True)

    # CODIGO POSTAL **********************************
    df["Codigo postal"] = pd.to_numeric(df["Codigo postal"], errors="coerce")
    df["Codigo postal"] = df["Codigo postal"].fillna(value=3000)
    df["Codigo postal"] = df["Codigo postal"].astype(int)
    df.rename(columns={"Codigo postal": "Codigo_postal"}, inplace=True)
    filtro_cpm = (df.Codigo_postal < 2000)
    df.loc[filtro_cpm, "Codigo_postal"] = 3000
    filtro_cpg = (df.Codigo_postal > 7000)
    df.loc[filtro_cpg, "Codigo_postal"] = 3000
    df.rename(columns={"Codigo_postal": "Codigo postal"}, inplace=True)
    # **********************************

    # CBU - CAMBIA O X 0 / ELIMINA [.] DEVUELVE ERRORES DE LARGOS  **********************************
    df["CBU"] = df.CBU.str.replace("-", "", regex=True)
    df["CBU"] = df.CBU.str.replace(".", "", regex=True)
    df["CBU"] = df.CBU.str.replace("o", "0", regex=True)
    df["CBU"] = df.CBU.str.replace("O", "0", regex=True)
    dfCBU = df[df.CBU.str.len() != 22]

    if dfCBU.notnull().shape[0] > 0:
        print("HAY ERROR EN LARGO DE CBU [Si aparece \ t es un salto]\n",
              dfCBU[["CBU", "ID de la Transaccion", "Apellido 1", "DNI"]], "\n")
    # **********************************

    df_dni = df[df.CUIT.str.len() != 11].copy().drop_duplicates(subset='DNI')
    lista_dni = df_dni["DNI"].tolist()
    #print("\n DNI", lista_dni, "\n")

    lista_jugador = df_dni["Jugador"].tolist()

    # ------------------------------------------


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




    # ------------------------------------------


    cuit_nosis=[]


    if lista_dni_a_nosis:

        base_dato_nosis = []

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--incognito")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        with webdriver.Chrome(options=options) as driver:
            driver_service = Service(executable_path="C:/chromedriver.exe")
            driver.get("https://informes.nosis.com/?source")

            busqueda_texto_elements = driver.find_elements(By.ID, "Busqueda_Texto")
            for element, x in zip(busqueda_texto_elements, lista_dni):
                element.clear()
                element.send_keys(x, Keys.ENTER)
                time.sleep(1)
                nos = driver.find_elements(By.XPATH, ('//*[@id="wrap-resultados"]/div/div[1]/div[1]/div[1]'))

                for element in nos:
                    n = element.text
                    formato = n[0:2] + n[3:11] + n[12:]
                    ahora = int(formato)
                    base_dato_nosis.append(ahora)
                    print(".")

        cuit_nosis = base_dato_nosis.copy()

        print("CUIT", cuit_nosis)


        # Conexión a la base de datos
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Crear una lista de tuplas con los datos a insertar
        data_to_insert = [(dni, cuit) for dni, cuit in zip(lista_dni_a_nosis, cuit_nosis)]

        # Insertar los datos en la tabla, omitiendo registros duplicados
        cursor.executemany("INSERT OR IGNORE INTO datos (DNI, CUIT) VALUES (?, ?)", data_to_insert)

        # Guardar los cambios en la base de datos
        conn.commit()

        # Cerrar la conexión a la base de datos
        conn.close()



    # ------------------------------------------

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


except Exception as a:
        print(f"Error {a}")