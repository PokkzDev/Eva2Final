"""
    Este archivo se encarga de manejar las vistas de la aplicación. #test
"""

# Importar Modulos
from modules.auth import Auth
from modules.modelo import Empleado, EmpleadoModel, Departamento, DepartamentoModel, Proyecto, ProyectoModel, Registro, RegistroModel, Informe, InformeModel
import pwinput
import os
import time
from prettytable import PrettyTable
import bcrypt
import datetime

# Clase de Menú Principal
class MenuPrincipal:
    def mostrar(self):
        limpiar_pantalla()
        print("--- Menú Principal ---\n")

        usuario = input("Ingrese su usuario: ")
        password = pwinput.pwinput(prompt="Ingrese su contraseña: ")

        auth = Auth()

        try:

            user = auth.iniciar_sesion(usuario, password)
            
            
            if user:
                print("\nUsuario autenticado")
                time.sleep(1)
               #

                
                if user[2] == "usuario":
                    print(user)
                    pausar()
                    menu = MenuEmpleado(user[1], user[2])
                    menu.mostrar()
                elif user[2] == "admin":
                    print(user)
                    pausar()
                    menu = MenuAdmin(user[1], user[2])
                    menu.mostrar()
                else:
                    print(user)
                    pausar()
                    menu = MenuGerente(user[1], user[2], user[3])
                    menu.mostrar()
                
            else:
                print("\nCreedenciales incorrectas")
                time.sleep(1)
                self.mostrar()
        except:
            print("\nError en la autenticación")
            pausar()
            time.sleep(1)
            self.mostrar()

