"""
    Este modulo se encarga de manejar la autenticación de los usuarios.

    Clase:
        Auth: Clase de Autenticación
    Metodos:
        iniciar_sesion: Metodo de Iniciar Sesión
        __del__: Metodo de Cerrar Conexión 
"""
if __name__ == '__main__':
    from db_conn import DB_Conn
else :
    from modules.db_conn import DB_Conn
import bcrypt
 
# Clase de Autenticación
class Auth:
    def __init__(self):
        self.db = DB_Conn()
        self.conexion = self.db.iniciar_conexion()
 
    # Metodo de Iniciar Sesión
    def iniciar_sesion(self, usuario, password):
        try:
            cursor = self.conexion.cursor()
            cursor.execute("SELECT id, username, password, rol FROM empleados WHERE username = %s", (usuario,))
            usuario = cursor.fetchone()

            # traer el departamento_id usando el id del usuario
            if usuario:
                cursor.execute("SELECT departamento_id FROM empleados_departamento WHERE empleado_id = %s", (usuario[0],))
                departamento_id = cursor.fetchone()
            
                # agregar el departamento_id al usuario
                usuario = list(usuario)
                usuario.append(departamento_id[0])

            cursor.close()

            # Cerrar la conexión
            self.db.cerrar_conexion()

            # Verificar si el usuario existe
            if usuario:
                # Verificar si la contraseña es correcta
                if bcrypt.checkpw(password.encode("utf-8"), usuario[2].encode("utf-8")):
                    # Crear un diccionario con los datos del usuario
                    user = {
                        "id": usuario[0],
                        "username": usuario[1],
                        "rol": usuario[3],
                        "departamento_id": usuario[4]
                    }
                    return user
                else:
                    return False
            else:
                return False
        except Exception as e:
            # Log the error or handle it as needed
            print(f"Error: {e}")
            return False
    
    # Metodo de Cerrar Conexión
    def __del__(self):
        self.db.cerrar_conexion()
 
if __name__ == '__main__':
    # Probar la autenticación
    auth = Auth()
    print(auth.iniciar_sesion("admin", "Asdf1234"))
    print("----")
    print(auth.iniciar_sesion("gerente", "Asdf1234"))
    print("----")
    print(auth.iniciar_sesion("usuario", "Asdf1234"))
   
