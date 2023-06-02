from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.keys import Keys
import sqlite3
from JSR import lista_dni_a_nosis

cuit_nosis=[]

if lista_dni_a_nosis:
   
   base_dato_nosis=[]


   options = webdriver.ChromeOptions()
   options.add_argument("--headless")
   options.add_argument("--incognito")
   options.add_experimental_option('excludeSwitches', ['enable-logging'])
   driver = webdriver.Chrome(options=options)
   driver_service = Service(executable_path="C:/chromedriver.exe")

   driver.get("https://informes.nosis.com/?source")

   for x in lista_dni_a_nosis:
      driver.find_element(By.ID , "Busqueda_Texto").clear()
      driver.find_element(By.ID , "Busqueda_Texto").send_keys(x , Keys.ENTER)
      time.sleep(1)
      nos = driver.find_elements(By.XPATH , ('//*[@id="wrap-resultados"]/div/div[1]/div[1]/div[1]'))
      
      for element in nos:
         n=(element.text)
         formato = n[0:2]+n[3:11]+n[12:]
         ahora = int(formato)
         base_dato_nosis.append(ahora)
         print(".")

      driver.quit

   cuit_nosis = base_dato_nosis.copy()


   #cuit_nosis = [27315667734, 20393694611, 20450572250, 27103151851, 20447757096, 27316024845, 27401157803, 27401157803]

   print("CUIT" , cuit_nosis)





# Conexión a la base de datos
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Crear una lista de tuplas con los datos a insertar
data_to_insert = [(dni, cuit) for dni, cuit in zip(lista_dni_a_nosis, cuit_nosis) if cuit is not None]

# Insertar los datos en la tabla, omitiendo registros duplicados
cursor.executemany("INSERT OR IGNORE INTO datos (DNI, CUIT) VALUES (?, ?)", data_to_insert)

# Guardar los cambios en la base de datos
conn.commit()

# Cerrar la conexión a la base de datos
conn.close()