# Clase de Menú de Administrador
class MenuAdmin:
    def __init__(self, usuario, rol):
        self.usuario = usuario.capitalize()
        self.rol = rol
      
    def mostrar(self):
        while True:
            limpiar_pantalla()
            
            print("--- Menú de Administrador ---\n")
            print(f"Bienvenido, {self.usuario}!\n")

            opciones = [
                "1. Administrar Empleados",
                "2. Administrar Departamentos",
                "3. Administrar Proyectos",
                "4. Administrar Registros de Tiempo",
                "5. Administrar Informes",
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
                elif seleccion_menu == "4":
                    menu = MenuAdministrarRegistros()
                    menu.mostrar()
                elif seleccion_menu == "5":
                    menu = MenuAdministrarInformes()
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
            table.field_names = ["ID", "RUT", "Username", "Direccion", "Telefono", "Fecha Inicio Contrato", "Salario", "Rol"]

            # Agregar filas a la tabla
            for empleado in empleados:
                table.add_row([empleado[0], empleado[1], empleado[2], empleado[4], empleado[5], empleado[6], empleado[7], empleado[9]])
            


            # Imprimir la tabla
            print(table)

            pausar()
            self.mostrar()

        elif seleccion == "2":
            limpiar_pantalla()
            eleccion = input("¿Sabe los ID de los departamentos? s/n: ").lower().strip()

            
            if eleccion != "s":
                departamento_model = DepartamentoModel()
                departamentos = departamento_model.listar()


                if departamentos != []:
                    # Crear una tabla
                    table = PrettyTable()

                    # Definir los nombres de las columnas
                    table.field_names = ["ID", "Nombre", "Descripcion"]

                    # Agregar filas a la tabla
                    for departamento in departamentos:
                        table.add_row([departamento[0], departamento[1], departamento[2]])
                    
                    print(table)

                else:
                    print("No hay departamentos registrados")
                    time.sleep(1)
                    self.mostrar()


            print("\n--- Agregar Empleado ---\n")
            
            while True:
                rut = input("RUT: ")
                if "-" not in rut:
                    print("No tiene digito verificador")
                
                partes = rut.split("-")
                
                if len(partes) != 2:
                    print("No contiene un digito verificador")
                
                try:
                    numero, digito_verificador = partes
                    # Verificar que la longitud del número esté entre 7 y 8 y que contenga solo dígitos
                    if not (7 <= len(numero) <= 8 and numero.isdigit()):
                        print("El rut no tiene el largo requerido\n 7 u 8 digitos sin contar el digito verificador separado por un '-'")
                        continue
                    # Validar que el dígito verificador tenga exactamente un carácter y sea un número del 0 al 9 o 'k'
                    if len(digito_verificador) != 1 or not (digito_verificador.isdigit() or digito_verificador.lower() == 'k'):
                        print("no es un digito verificador valido")
                        continue
                except:
                    print()
                    continue
                if rut.strip():
                    break
                else:
                    print("El rut no puede estar vacio")
            while True:
                username = input("Username: ")
                if username.strip():
                    break
                else:
                    print("El username no puede estar vacio")
            while True:
                password = pwinput.pwinput(prompt="Password: ")

                # Si contraseña esta vacia
                if not password.strip():
                    print("La contraseña no puede estar vacía.")
                    continue

                password2 = pwinput.pwinput(prompt="Confirme el Password: ") 

                # Si contraseña esta vacia
                if not password2.strip():
                    print("La contraseña no puede estar vacía.")
                    continue

                # Validar que la contraseña sea válida y coincida
                if password != password2:
                    print("Las contraseñas no coinciden.")
                    
                    continue
                else:
                    break
                    

            while True:
                direccion = input("Direccion: ")
                if direccion.strip():
                    break
                else:
                    print("La direccion no puede estar vacia")
            while True:
                telefono = input("Telefono 9XXXXXXXX: ")
                telefono = telefono.strip()
                try:
                    if telefono.startswith("9"):
                        if len(telefono) == 9:
                            telefono = int(telefono)
                            break
                        else:
                            print("No tiene la cantidad de numeros correspondiente a un telefono")
                    else:
                        print("Usted no ingreso el formato correcto de un telefono")
                except:
                        print("Usted no ingreso el formato correcto de un telefono")
            while True:
                fecha_contrato = input("Fecha Inicio Contrato DD-MM-YYYY: ")
                try:
                    fecha_inicio_contrato = datetime.datetime.strptime(fecha_contrato, '%d-%m-%Y')
                    break
                except:
                    print("Usted no igreso una fecha")
            while True:
                salario = input("Salario: ")
                try:
                    if salario.strip():
                        salario = float(salario)
                        break
                    else:
                        print("El salario no puede estar vacio")
                except:
                    print("Esto no es un digito")

            while True:
                departamento_id = input("Departamento ID (0 para 'No asignado'): ")
                try:
                    if departamento_id.strip():
                        if departamento_id.isdigit():
                            break
                    else:
                        print("Ingrese una opcion valida")
                except:
                    print("Usted no agrego un ID valido")

            while True:
                rol = input("Rol: ")
                if rol.strip():
                    if rol == "admin" or rol == "usuario" or rol == "gerente":
                        break
                    else:
                        print("Usted no ingreso un rol existente")
                else:
                    print("Usted debe ingresar un rol")

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

                while True: # Ingreso del nuevo rut en caso que lo requiera
                    # Mostrar los datos del empleado
                    new_rut = input(f"RUT ({empleado[1]}): ") or empleado[1]

                    if "-" not in new_rut:
                        print("No tiene digito verificador")
                    partes = new_rut.split("-")
                    
                    if len(partes) != 2:
                        print("No contiene un digito verificador")
                    
                    try:
                        numero, digito_verificador = partes
                        # Verificar que la longitud del número esté entre 7 y 8 y que contenga solo dígitos
                        if not (7 <= len(numero) <= 8 and numero.isdigit()):
                            print("El rut no tiene el largo requerido\n 7 u 8 digitos sin contar el digito verificador separado por un '-'")
                            continue
                        # Validar que el dígito verificador tenga exactamente un carácter y sea un número del 0 al 9 o 'k'
                        if len(digito_verificador) != 1 or not (digito_verificador.isdigit() or digito_verificador.lower() == 'k'):
                            print("no es un digito verificador valido")
                            continue
                    except:
                        print()
                        continue
                    if rut.strip():
                        break
                    else:
                        print("El rut no puede estar vacio")


                while True: # ingreso nuevo username si requiere cambiarse
                    new_username = input(f"Username ({empleado[2]}): ") or empleado[2]
                    if new_username.strip():
                        break
                    else:
                        print("El username no puede estar vacio")

                new_password = pwinput.pwinput(prompt="Password: ")
                # Encriptar la contraseña
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt(rounds=10)).decode('utf-8')

                while True: # Ingreso de nueva direccion en caso de que lo requiera
                    new_direccion = input(f"Direccion ({empleado[4]}): ") or empleado[4]
                    if new_direccion.strip():
                        break
                    else:
                        print("La direccion no puede estar vacia")

                while True: # Ingreso de un nuevo telefono en caso que lo requiera
                    new_telefono = input(f"Telefono ({empleado[5]}): ") or empleado[5]
                    new_telefono = new_telefono.strip()
                    try:
                        if new_telefono.startswith("9"):

                            if len(new_telefono) == 9:
                                new_telefono = int(new_telefono)
                                break
                            else:
                                print("No tiene la cantidad de numeros correspondiente a un telefono")
                        else:
                            print("Usted no ingreso el formato correcto de un telefono")
                    except:
                            print("Usted no ingreso el formato correcto de un telefono")

                while True:
                    new_fecha_contrato = input(f"Fecha Inicio Contrato ({empleado[6]}): ") or empleado[6]
                    try:
                        new_fecha_inicio_contrato = datetime.datetime.strptime(new_fecha_contrato, '%d-%m-%Y')
                        break
                    except:
                        print("No ingreso el formato de fecha")

                while True:
                    new_salario = input(f"Salario ({empleado[7]}): ") or empleado[7]
                    try:
                        new_salario = str(new_salario)
                        if new_salario.strip():
                            new_salario = float(new_salario)
                            break
                        else:
                            print("El salario no puede estar vacio")
                    except:
                        print("Esto no es un digito")


                new_departamento_id = input(f"Departamento ID ({empleado[8]}): ") or empleado[8]


                while True:
                    new_rol = input(f"Rol (admin, gerente, usuario): ") or empleado[9]
                    
                    roles = ["admin", "usuario", "gerente"]

                    if new_rol in roles:
                        break
                    else:
                        print("Usted no ingreso un rol existente")

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
            "1. Administrar Departamentos",
            "2. Administrar Empleados de Departamento",
        ]
        
        for opcion in opciones:
            print(opcion)


        seleccion = input("\nSeleccione una opción: ").strip().lower()

        if seleccion == "1":
            limpiar_pantalla()
            print("--- Menú de Departamentos ---\n")

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

        elif seleccion == "2":
            limpiar_pantalla()
            print("--- Menú de Empleados de Departamento ---\n")
            opciones = [
                "1. Ver Empleados por Departamento",
                "2. Asignar Empleados a Departamento",
                "3. Modificar Empleados de Departamento",
                "4. Eliminar Empleados de Departamento",
                "S. Volver"
            ]

            for opcion in opciones:
                print(opcion)

            seleccion = input("\nSeleccione una opción: ").strip().lower()

            if seleccion == "1":
                limpiar_pantalla()
                print("--- Empleados por Departamento ---\n")

                departamento_id = input("Ingrese el ID del departamento: ")

                # Buscar el departamento en la base de datos
                departamento_model = DepartamentoModel()
                departamento = departamento_model.existe(departamento_id)

                if departamento:
                    print("\nDepartamento encontrado\n")

                    empleados = departamento_model.listar_empleados(departamento_id)

                    # Crear una tabla
                    table = PrettyTable()

                    # Definir los nombres de las columnas
                    table.field_names = ["ID", "RUT", "Username", "Direccion", "Telefono", "Fecha Inicio Contrato", "Salario", "Rol"]

                    # Agregar filas a la tabla
                    for empleado in empleados:
                        table.add_row([empleado[0], empleado[1], empleado[2], empleado[4], empleado[5], empleado[6], empleado[7], empleado[9]])

                    # Imprimir la tabla
                    print(table)
                    pausar()
                    self.mostrar()
                else:
                    print("\nDepartamento no encontrado")
                    pausar()
                    self.mostrar()
            
            # Asignar Empleados a Departamento
            elif seleccion == "2":
                limpiar_pantalla()
                print("--- Asignar Empleados a Departamento ---\n")

                empleado_id = input("ID Empleado: ")
                departamento_id = input("ID Departamento: ")

                # a INT
                empleado_id = int(empleado_id)
                departamento_id = int(departamento_id)

                try:
                    # Asignar el empleado al departamento
                    departamento_model = DepartamentoModel()
                    if departamento_model.asignar_empleado(empleado_id, departamento_id):
                        print("\nEmpleado asignado exitosamente")
                    else:
                        print("\nEmpleado ya esta asignado a un departamento")
                        
                except Exception as e:
                    print(f"\nError al asignar el empleado: {str(e)}")
                
                pausar()
                self.mostrar()
            
            # Modificar Empleados de Departamento
            elif seleccion == "3":
                limpiar_pantalla()
                print("--- Modificar Empleados de Departamento ---\n")

                empleado_id = input("ID Empleado: ")
                departamento_id = input("ID Departamento al que se asignara: ")

                # a INT
                empleado_id = int(empleado_id)
                departamento_id = int(departamento_id)

                try:
                    # Modificar el empleado del departamento
                    departamento_model = DepartamentoModel()
                    departamento_model.modificar_empleado(empleado_id, departamento_id)
                    print("\nEmpleado modificado exitosamente")
                except Exception as e:
                    print(f"\nError al modificar el empleado: {str(e)}")
                
                pausar()
                self.mostrar()
            
            # Eliminar Empleados de Departamento
            elif seleccion == "4":
                limpiar_pantalla()
                print("--- Eliminar Empleados de Departamento ---\n")

                empleado_id = input("ID Empleado: ")
                

                try:
                    # Eliminar el empleado del departamento
                    departamento_model = DepartamentoModel()
                    departamento_model.eliminar_empleado(empleado_id)
                    print("\nEmpleado eliminado exitosamente")

                except Exception as e:
                    print(f"\nError al eliminar el empleado: {str(e)}")
                
                pausar()
                self.mostrar()

            elif seleccion == "s":
                return
            else:
                print("Opción no válida")
                time.sleep(1)
                self.mostrar()

        elif seleccion == "s":
            return
        

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

            try:
                nombre = input("Nombre: ")
                descripcion = input("Descripcion: ")

                while True:
                    try:
                        fecha_inicio = input("Fecha Inicio DD-MM-YYYY: ")
                        fecha_inicio = datetime.datetime.strptime(fecha_inicio, '%d-%m-%Y')

                        fecha_fin = input("Fecha Fin DD-MM-YYYY: ")
                        fecha_fin = datetime.datetime.strptime(fecha_fin, '%d-%m-%Y')

                        if fecha_fin > fecha_inicio:
                            break
                        else:
                            print("Error: La fecha de término no puede ser anterior a la fecha de inicio.")
                    except ValueError:
                        print("Error: Formato de fecha incorrecto. Use DD-MM-YYYY.")
            except Exception as e:
                print(f"Error al ingresar datos: {str(e)}")
                pausar()
                self.mostrar()

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
                while True:
                    new_fecha_inicio = input(f"Fecha Inicio ({proyecto[3]}): ") or proyecto[3]
                    try:
                        new_fecha_inicio = datetime.datetime.strptime(new_fecha_inicio, '%d-%m-%Y')

                    except:
                        print("No ingreso el formato de fecha")

                    new_fecha_fin = input(f"Fecha Fin ({proyecto[4]}): ") or proyecto[4]
                    try:
                        new_fecha_fin = datetime.datetime.strptime(new_fecha_fin, '%d-%m-%Y')
                        diferencia_fechas = new_fecha_fin - new_fecha_inicio
                        diferencia_fechas = diferencia_fechas.days
                
                        if diferencia_fechas > 0:
                            break
                        else:
                            print("No puede ser la fecha de termino anterior a la de inicio")
                    except:
                        print("No ingreso el formato de fecha")


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

