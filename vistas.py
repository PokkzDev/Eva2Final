"""
    Este archivo se encarga de manejar las vistas de la aplicación. #test
"""

# Importar Modulos
from modules.auth import Auth
from modules.modelo import Empleado, EmpleadoModel, Departamento, DepartamentoModel, Proyecto, ProyectoModel
import pwinput
import os
import time
from prettytable import PrettyTable
import bcrypt

# Clase de Menú Principal
class MenuPrincipal:
    def mostrar(self):
        limpiar_pantalla()
        print("--- Menú Principal ---\n")

        usuario = input("Ingrese su usuario: ")
        password = pwinput.pwinput(prompt="Ingrese su contraseña: ")

        auth = Auth()

        try:
            if auth.iniciar_sesion(usuario, password):
                print("\nUsuario autenticado")
                time.sleep(1)
                user = auth.iniciar_sesion(usuario, password)

                if user[2] == "admin":
                    menu = MenuAdmin(user[1])
                    menu.mostrar()
                elif user[2] == "gerente":
                    menu = MenuGerente(user[1])
                    menu.mostrar()
                else:
                    menu = MenuEmpleado(user[1])
                    menu.mostrar()
            else:
                print("\nCreedenciales incorrectas")
                time.sleep(1)
                self.mostrar()
        except:
            print("\nError en la autenticación")
            time.sleep(1)
            self.mostrar()

# Clase de Menú de Administrador
class MenuAdmin:
    def __init__(self, usuario):
        self.usuario = usuario

    def mostrar(self):
        while True:
            limpiar_pantalla()
            print("--- Menú de Administrador ---\n")

            print(f"Bienvenido {self.usuario}\n")

            opciones = [
                "1. Administrar Empleados",
                "2. Administrar Departamentos",
                "3. Administrar Proyectos",
                "S. Salir"
            ]

            for opcion in opciones:
                print(opcion)

            try: 
                seleccion_menu = input("\nSeleccione una opción: ").strip().lower()

                if seleccion_menu == "1":
                    menu = MenuAdministrarEmpleados()
                    menu.mostrar()
                elif seleccion_menu == "2":
                    menu = MenuAdministrarDepartamentos()
                    menu.mostrar()
                elif seleccion_menu == "3":
                    menu = MenuAdministrarProyectos()
                    menu.mostrar()
                elif seleccion_menu == "s":
                    limpiar_pantalla()
                    return
                else:
                    print("Opción no válida")
                    time.sleep(1)
                    self.mostrar()
            except:
                print("Error en la selección")
                time.sleep(1)
                self.mostrar()

