"""
    Archivo de conexión a la base de datos
"""

# Importar Modulos
import mysql.connector

# Clase de Conexión
class DB_Conn:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'lc_pa_ba_eva2_2024'
        self.password = 'lc_pa_ba_eva2_2024'
        self.db = 'lc_pa_ba_eva2_2024'
        self.port = 3306
    
    def iniciar_conexion(self):
        self.conexion = mysql.connector.connect(host = self.host,
                                                user = self.user,
                                                password = self.password,
                                                database = self.db,
                                                port = self.port)
        return self.conexion
    
    def cerrar_conexion(self):
        self.conexion.close()


if __name__ == '__main__':
    # Probar la conexión
    db = DB_Conn()
    conexion = db.iniciar_conexion()
    
    if conexion.is_connected():
        print("Conexión exitosa")
    else:
        print("Error en la conexión")

    db.cerrar_conexion()
    