# Clase de Menú de Administrar Registros
class MenuAdministrarRegistros:
    def mostrar(self):
        limpiar_pantalla()
        print("--- Menú de Administrar Registros ---\n")

        opciones = [
            "1. Ver Registros",
            "2. Agregar Registro",
            "3. Modificar Registro",
            "4. Eliminar Registro",
            "S. Volver"
        ]

        for opcion in opciones:
            print(opcion)

        seleccion = input("\nSeleccione una opción: ").strip().lower()

        if seleccion == "1":
            limpiar_pantalla()
            print("--- Registros de Tiempo ---\n")
            
            registro_model = RegistroModel()
            registros = registro_model.listar()

            # Crear una tabla
            table = PrettyTable()

            # Definir los nombres de las columnas
            table.field_names = ["ID", "Username", "Nombre Proyecto", "Fecha", "Horas Trabajadas", "Tarea Descrita"]
            
            # Transformar la fecha a un formato más legible
            for registro in registros:
                fecha = registro[3].strftime("%d-%m-%Y")
                table.add_row([registro[0], registro[1], registro[2], fecha, registro[4], registro[5]])
            
            # Imprimir la tabla
            print(table)

            pausar()
            self.mostrar()  

        elif seleccion == "2":
            limpiar_pantalla()
            print("--- Agregar Registro ---\n")

            empleado_id = input("ID Empleado: ")
            proyecto_id = input("ID Proyecto: ")
            
            while True:
                fecha = input("Fecha YYYY-MM-DD: ")
                try:
                    fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d')
                    break
                except:
                    print("No ingreso el formato de fecha")

            horas_trabajadas = input("Horas Trabajadas: ")
            descripcion_tareas = input("Descripcion de Tareas: ")

            # Crear el objeto Registro
            registro = Registro(empleado_id, proyecto_id, fecha, horas_trabajadas, descripcion_tareas)

            try:
                # Guardar el registro en la base de datos
                registro_model = RegistroModel()
                registro_model.crear(registro)
                print("\nRegistro creado exitosamente")

            except Exception as e:
                print(f"\nError al crear el registro: {str(e)}")
            
            pausar()
            self.mostrar()
        elif seleccion == "3":
            limpiar_pantalla()
            print("--- Modificar Registro ---\n")

            id = input("Ingrese el ID del registro a modificar: ")

            # Buscar el registro en la base de datos
            registro_model = RegistroModel()
            registro = registro_model.existe(id)

            if registro:
                print("\nRegistro encontrado\n")

                # Mostrar los datos del registro
                new_empleado_id = input(f"ID Empleado ({registro[1]}): ") or registro[1]
                new_proyecto_id = input(f"ID Proyecto ({registro[2]}): ") or registro[2]
                new_fecha = input(f"Fecha ({registro[3]}): ") or registro[3]
                new_horas_trabajadas = input(f"Horas Trabajadas ({registro[4]}): ") or registro[4]
                new_descripcion_tareas = input(f"Descripcion de Tareas ({registro[5]}): ") or registro[5]

                # Crear el objeto Registro
                registro = Registro(new_empleado_id, new_proyecto_id, new_fecha, new_horas_trabajadas, new_descripcion_tareas)

                try:
                    # Actualizar el registro en la base de datos
                    registro_model.actualizar(registro, id)
                    print("\nRegistro actualizado exitosamente")
                    pausar()
                    self.mostrar()

                except Exception as e:
                    print(f"\nError al actualizar el registro: {str(e)}")

            else:
                print("\nRegistro no encontrado")
                pausar()
                self.mostrar()
        elif seleccion == "4":
            limpiar_pantalla()
            print("--- Eliminar Registro ---\n")

            id = input("Ingrese el ID del registro a eliminar: ")

            # Buscar el registro en la base de datos
            registro_model = RegistroModel()
            registro = registro_model.existe(id)

            if registro:
                print("\nRegistro encontrado\n")

                try:
                    # Eliminar el registro de la base de datos
                    registro_model.eliminar(id)
                    print("\nRegistro eliminado exitosamente")
                    pausar()
                    self.mostrar()
                except Exception as e:
                    print(f"\nError al eliminar el registro: {str(e)}")
                    pausar()
                    self.mostrar()
            else:
                print("\nRegistro no encontrado")
                pausar()
                self.mostrar()

        elif seleccion == "s":
            return