# Clase de Menú de Administrar Empleados
class MenuAdministrarEmpleados:
    def __init__(self):
        self.empleado_model = EmpleadoModel()
        self.departamento_model = DepartamentoModel()

    def mostrar(self):
        limpiar_pantalla()
        print("--- Menú de Administrar Empleados ---\n")


        opciones = [
            "1. Ver Empleados",
            "2. Agregar Empleado",
            "3. Modificar Empleado",
            "4. Eliminar Empleado",
            "S. Volver"
        ]

        for opcion in opciones:
            print(opcion)

        seleccion = input("\nSeleccione una opción: ").strip().lower()

        if seleccion == "1":
            limpiar_pantalla()
            empleados = self.empleado_model.listar()
            print("\n--- Empleados ---\n")

            # Crear una tabla
            table = PrettyTable()
            
            # Definir los nombres de las columnas
            table.field_names = ["ID", "RUT", "Username", "Direccion", "Telefono", "Fecha Inicio Contrato", "Salario", "Departamento", "Rol"]

            # Agregar filas a la tabla
            for empleado in empleados:
                table.add_row([empleado[0], empleado[1], empleado[2], empleado[4], empleado[5], empleado[6], empleado[7], empleado[10], empleado[9]])
            


            # Imprimir la tabla
            print(table)

            pausar()
            self.mostrar()

        elif seleccion == "2":
            limpiar_pantalla()
            eleccion = input("¿Desea ver los departamentos que existen? s/n: ").lower().strip()

            if eleccion == "s":
                departamento_model = DepartamentoModel()
                departamentos = departamento_model.listar()

                # Crear una tabla
                table = PrettyTable()

                # Definir los nombres de las columnas
                table.field_names = ["ID", "Nombre", "Descripcion"]

                # Agregar filas a la tabla
                for departamento in departamentos:
                    table.add_row([departamento[0], departamento[1], departamento[2]])
                
                print(table)
            else:
                pass 

            print("\n--- Agregar Empleado ---\n")
            

            rut = input("RUT: ")
            username = input("Username: ")
            password = pwinput.pwinput(prompt="Password: ")
            direccion = input("Direccion: ")
            telefono = input("Telefono 9XXXXXXXX: ")
            fecha_inicio_contrato = input("Fecha Inicio Contrato YYYY-MM-DD: ")
            salario = input("Salario: ")
            departamento_id = input("Departamento ID (0 para 'No asignado'): ")
            rol = input("Rol: ")

            # Crear el objeto Empleado
            empleado = Empleado(rut, username, password, direccion, telefono, fecha_inicio_contrato, salario, departamento_id, rol)

            try:
                # Guardar el empleado en la base de datos
                self.empleado_model.crear(empleado)
                print("\nEmpleado creado exitosamente")
            except Exception as e:
                print(f"\nError al crear el empleado: {str(e)}")
            
            pausar()
            self.mostrar()

        elif seleccion == "3":
            # Pedir RUT del empleado a modificar
            limpiar_pantalla()
            print("--- Modificar Empleado ---\n")
            rut = input("Ingrese el RUT del empleado a modificar: ")

            # Buscar el empleado en la base de datos
            empleado = self.empleado_model.existe(rut)

            if empleado:
                print("\nEmpleado encontrado\n")

                # Mostrar los datos del empleado
                new_rut = input(f"RUT ({empleado[1]}): ") or empleado[1]
                new_username = input(f"Username ({empleado[2]}): ") or empleado[2]
                new_password = pwinput.pwinput(prompt="Password: ")
                # Encriptar la contraseña
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt(rounds=10)).decode('utf-8')
                new_direccion = input(f"Direccion ({empleado[4]}): ") or empleado[4]
                new_telefono = input(f"Telefono ({empleado[5]}): ") or empleado[5]
                new_fecha_inicio_contrato = input(f"Fecha Inicio Contrato ({empleado[6]}): ") or empleado[6]
                new_salario = input(f"Salario ({empleado[7]}): ") or empleado[7]
                new_departamento_id = input(f"Departamento ID ({empleado[8]}): ") or empleado[8]
                new_rol = input(f"Rol ({empleado[9]}): ") or empleado[9]

                # Crear el objeto Empleado
                empleado = Empleado(new_rut, new_username, hashed_password, new_direccion, new_telefono, new_fecha_inicio_contrato, new_salario, new_departamento_id, new_rol)

                try:
                    # Actualizar el empleado en la base de datos
                    self.empleado_model.actualizar(empleado, rut)
                    print("\nEmpleado actualizado exitosamente")
                    pausar()
                    self.mostrar()
                except Exception as e:
                    print(f"\nError al actualizar el empleado: {str(e)}")

            else:
                print("\nEmpleado no encontrado")
                pausar()
                self.mostrar()

        
        elif seleccion == "4":
            # Pedir RUT del empleado a eliminar
            limpiar_pantalla()
            print("--- Eliminar Empleado ---\n")
            rut = input("Ingrese el RUT del empleado a eliminar: ")

            # Buscar el empleado en la base de datos
            empleado = self.empleado_model.existe(rut)

            if empleado:
                print("\nEmpleado encontrado\n")

                try:
                    # Eliminar el empleado de la base de datos
                    self.empleado_model.eliminar(rut)
                    print("\nEmpleado eliminado exitosamente")
                    pausar()
                    self.mostrar()
                except Exception as e:
                    print(f"\nError al eliminar el empleado: {str(e)}")
                    pausar()
                    self.mostrar()
            else:
                print("\nEmpleado no encontrado")
                pausar()
                self.mostrar()

            
        elif seleccion == "s":
            limpiar_pantalla()
            # Retornar al menú principal
            return
        else:
            print("Opción no válida")
            time.sleep(1)
            self.mostrar()

