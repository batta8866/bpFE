import sqlite3



def conectar():
    try:
        conexion = sqlite3.connect("database.db")
        conexion.execute("PRAGMA foreing_keys = ON")
        print ("Conexion Exitosa")
        return conexion
    except:
        print("Error")



def eliminarFila(conexion, dni):

    consulta = "DELETE FROM datos WHERE dni = ?"
    conexion.execute(consulta, (dni,))
    conexion.commit()
    print("Eliminada la fila con DNI:", dni)



con = conectar()
eliminarFila(con, 32151476)

con.close