# Clase de Menú de Informes
class MenuAdministrarInformes:
    """
        CREATE TABLE informe (
        id INT AUTO_INCREMENT PRIMARY KEY,
        titulo VARCHAR(100) NOT NULL,
        descripcion TEXT NOT NULL,
        fecha DATE NOT NULL,
        empleado_id INT NOT NULL,
        proyecto_id INT NOT NULL,
        FOREIGN KEY (empleado_id) REFERENCES empleados(id) ON DELETE CASCADE,
        FOREIGN KEY (proyecto_id) REFERENCES proyectos(id) ON DELETE CASCADE,
        INDEX (empleado_id),
        INDEX (proyecto_id)
        );
    """
    def mostrar(self):
        limpiar_pantalla()
        print("--- Menú de Informes ---\n")

        opciones = [
            "1. Ver Informes",
            "2. Agregar Informe",
            "3. Modificar Informe",
            "4. Eliminar Informe",
            "S. Volver"
        ]

        for opcion in opciones:
            print(opcion)

        seleccion = input("\nSeleccione una opción: ").strip().lower()

        if seleccion == "1":
            limpiar_pantalla()
            print("--- Informes ---\n")
            
            informe_model = InformeModel()
            informes = informe_model.listar()

            # Crear una tabla
            table = PrettyTable()

            # Definir los nombres de las columnas
            table.field_names = ["ID", "Username", "Nombre Proyecto", "Titulo", "Descripcion", "Fecha"]

            # Agregar filas a la tabla
            for informe in informes:
                table.add_row([informe[0], informe[1], informe[2], informe[4], informe[5], informe[3]])

            # Imprimir la tabla
            print(table)

            pausar()
            self.mostrar()

        elif seleccion == "2":
            limpiar_pantalla()
            print("--- Agregar Informe ---\n")

            titulo = input("Titulo: ")
            descripcion = input("Descripcion: ")
            while True:
                try:
                    fecha = input("Fecha YYYY-MM-DD: ")
                    fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d')
                    break
                except:
                    print("No ingreso el formato de fecha")

            empleado_id = input("ID Empleado: ")
            proyecto_id = input("ID Proyecto: ")

            # Crear el objeto Informe
            informe = Informe(titulo, descripcion, fecha, empleado_id, proyecto_id)

            try:
                # Guardar el informe en la base de datos
                informe_model = InformeModel()
                informe_model.crear(informe)
                print("\nInforme creado exitosamente")

            except Exception as e:
                print(f"\nError al crear el informe: {str(e)}")
            
            pausar()
            self.mostrar()

        elif seleccion == "3":
            limpiar_pantalla()
            print("--- Modificar Informe ---\n")

            id = input("Ingrese el ID del informe a modificar: ")

            # Buscar el informe en la base de datos
            informe_model = InformeModel()
            informe = informe_model.existe(id)

            if informe:
                print("\nInforme encontrado\n")

                # Mostrar los datos del informe
                new_titulo = input(f"Titulo ({informe[1]}): ") or informe[1]
                new_descripcion = input(f"Descripcion ({informe[2]}): ") or informe[2]
                new_fecha = input(f"Fecha ({informe[3]}): ") or informe[3]
                new_empleado_id = input(f"ID Empleado ({informe[4]}): ") or informe[4]
                new_proyecto_id = input(f"ID Proyecto ({informe[5]}): ") or informe[5]

                # Crear el objeto Informe
                informe = Informe(new_titulo, new_descripcion, new_fecha, new_empleado_id, new_proyecto_id)

                try:
                    # Actualizar el informe en la base de datos
                    informe_model.actualizar(informe, id)
                    print("\nInforme actualizado exitosamente")
                    pausar()
                    self.mostrar()

                except Exception as e:
                    print(f"\nError al actualizar el informe: {str(e)}")

            else:
                print("\nInforme no encontrado")
                pausar()
                self.mostrar()
        
        elif seleccion == "4":
            limpiar_pantalla()
            print("--- Eliminar Informe ---\n")

            id = input("Ingrese el ID del informe a eliminar: ")

            # Buscar el informe en la base de datos
            informe_model = InformeModel()
            informe = informe_model.existe(id)

            if informe:
                print("\nInforme encontrado\n")

                try:
                    # Eliminar el informe de la base de datos
                    informe_model.eliminar(id)
                    print("\nInforme eliminado exitosamente")
                    pausar()
                    self.mostrar()
                except Exception as e:
                    print(f"\nError al eliminar el informe: {str(e)}")
                    pausar()
                    self.mostrar()
            else:
                print("\nInforme no encontrado")
                pausar()
                self.mostrar()
        