# Clase de Menú de Administrar Departamentos
class MenuAdministrarDepartamentos:
    def mostrar(self):
        limpiar_pantalla()
        print("--- Menú de Administrar Departamentos ---\n")

        opciones = [
            "1. Ver Departamentos",
            "2. Agregar Departamento",
            "3. Modificar Departamento",
            "4. Eliminar Departamento",
            "S. Volver"
        ]

        for opcion in opciones:
            print(opcion)

        seleccion = input("\nSeleccione una opción: ").strip().lower()

        if seleccion == "1":
            limpiar_pantalla()
            print("--- Departamentos ---\n")
            
            departamento_model = DepartamentoModel()
            departamentos = departamento_model.listar()

            # Crear una tabla
            table = PrettyTable()

            # Definir los nombres de las columnas
            table.field_names = ["ID", "Nombre", "Descripcion", "ID Gerente", "Empleado", "Rol"]

            # Agregar filas a la tabla
            for departamento in departamentos:
                table.add_row([departamento[0], departamento[1], departamento[2], departamento[3], departamento[4], departamento[5]])

            # Imprimir la tabla
            print(table)

            pausar()
            self.mostrar()


            
        elif seleccion == "2":
            limpiar_pantalla()
            print("--- Agregar Departamento ---\n")

            nombre = input("Nombre: ")
            descripcion = input("Descripcion: ")
            id_gerente = input("ID Gerente (0 para 'No asignado'): ")

            # Crear el objeto Departamento
            departamento = Departamento(nombre, descripcion, id_gerente)

            try:
                # Guardar el departamento en la base de datos
                departamento_model = DepartamentoModel()
                departamento_model.crear(departamento)
                print("\nDepartamento creado exitosamente")
            except Exception as e:
                print(f"\nError al crear el departamento: {str(e)}")
            
            pausar()
            self.mostrar()
        elif seleccion == "3":
            limpiar_pantalla()
            print("--- Modificar Departamento ---\n")

            id_departamento = input("Ingrese el ID del departamento a modificar: ")

            # Buscar el departamento en la base de datos
            departamento_model = DepartamentoModel()
            departamento = departamento_model.existe(id_departamento)

            if departamento:
                print("\nDepartamento encontrado\n")

                # Mostrar los datos del departamento
                new_nombre = input(f"Nombre ({departamento[1]}): ") or departamento[1]
                new_descripcion = input(f"Descripcion ({departamento[2]}): ") or departamento[2]
                new_id_gerente = input(f"ID Gerente ({departamento[3]}): ") or departamento[3]

                # Crear el objeto Departamento
                departamento = Departamento(new_nombre, new_descripcion, new_id_gerente)

                try:
                    # Actualizar el departamento en la base de datos
                    departamento_model.actualizar(departamento, id_departamento)
                    print("\nDepartamento actualizado exitosamente")
                    pausar()
                    self.mostrar()
                except Exception as e:
                    print(f"\nError al actualizar el departamento: {str(e)}")

            else:
                print("\nDepartamento no encontrado")
                pausar()
                self.mostrar()
        elif seleccion == "4":
            limpiar_pantalla()
            print("--- Eliminar Departamento ---\n")

            id_departamento = input("Ingrese el ID del departamento a eliminar: ")

            # Buscar el departamento en la base de datos
            departamento_model = DepartamentoModel()
            departamento = departamento_model.existe(id_departamento)

            if departamento:
                print("\nDepartamento encontrado\n")

                try:
                    # Eliminar el departamento de la base de datos
                    departamento_model.eliminar(id_departamento)
                    print("\nDepartamento eliminado exitosamente")
                    pausar()
                    self.mostrar()
                except Exception as e:
                    print(f"\nError al eliminar el departamento: {str(e)}")
                    pausar()
                    self.mostrar()
            else:
                print("\nDepartamento no encontrado")
                pausar()
                self.mostrar()
        elif seleccion == "s":
            return
        else:
            print("Opción no válida")
            time.sleep(1)
            self.mostrar()

