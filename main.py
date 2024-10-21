# Importar Modulos
from vistas import MenuPrincipal

# Punto de entrada
if __name__ == '__main__':
    # Mostrar el Menú Principal
    MenuPrincipal().mostrar()

# usuarios de prueba
# admin: Asdf1234
# gerente: Asdf1234
# usuario: Asdf1234

# REQUUERIMIENTOS DE PYTHON
# pip install mysql-connector-python bcrypt prettytable pwinput

# PARA CREAR BASE DE DATOS CORRER /SCRIPTS/DB_INICIALIZAR.SQL EN PHPMYADMIN
# PARA CAMBIAR PUERTO MYSQL, MODIFICAR EN /MODULES/DB_CONN.PY  // DEFAULT 3306