# Clase de Menú de Gerente
class MenuGerente:
    def __init__(self, usuario, departamento_id, rol):
        self.usuario = usuario
        self.departamento_id = departamento_id
        self.rol = rol

    def mostrar(self):
        while True:
            limpiar_pantalla()
            print("--- Menú de Gerente ---\n")

            opciones = [
                "1. Gestionar empleados en departamentos designado",
                "2. Administrar Proyectos",
                "3. Registrar horario",
                "4. Administrar informes",
                "S. Salir"
            ]

            for opcion in opciones:
                print(opcion)

            try: 
                seleccion_menu = input("\nSeleccione una opción: ").strip().lower()

                if seleccion_menu == "1":
                    menu = MenuGerenteEmpleadosDepartamentos(self.usuario, self.departamento_id, self.rol)
                    menu.mostrar()
                elif seleccion_menu == "2":
                    menu = MenuAdministrarProyectos()
                    menu.mostrar()
                elif seleccion_menu == "3":
                    menu = MenuGestionarRegistros(self.usuario, self.departamento_id, self.rol)
                    menu.mostrar()
                elif seleccion_menu == "4":
                    menu = MenuAdministrarInformes()
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

# Menu de gerente para Administrar Empleados en su departamento
class MenuGerenteEmpleadosDepartamentos:
    def __init__(self, usuario, departamento_id, rol):
        self.usuario = usuario
        self.departamento_id = departamento_id
        self.rol = rol
        self.empleado_model = EmpleadoModel()
    
    def mostrar(self):
        limpiar_pantalla()

        print("--- Menú de Gestionar Empleados en Departamento asignado ---\n")

        opciones = [
            "1. Mostrar Empleados en Departamento asignado",
            "2. Agregar Empleados en Departamento asignado",
            "3. Eliminar Empleados en Departamento asignado",
            
            "S. Volver"
        ]

        for opcion in opciones:
            print(opcion)

        seleccion = input("\nSeleccione una opción: ").strip().lower()

        # Ver Departamentos

        if seleccion == "1":
            limpiar_pantalla()
            print("--- Empleados por Departamento ---\n")

            departamento_id = self.departamento_id

            # Buscar el departamento en la base de datos
            departamento_model = DepartamentoModel()
            departamento = departamento_model.existe(departamento_id)

            if departamento:
                print("\nDepartamento encontrado\n")

                empleados = departamento_model.listar_empleados(departamento_id)

                # Crear una tabla
                table = PrettyTable()

                # Definir los nombres de las columnas
                table.field_names = ["ID", "RUT", "Username", "Direccion", "Telefono", "Fecha Inicio Contrato", "Salario", "Rol"]

                # Agregar filas a la tabla
                for empleado in empleados:
                    table.add_row([empleado[0], empleado[1], empleado[2], empleado[4], empleado[5], empleado[6], empleado[7], empleado[9]])

                # Imprimir la tabla
                print(table)
                pausar()
                self.mostrar()
            else:
                print("\nDepartamento no encontrado")
                pausar()
                self.mostrar()
        
        # Asignar Empleados a Departamento
        elif seleccion == "2":
            limpiar_pantalla()
            print("--- Asignar Empleados a Departamento ---\n")
            empleados = self.empleado_model.listar()
            print("\n--- Empleados ---\n")

            # Crear una tabla
            table = PrettyTable()
            empleados_desasignados = []
            
            # Definir los nombres de las columnas
            table.field_names = ["ID", "Username", "ID Departamento", "Rol"]

            # Agregar filas a la tabla
            for empleado in empleados:
                if empleado[10] == None and empleado[9] != "gerente" and empleado[9] != "admin":
                    table.add_row([empleado[0], empleado[2], empleado[10], empleado[9]])
                    empleados_desasignados.append(empleado[0])


            # Imprimir la tabla
            print(table)

            while True:

                empleado_id = input("ID Empleado: ")
                departamento_id = self.departamento_id

                # a INT
                empleado_id = int(empleado_id)
                departamento_id = int(departamento_id)

                try:
                    if empleado_id not in empleados_desasignados:
                        print("Empleado ya esta asignado a un departamento")
                    else:
                        # Asignar el empleado al departamento
                        departamento_model = DepartamentoModel()
                        if departamento_model.asignar_empleado(empleado_id, departamento_id):
                            print("\nEmpleado asignado exitosamente")
                            break
                        else:
                            print("\nEmpleado ya esta asignado a un departamento")
                            break
                    
                except Exception as e:
                    print(f"\nError al asignar el empleado: {str(e)}")
                
            pausar()
            self.mostrar()



        # Eliminar Empleados de Departamento
        elif seleccion == "3":
            limpiar_pantalla()
            print("--- Eliminar Empleados de Departamento ---\n")
            departamento_id = self.departamento_id
            empleados = self.empleado_model.listar()
            print("\n--- Empleados ---\n")

            # Crear una tabla
            table = PrettyTable()
            empleados_desasignados = []
            
            # Definir los nombres de las columnas
            table.field_names = ["ID", "Username", "ID Departamento", "Rol"]

            # Agregar filas a la tabla
            for empleado in empleados:
                if empleado[10] == departamento_id and empleado[9] != "gerente":
                    table.add_row([empleado[0], empleado[2], empleado[10], empleado[9]])
                    empleados_desasignados.append(empleado[0])


            # Imprimir la tabla
            print(table)

            empleado_id = input("ID Empleado: ")
            

            try:
                # Eliminar el empleado del departamento
                departamento_model = DepartamentoModel()
                #AGREGAR IF TRUE
                departamento_model.eliminar_empleado(empleado_id)
                print("\nEmpleado eliminado exitosamente")

            except Exception as e:
                print(f"\nError al eliminar el empleado: {str(e)}")
            
            pausar()
            self.mostrar()

        elif seleccion == "s":
            return
        else:
            print("Opción no válida")
            time.sleep(1)
            self.mostrar()