# Clase de Menú de Administrar Proyectos
class MenuAdministrarProyectos:
    def mostrar(self):
        limpiar_pantalla()
        print("--- Menú de Administrar Proyectos ---\n")

        opciones = [
            "1. Ver Proyectos",
            "2. Agregar Proyecto",
            "3. Modificar Proyecto",
            "4. Eliminar Proyecto",
            "S. Volver"
        ]

        for opcion in opciones:
            print(opcion)

        seleccion = input("\nSeleccione una opción: ").strip().lower()

        if seleccion == "1":
            limpiar_pantalla()
            print("--- Proyectos ---\n")
            
            proyecto_model = ProyectoModel()
            proyectos = proyecto_model.listar()

            # Crear una tabla
            table = PrettyTable()

            # Definir los nombres de las columnas
            table.field_names = ["ID", "Nombre", "Descripcion", "Fecha Inicio", "Fecha Fin"]

            # Agregar filas a la tabla
            for proyecto in proyectos:
                table.add_row([proyecto[0], proyecto[1], proyecto[2], proyecto[3], proyecto[4]])

            # Imprimir la tabla
            print(table)

            pausar()
            self.mostrar()
            
        elif seleccion == "2":
            limpiar_pantalla()
            print("--- Agregar Proyecto ---\n")

            nombre = input("Nombre: ")
            descripcion = input("Descripcion: ")
            fecha_inicio = input("Fecha Inicio YYYY-MM-DD: ")
            fecha_fin = input("Fecha Fin YYYY-MM-DD: ")

            # Crear el objeto Proyecto
            proyecto = Proyecto(nombre, descripcion, fecha_inicio, fecha_fin)

            try:
                # Guardar el proyecto en la base de datos
                proyecto_model = ProyectoModel()
                proyecto_model.crear(proyecto)
                print("\nProyecto creado exitosamente")

            except Exception as e:
                print(f"\nError al crear el proyecto: {str(e)}")
            
            pausar()
            self.mostrar()
        elif seleccion == "3":
            limpiar_pantalla()
            print("--- Modificar Proyecto ---\n")

            id = input("Ingrese el ID del proyecto a modificar: ")

            # Buscar el proyecto en la base de datos
            proyecto_model = ProyectoModel()
            proyecto = proyecto_model.existe(id)

            if proyecto:
                print("\nProyecto encontrado\n")

                # Mostrar los datos del proyecto
                new_nombre = input(f"Nombre ({proyecto[1]}): ") or proyecto[1]
                new_descripcion = input(f"Descripcion ({proyecto[2]}): ") or proyecto[2]
                new_fecha_inicio = input(f"Fecha Inicio ({proyecto[3]}): ") or proyecto[3]
                new_fecha_fin = input(f"Fecha Fin ({proyecto[4]}): ") or proyecto[4]

                # Crear el objeto Proyecto
                proyecto = Proyecto(new_nombre, new_descripcion, new_fecha_inicio, new_fecha_fin)

                try:
                    # Actualizar el proyecto en la base de datos
                    proyecto_model.actualizar(proyecto, id)
                    print("\nProyecto actualizado exitosamente")
                    pausar()
                    self.mostrar()

                except Exception as e:
                    print(f"\nError al actualizar el proyecto: {str(e)}")

            else:
                print("\nProyecto no encontrado")
                pausar()
                self.mostrar()
        elif seleccion == "4":
            limpiar_pantalla()
            print("--- Eliminar Proyecto ---\n")

            id = input("Ingrese el ID del proyecto a eliminar: ")

            # Buscar el proyecto en la base de datos
            proyecto_model = ProyectoModel()
            proyecto = proyecto_model.existe(id)

            if proyecto:
                print("\nProyecto encontrado\n")

                try:
                    # Eliminar el proyecto de la base de datos
                    proyecto_model.eliminar(id)
                    print("\nProyecto eliminado exitosamente")
                    pausar()
                    self.mostrar()
                except Exception as e:
                    print(f"\nError al eliminar el proyecto: {str(e)}")
                    pausar()
                    self.mostrar()
            else:
                print("\nProyecto no encontrado")
                pausar()
                self.mostrar()
        elif seleccion == "s":
            return
        else:
            print("Opción no válida")
            time.sleep(1)
            self.mostrar()

# Clase de Menú de Gerente
class MenuGerente:
    def __init__(self, usuario):
        self.usuario = usuario

    def mostrar(self):
        while True:
            limpiar_pantalla()
            print("--- Menú de Gerente ---\n")

            opciones = [
                "1. Asignar Empleados a proyectos",
                "2. Asignar Empleados a Departamentos",
                "3. Administrar Proyectos",
                "S. Salir"
            ]

            for opcion in opciones:
                print(opcion)

            try: 
                seleccion_menu = input("\nSeleccione una opción: ").strip().lower()

                if seleccion_menu == "1":
                    en_desarrollo()
                elif seleccion_menu == "2":
                    en_desarrollo()
                elif seleccion_menu == "3":
                    en_desarrollo()
                elif seleccion_menu == "s":
                    limpiar_pantalla()
                    return
                else:
                    print("Opción no válida")
                    time.sleep(1)
                    self.mostrar()
            except:
                print("Error en la selección")
                time.sleep(1)
                self.mostrar()

# Clase de Menú de Empleado
class MenuEmpleado:
    def __init__(self, usuario):
        self.usuario = usuario

    def mostrar(self):
        limpiar_pantalla()
        print("--- Menú de Empleado ---\n")

        opciones = [
            "1. Ver Proyectos",
            "2. Ver Departamentos",
            "S. Salir"
        ]

        for opcion in opciones:
            print(opcion)

        seleccion = input("\nSeleccione una opción: ").strip().lower()

        if seleccion == "1":
            en_desarrollo()
        elif seleccion == "2":
            en_desarrollo()
        elif seleccion == "s":
            limpiar_pantalla()
            return
        else:
            print("Opción no válida")
            time.sleep(1)
            self.mostrar()


# Funciones Helper
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input("\nPresione Enter para continuar...")   

def en_desarrollo():
    print("Funcion en desarrollo :c")
    pausar()


# Si el archivo es ejecutado directamente se ejecuta el menú principal
if __name__ == '__main__':
    # bypass para no tener que logearse
    menu = MenuAdmin("admin")
    menu.mostrar()

