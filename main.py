"""
    Notas de la Aplicación actualizado al (14-10-2024 0:21 AM):
        Actualmente funcionando:
            - Menú Principal (accesso a app segun rol)
            - CRUD de Empleados
            - CRUD de Departamentos
            - Script SQL para crear tablas, usuarios y cuentas de prueba

        Por hacer:
            - CRUD de Proyectos
            - CRUD Registro de Tiempo
            - Menu de Usuario Normal y Funciones Basicas
            - CRUD Informes

    ***Cuentas de Usuario:
        - Admin: admin / Asdf1234
        - Usuario: usuario / Asdf1234

    Bypass de Login:
        - Abrir (play) el archivo vistas.py

    Repositorio:
        - https://github.com/PokkzDev/Eva2Final

    Ramas activas:
        - main (master)
        - Chito 
        - Basty
        - Paola
"""

"""
    Punto de entrada de la aplicación
"""

""" 
    Pregunta para el profesor:
        - Es mejor hacer una clase hija con padre de Conexion a la BD o instanciar la clase Conexion en cada clase hija? 
        En cuanto a eficiencia de memoria y tiempo de ejecución.

        ie:
            -class DB_Conn:
                logica de conexion
            
            -class EmpleadoModel(DB_Conn):?

        O 
            
            -class EmpleadoModel:
                conexion = DB_Conn()?
"""

# Importar Modulos
from vistas import MenuPrincipal

# Punto de entrada
if __name__ == '__main__':
    # Mostrar el Menú Principal
    MenuPrincipal().mostrar()