# Menu de Gerente para Gestionar Los registros de su tiempo
class MenuGestionarRegistros:
    def __init__(self, usuario, departamento_id, rol):
        self.usuario = usuario
        self.departamento_id = departamento_id
        self.rol = rol
        self.empleado_model = EmpleadoModel()

    def mostrar(self):
        limpiar_pantalla()
        print("--- Menú de Administrar Registros ---\n")

        opciones = [
            "1. Ver Registros",
            "2. Agregar Registro",
            "3. Modificar Registro",
            "S. Volver"
        ]

        for opcion in opciones:
            print(opcion)

        seleccion = input("\nSeleccione una opción: ").strip().lower()

        if seleccion == "1":
            limpiar_pantalla()
            print("--- Registros de Tiempo ---\n")

            usuario = self.usuario
            
            registro_model = RegistroModel()
            registros = registro_model.listar()

            # Crear una tabla
            table = PrettyTable()

            # Definir los nombres de las columnas
            table.field_names = ["ID", "Username", "Nombre Proyecto", "Fecha", "Horas Trabajadas", "Tarea Descrita"]
            
            # Transformar la fecha a un formato más legible
            for registro in registros:
                if registro[1] == usuario:
                    fecha = registro[3].strftime("%d-%m-%Y")
                    table.add_row([registro[0], registro[1], registro[2], fecha, registro[4], registro[5]])
            
            # Imprimir la tabla
            print(table)

            pausar()
            self.mostrar()  

        elif seleccion == "2":
            limpiar_pantalla()
            print("--- Agregar Registro ---\n")
            empleados = self.empleado_model.listar()
            table = PrettyTable()
            usuario = self.usuario

            # Definir los nombres de las columnas
            table.field_names = ["ID", "RUT", "Username", "Direccion", "Telefono", "Fecha Inicio Contrato", "Salario", "Rol"]
            
            for empleado in empleados:
                if empleado[2] == usuario:
                    table.add_row([empleado[0], empleado[1], empleado[2], empleado[4], empleado[5], empleado[6], empleado[7], empleado[9]])
                    empleado_propio = empleado[0]

            empleado_id = empleado_propio
            proyecto_id = input("ID Proyecto: ")
            
            while True:
                fecha = input("Fecha DD-MM-YYYY: ")
                try:
                    fecha = datetime.datetime.strptime(fecha, '%d-%m-%Y')
                    break
                except:
                    print("No ingreso el formato de fecha")

            horas_trabajadas = input("Horas Trabajadas: ")
            descripcion_tareas = input("Descripcion de Tareas: ")

            # Crear el objeto Registro
            registro = Registro(empleado_id, proyecto_id, fecha, horas_trabajadas, descripcion_tareas)

            try:
                # Guardar el registro en la base de datos
                registro_model = RegistroModel()
                # AGREGAR IF TRUE
                registro_model.crear(registro)
                print("\nRegistro creado exitosamente")

            except Exception as e:
                print(f"\nError al crear el registro: {str(e)}")
            
            pausar()
            self.mostrar()
        # Modificar Registro de Tiempo
        elif seleccion == "3":
            limpiar_pantalla()
            print("--- Modificar Registro ---\n")

            id = input("Ingrese el ID del registro a modificar: ")

            # Buscar el registro en la base de datos
            registro_model = RegistroModel()
            registro = registro_model.existe(id)

            if registro:
                print("\nRegistro encontrado\n")

                # Mostrar los datos del registro
                new_empleado_id = registro[1]
                new_proyecto_id = input(f"ID Proyecto ({registro[2]}): ") or registro[2]
                new_fecha = input(f"Fecha ({registro[3]}): ") or registro[3]
                new_horas_trabajadas = input(f"Horas Trabajadas ({registro[4]}): ") or registro[4]
                new_descripcion_tareas = input(f"Descripcion de Tareas ({registro[5]}): ") or registro[5]

                # Crear el objeto Registro
                registro = Registro(new_empleado_id, new_proyecto_id, new_fecha, new_horas_trabajadas, new_descripcion_tareas)

                try:
                    # Actualizar el registro en la base de datos
                    # AGREGAR IF TRUE
                    registro_model.actualizar(registro, id)
                    print("\nRegistro actualizado exitosamente")
                    pausar()
                    self.mostrar()

                except Exception as e:
                    print(f"\nError al actualizar el registro: {str(e)}")

            else:
                print("\nRegistro no encontrado")
                pausar()
                self.mostrar()

        elif seleccion == "s":
            return


