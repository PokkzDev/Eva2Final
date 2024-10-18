"""
    Este modulo se encarga de manejar la autenticación de los usuarios.
"""
from modules.db_conn import DB_Conn
import bcrypt

# Clase de Autenticación
class Auth:
    def __init__(self):
        self.db = DB_Conn()
        self.conexion = self.db.iniciar_conexion()
    
    # Metodo de Iniciar Sesión
    def iniciar_sesion(self, usuario, password):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT username, password, rol FROM empleados WHERE username = %s", (usuario,))
        usuario = cursor.fetchone()
        cursor.close()
        
        if usuario:
            if bcrypt.checkpw(password.encode('utf-8'), usuario[1].encode('utf-8')):
                # return True, username, rol
                return True, usuario[0], usuario[2]
            else:
                return False
        else:
            return False

    # Metodo de Cerrar Conexión
    def __del__(self):
        self.db.cerrar_conexion()

if __name__ == '__main__':
    pass
        
    