# Clase de Menú de Empleado
class MenuEmpleado:
    def __init__(self, usuario, rol):
        self.usuario = usuario
        self.rol = rol

    def mostrar(self):
        
        limpiar_pantalla()
        print("--- Menú de Empleado ---\n")

        print(f"Bienvenido {self.usuario}\n")

        opciones = [
            "1. Ver Proyectos",
            "2. Ver Departamentos",
            "3. Ver Empleados",
            "4. Registro del tiempo",
            "5. Informes",
            "S. Salir"
        ]

        for opcion in opciones:
            print(opcion)

        try:
            seleccion_menu_empleado = input("\nSeleccione una opción: ").strip().lower()

            if seleccion_menu_empleado == "1":
                self.proyecto_model = ProyectoModel()
                proyectos = self.proyecto_model.listar()
                
                limpiar_pantalla()
                # Limpia la pantalla
                print("---Proyectos---\n")
                # Mostrar Menu ---- Proyectos ---
                table = PrettyTable()
                # Invocar tabla
                table.field_names = ["ID", "Nombre", "Descripcion", "Fecha Inicio", "Fecha Fin"]
                # Agregar Filas
                for proyecto in proyectos:
                    table.add_row([proyecto[0], proyecto[1], proyecto[2], proyecto[3], proyecto[4]])
                # Iterar sobre los proyectos
                print(table)
                pausar()
                self.mostrar()
                # Funciones Finales

            elif seleccion_menu_empleado == "2":
                self.departamento_model = DepartamentoModel()
                departamentos = self.departamento_model.listar()

                limpiar_pantalla()
                print("---Departamentos---\n")

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

            elif seleccion_menu_empleado == "3":
                self.empleado_model = EmpleadoModel()
                empleados = self.empleado_model.listar()

                limpiar_pantalla()

                print("---Empleados---\n")

                table = PrettyTable()

                table.field_names = ["ID", "RUT", "Username", "Direccion", "Telefono", "Fecha Inicio Contrato", "Salario", "Departamento", "Rol"]
                for empleado in empleados:
                    table.add_row([empleado[0], empleado[1], empleado[2], empleado[4], empleado[5], empleado[6], empleado[7], empleado[10], empleado[9]])

                print(table)

                pausar()
                self.mostrar()

            elif seleccion_menu_empleado == "4":
                self.registro_model = RegistroModel()

                limpiar_pantalla()
                print("--- Registros de tiempo ---\n")

                opciones = [
                    "1. Ver Registros",
                    "2. Crear Registro",
                ]

                for opcion in opciones:
                    print(opcion)

                seleccion = input("\nSeleccione una opción: ").strip().lower()

                
                if seleccion == "1":
                    registros = self.registro_model.listar()

                    limpiar_pantalla()
                    print("--- Registros de tiempo ---\n")

                    table = PrettyTable()

                    table.field_names = ["ID", "Empleado ID", "Proyecto ID", "Fecha", "Horas Trabajadas", "Descripcion"]

                    for registro in registros:
                        table.add_row([registro[0], registro[1], registro[2], registro[3], registro[4], registro[5]])

                    print(table)

                    pausar()
                    self.mostrar()
                
                elif seleccion == "2":
                    limpiar_pantalla()
                    print("--- Crear Registro ---\n")

                    id_empleado = input("ID Empleado: ")
                    id_proyecto = input("ID Proyecto: ")
                    fecha = input("Fecha YYYY-MM-DD: ")
                    horas = input("Horas trabajadas: ")
                    descripcion = input("Descripcion de tareas: ")

                    registro = Registro(id_empleado, id_proyecto, fecha, horas, descripcion)

                    try:
                        self.registro_model.crear(registro)
                        print("\nRegistro creado exitosamente")
                    except Exception as e:
                        print(f"\nError al crear el registro: {str(e)}")

                    pausar()
                    self.mostrar()

                pausar()
                self.mostrar()

            elif seleccion_menu_empleado == "5":
                self.informe_model = InformeModel()
                informes = self.informe_model.listar()

                limpiar_pantalla()
                print("---Informes---\n")

                table = PrettyTable()

                table.field_names = ["ID", "Titulo", "Descripcion", "Fecha", "Empleado ID", "Proyecto ID"]

                for informe in informes:
                    table.add_row([informe[0], informe[1], informe[2], informe[3], informe[4], informe[5]])

                print(table)

                pausar()
                self.mostrar()
            
            elif seleccion_menu_empleado == "s":
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
   pass
