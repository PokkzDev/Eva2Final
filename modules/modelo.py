"""
Archivo que contiene la definición de los modelos de la aplicación.
"""

from modules.db_conn import DB_Conn
import bcrypt

# Clase Empleado
class Empleado:
    def __init__(self, rut: str, username: str, password: str, direccion: str, telefono: int, fecha_inicio_contrato: str, salario: float, departamento_id: 'Departamento', rol: str):
        self.rut = rut
        self.username = username
        self.password = password
        self.direccion = direccion
        self.telefono = telefono
        self.fecha_inicio_contrato = fecha_inicio_contrato
        self.salario = salario
        self.departamento_id = departamento_id

        if self.departamento_id == "" or self.departamento_id == "0":
            self.departamento_id = None

        self.rol = rol

# Clase EmpleadoModel que maneja la lógica de la base de datos
class EmpleadoModel:
    def listar(self):
        db = DB_Conn()
        conexion = db.iniciar_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT e.*, ed.departamento_id, d.nombre FROM empleados e LEFT JOIN empleados_departamento ed ON e.id = ed.empleado_id LEFT JOIN departamento d ON ed.departamento_id = d.id")
        empleados = cursor.fetchall()

        cursor.close()
        db.cerrar_conexion()
        # Formatear las fechas de 'YYYY-MM-DD' a 'DD-MM-YYYY'
        empleados_formateados = []
        for empleado in empleados:
            (id, rut, username, password, direccion, telefono, fecha_inicio_contrato, salario, departamento_id, rol, departamento_id, nombre_departamento) = empleado

            # Formatear la fecha si no es None
            if fecha_inicio_contrato:
                fecha_inicio_contrato = fecha_inicio_contrato.strftime('%d-%m-%Y')

            # Crear una nueva tupla con las fechas formateadas
            empleado_formateado = (id, rut, username, password, direccion, telefono, fecha_inicio_contrato, salario, departamento_id, rol, departamento_id, nombre_departamento)
            empleados_formateados.append(empleado_formateado)

        return empleados_formateados

    def crear(self, empleado: Empleado):
        db = DB_Conn()
        conexion = db.iniciar_conexion()
        cursor = conexion.cursor()

        # Use 10 rounds for bcrypt salt
        hashed_password = bcrypt.hashpw(empleado.password.encode('utf-8'), bcrypt.gensalt(rounds=10)).decode('utf-8')

        cursor.execute(
            "INSERT INTO empleados (rut, username, password, direccion, telefono, fecha_inicio_contrato, salario, departamento_id, rol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
            (empleado.rut, empleado.username, 
             hashed_password, 
             empleado.direccion, empleado.telefono, 
             empleado.fecha_inicio_contrato, empleado.salario, 
             empleado.departamento_id, empleado.rol)
        )

        conexion.commit()
        cursor.close()
        db.cerrar_conexion()

    def actualizar(self, empleado: Empleado, old_rut: str):
        db = DB_Conn()
        conexion = db.iniciar_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "UPDATE empleados SET rut = %s, username = %s, password = %s, direccion = %s, telefono = %s, fecha_inicio_contrato = %s, salario = %s, departamento_id = %s, rol = %s WHERE rut = %s", 
            (empleado.rut, empleado.username, 
             empleado.password, 
             empleado.direccion, empleado.telefono, 
             empleado.fecha_inicio_contrato, empleado.salario, 
             empleado.departamento_id, empleado.rol, old_rut)
        )

        conexion.commit()
        cursor.close()
        db.cerrar_conexion()

    def existe(self, rut: str):
        db = DB_Conn()
        conexion = db.iniciar_conexion()
         
        try: 
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM empleados WHERE rut = %s", (rut,))
            empleado = cursor.fetchone()
            cursor.close()
            db.cerrar_conexion()
            if empleado:
                # Asumiendo que la columna 'fecha_inicio_contrato' está en la posición 6 (índice 5 en la tupla)
                (id, rut, username, password, direccion, telefono, fecha_inicio_contrato, salario, departamento_id, rol) = empleado

                # Formatear la fecha si no es None
                if fecha_inicio_contrato:
                    fecha_inicio_contrato = fecha_inicio_contrato.strftime('%d-%m-%Y')

                # Crear una nueva tupla con la fecha formateada
                empleado_formateado = (id, rut, username, password, direccion, telefono, fecha_inicio_contrato, salario, departamento_id, rol)

            return empleado_formateado
        except Exception as e:
            print(f"Error al buscar el empleado: {str(e)}")
            return False
    def eliminar(self, rut: str):
        db = DB_Conn()
        conexion = db.iniciar_conexion()
        cursor = conexion.cursor()

        cursor.execute("DELETE FROM empleados WHERE rut = %s", (rut,))

        conexion.commit()
        cursor.close()
        db.cerrar_conexion()

# Clase Departamento que representa un departamento de la empresa
class Departamento:
    """
        CREATE TABLE departamento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion VARCHAR(100) NOT NULL,
    id_gerente INT,
    INDEX (id_gerente),
    FOREIGN KEY (id_gerente) REFERENCES empleados(id) ON DELETE SET NULL
);
    """

    def __init__(self, nombre: str, descripcion: str, id_gerente: Empleado)-> None:
        self.nombre = nombre
        self.descripcion = descripcion
        self.id_gerente = id_gerente

        if self.id_gerente == "" or self.id_gerente == "0":
            self.id_gerente = None

# Clase DepartamentoModel que maneja la lógica de la base de datos
class DepartamentoModel:
    def listar(self)-> list:
        db = DB_Conn()
        conexion = db.iniciar_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT d.*, e.username, e.rol FROM departamento d LEFT JOIN empleados e ON d.id_gerente=e.id")
        departamentos = cursor.fetchall()

        cursor.close()
        if departamentos == []:
            print("No existe un departamento por el momento")
        db.cerrar_conexion()

        return departamentos

    def crear(self, departamento: Departamento):
        db = DB_Conn()
        conexion = db.iniciar_conexion()
        cursor = conexion.cursor()

        try:
            # Buscar si el gerente existe en caso de que se haya ingresado
            if departamento.id_gerente:
                cursor.execute("SELECT * FROM empleados WHERE id = %s", (departamento.id_gerente,))
                gerente = cursor.fetchone()

                if not gerente:
                    raise Exception("El gerente no existe")
        except Exception as e:
            print(f"Error al buscar el gerente: {str(e)}")
            return False
        
        try:
            cursor.execute(
                "INSERT INTO departamento (nombre, descripcion, id_gerente) VALUES (%s, %s, %s)", 
                (departamento.nombre, departamento.descripcion, departamento.id_gerente)
            )

            conexion.commit()
            cursor.close()
        except Exception as e:
            print(f"Error al crear el departamento: {str(e)}")
            conexion.rollback()
            return
        finally:
            cursor.close()
            db.cerrar_conexion()


    def actualizar(self, departamento: Departamento, id: int):
        db = DB_Conn()
        conexion = db.iniciar_conexion()
        cursor = conexion.cursor()

        try:
            # Actualizar Datos en BD
            cursor.execute(
                "UPDATE departamento SET nombre = %s, descripcion = %s, id_gerente = %s WHERE id = %s",
                (departamento.nombre, departamento.descripcion, departamento.id_gerente, id)
            )

            conexion.commit()
            cursor.close()
        except Exception as e:
            print(f"Error al actualizar el departamento: {str(e)}")
            conexion.rollback()
            return
        finally:
            cursor.close()
            db.cerrar_conexion()

    def listar_empleados(self, id_departamento: int):
        db = DB_Conn()
        conexion = db.iniciar_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT e.* FROM empleados e JOIN empleados_departamento ed ON e.id = ed.empleado_id WHERE ed.departamento_id = %s",
            (id_departamento,)
        )

        empleados = cursor.fetchall()

        cursor.close()
        db.cerrar_conexion()

        return empleados

    def asignar_empleado(self, id_empleado: int, id_departamento: int):
        """
            CREATE TABLE empleados_departamento (
            empleado_id INT NOT NULL,
            departamento_id INT NOT NULL,
            PRIMARY KEY (empleado_id, departamento_id),
            FOREIGN KEY (empleado_id) REFERENCES empleados(id) ON DELETE CASCADE,
            FOREIGN KEY (departamento_id) REFERENCES departamento(id) ON DELETE CASCADE,
        );
        """
        
        db = DB_Conn()
        conexion = db.iniciar_conexion()
        cursor = conexion.cursor()

        # Verificar si el empleado ya está asignado un departamento
        cursor.execute(
            "SELECT * FROM empleados_departamento WHERE empleado_id = %s",
            (id_empleado,)
        )

        empleado_departamento = cursor.fetchone()

        if empleado_departamento:
            return False
        else:
            try:
                cursor.execute(
                    "INSERT INTO empleados_departamento (empleado_id, departamento_id) VALUES (%s, %s)",
                    (id_empleado, id_departamento)
                )

                conexion.commit()
                cursor.close()

                return True
            except Exception as e:
                print(f"Error al asignar empleado a departamento: {str(e)}")
                conexion.rollback()
                return
            finally:
                cursor.close()
                db.cerrar_conexion()

    def modificar_empleado(self, id_empleado: int, id_departamento: int):
        db = DB_Conn()
        conexion = db.iniciar_conexion()
        cursor = conexion.cursor()

        try:
            # modificar empleado de departamento
            cursor.execute(
                "UPDATE empleados_departamento SET departamento_id = %s WHERE empleado_id = %s",
                (id_departamento, id_empleado)
            )

            conexion.commit()
            cursor.close()
        except Exception as e:
            print(f"Error al modificar empleado de departamento: {str(e)}")
            conexion.rollback()
            return
        finally:
            cursor.close()
            db.cerrar_conexion()
        
    def eliminar_empleado(self, id_empleado: int):
        db = DB_Conn()
        conexion = db.iniciar_conexion()
        cursor = conexion.cursor()

        try:
            # Eliminar empleado de departamento
            cursor.execute(
                "DELETE FROM empleados_departamento WHERE empleado_id = %s",
                (id_empleado,)
            )

            conexion.commit()
            cursor.close()
        except Exception as e:
            print(f"Error al eliminar empleado de departamento: {str(e)}")
            conexion.rollback()
            return
        finally:
            cursor.close()
            db.cerrar_conexion()

    def existe(self, id: int):
        db = DB_Conn()
        conexion = db.iniciar_conexion()
         
        try: 
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM departamento WHERE id = %s", (id,))
            departamento = cursor.fetchone()
            cursor.close()
            db.cerrar_conexion()
            return departamento
        except Exception as e:
            print(f"Error al buscar el departamento: {str(e)}")
            return False

    def eliminar(self, id: int):
        db = DB_Conn()
        conexion = db.iniciar_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute("DELETE FROM departamento WHERE id = %s", (id,))
            conexion.commit()
        except Exception as e:
            print(f"Error al eliminar el departamento: {str(e)}")
            conexion.rollback()
            return
        finally:
            cursor.close()
            db.cerrar_conexion()

# Clase Proyecto que representa un proyecto de la empresa
class Proyecto:
    def __init__(self, nombre, descripcion, fecha_inicio, fecha_fin):
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin

# Clase ProyectoModel que maneja la lógica de la base de datos
class ProyectoModel:
    def listar(self):
        db = DB_Conn()
        conexion = db.iniciar_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM proyectos")
        proyectos = cursor.fetchall()

        cursor.close()
        db.cerrar_conexion()

        proyectos_formateados = []
        for proyecto in proyectos:
            (id, nombre, descripcion, fecha_inicio, fecha_fin) = proyecto

            if fecha_inicio or fecha_fin:
                fecha_inicio = fecha_inicio.strftime('%d-%m-%Y')
                fecha_fin = fecha_fin.strftime('%d-%m-%Y')

            proyecto_formateado = (id, nombre, descripcion, fecha_inicio, fecha_fin)
            proyectos_formateados.append(proyecto_formateado)

        return proyectos_formateados

    def crear(self, proyecto: Proyecto):
        db = DB_Conn()
        conexion = db.iniciar_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute(
                "INSERT INTO proyectos (nombre, descripcion, fecha_inicio, fecha_fin) VALUES (%s, %s, %s, %s)", 
                (proyecto.nombre, proyecto.descripcion, proyecto.fecha_inicio, proyecto.fecha_fin)
            )

            conexion.commit()
        except Exception as e:
            print(f"Error al crear el proyecto: {str(e)}")
            conexion.rollback()
            return
        finally:
            cursor.close()
            db.cerrar_conexion()

    def actualizar(self, proyecto: Proyecto, id: int):
        db = DB_Conn()
        conexion = db.iniciar_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute(
                "UPDATE proyectos SET nombre = %s, descripcion = %s, fecha_inicio = %s, fecha_fin = %s WHERE id = %s", 
                (proyecto.nombre, proyecto.descripcion, proyecto.fecha_inicio, proyecto.fecha_fin, id)
            )

            conexion.commit()
        except Exception as e:
            print(f"Error al actualizar el proyecto: {str(e)}")
            conexion.rollback()
            return
        finally:
            cursor.close()
            db.cerrar_conexion()

    def existe(self, id: int):
        db = DB_Conn()
        conexion = db.iniciar_conexion()
         
        try: 
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM proyectos WHERE id = %s", (id,))
            proyecto = cursor.fetchone()
            cursor.close()
            db.cerrar_conexion()
            if proyecto:
                (id, nombre, descripcion, fecha_inicio, fecha_fin) = proyecto

                if fecha_inicio or fecha_fin:
                    fecha_inicio = fecha_inicio.strftime('%d-%m-%Y')
                    fecha_fin = fecha_fin.strftime('%d-%m-%Y')
                
                proyecto_formateado = (id, nombre, descripcion, fecha_inicio, fecha_fin)
                
            return proyecto_formateado
        except Exception as e:
            print(f"Error al buscar el proyecto: {str(e)}")
            return False

    def eliminar(self, id: int):
        db = DB_Conn()
        conexion = db.iniciar_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute("DELETE FROM proyectos WHERE id = %s", (id,))
            conexion.commit()
        except Exception as e:
            print(f"Error al eliminar el proyecto: {str(e)}")
            conexion.rollback()
            return
        finally:
            cursor.close()
            db.cerrar_conexion()

# Clase RegistroDeTiempo que representa un registro de tiempo de un empleado en un proyecto
class Registro:
    def __init__(self, empleado_id: int, proyecto_id: int, fecha: str, horas_trabajadas: float, descripcion_tareas: str):
        self.empleado_id = empleado_id
        self.proyecto_id = proyecto_id
        self.fecha = fecha
        self.horas_trabajadas = horas_trabajadas
        self.descripcion_tareas = descripcion_tareas

# Clase RegistroModel que maneja la lógica de la base de datos
class RegistroModel:
    def listar(self):
        db = DB_Conn()
        conexion = db.iniciar_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
                    SELECT r.id, e.username, p.nombre AS Nombre_Proyecto, r.fecha AS FECHA_REGISTRO, r.horas_trabajadas AS Horas_Trabajadas, r.descripcion_tareas AS Tarea_Descrita
                    FROM registro_de_tiempo r
                    JOIN empleados e ON r.empleado_id = e.id
                    JOIN proyectos p ON r.proyecto_id = p.id;
        """)

        registros = cursor.fetchall()

        return registros
    
    def crear(self, registro: Registro):
        db = DB_Conn()
        conexion = db.iniciar_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute(
                "INSERT INTO registro_de_tiempo (empleado_id, proyecto_id, fecha, horas_trabajadas, descripcion_tareas) VALUES (%s, %s, %s, %s, %s)", 
                (registro.empleado_id, registro.proyecto_id, registro.fecha, registro.horas_trabajadas, registro.descripcion_tareas)
            )

            conexion.commit()
        except Exception as e:
            print(f"Error al crear el registro: {str(e)}")
            conexion.rollback()
            return
        finally:
            cursor.close()
            db.cerrar_conexion()

    def actualizar(self, registro: Registro, id: int):
        db = DB_Conn()
        conexion = db.iniciar_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute(
                "UPDATE registro_de_tiempo SET empleado_id = %s, proyecto_id = %s, fecha = %s, horas_trabajadas = %s, descripcion_tareas = %s WHERE id = %s", 
                (registro.empleado_id, registro.proyecto_id, registro.fecha, registro.horas_trabajadas, registro.descripcion_tareas, id)
            )

            conexion.commit()
        except Exception as e:
            print(f"Error al actualizar el registro: {str(e)}")
            conexion.rollback()
            return
        finally:
            cursor.close()
            db.cerrar_conexion()
    
    def existe(self, id: int):
        db = DB_Conn()
        conexion = db.iniciar_conexion()
         
        try: 
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM registro_de_tiempo WHERE id = %s", (id,))
            registro = cursor.fetchone()
            cursor.close()
            db.cerrar_conexion()
            
            return registro
        except Exception as e:
            print(f"Error al buscar el registro: {str(e)}")
            return False

    def eliminar(self, id: int):
        db = DB_Conn()
        conexion = db.iniciar_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute("DELETE FROM registro_de_tiempo WHERE id = %s", (id,))
            conexion.commit()
        except Exception as e:
            print(f"Error al eliminar el registro: {str(e)}")
            conexion.rollback()
            return
        finally:
            cursor.close()
            db.cerrar_conexion()

# Clase Informe que representa un informe de tiempo de un empleado en un proyecto
class Informe: 
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
    def __init__(self, titulo: str, descripcion: str, fecha: str, empleado_id: int, proyecto_id: int):
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha = fecha
        self.empleado_id = empleado_id
        self.proyecto_id = proyecto_id

# Clase InformeModel que maneja la lógica de la base de datos
class InformeModel:
    def listar(self):
        db = DB_Conn()
        conexion = db.iniciar_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
                    SELECT i.id, e.username, p.nombre AS Nombre_Proyecto, i.fecha AS FECHA_INFORME, i.titulo AS Titulo, i.descripcion AS Descripcion
                    FROM informe i
                    JOIN empleados e ON i.empleado_id = e.id
                    JOIN proyectos p ON i.proyecto_id = p.id;
        """)

        informes = cursor.fetchall()

        return informes
    
    def crear(self, informe: Informe):
        db = DB_Conn()
        conexion = db.iniciar_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute(
                "INSERT INTO informe (titulo, descripcion, fecha, empleado_id, proyecto_id) VALUES (%s, %s, %s, %s, %s)", 
                (informe.titulo, informe.descripcion, informe.fecha, informe.empleado_id, informe.proyecto_id)
            )

            conexion.commit()
        except Exception as e:
            print(f"Error al crear el informe: {str(e)}")
            conexion.rollback()
            return
        finally:
            cursor.close()
            db.cerrar_conexion()

    def actualizar(self, informe: Informe, id: int):
        db = DB_Conn()
        conexion = db.iniciar_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute(
                "UPDATE informe SET titulo = %s, descripcion = %s, fecha = %s, empleado_id = %s, proyecto_id = %s WHERE id = %s", 
                (informe.titulo, informe.descripcion, informe.fecha, informe.empleado_id, informe.proyecto_id, id)
            )

            conexion.commit()
        except Exception as e:
            print(f"Error al actualizar el informe: {str(e)}")
            conexion.rollback()
            return
        finally:
            cursor.close()
            db.cerrar_conexion()
    
    def existe(self, id: int):
        db = DB_Conn()
        conexion = db.iniciar_conexion()
         
        try: 
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM informe WHERE id = %s", (id,))
            informe = cursor.fetchone()
            cursor.close()
            db.cerrar_conexion()
            
            return informe
        except Exception as e:
            print(f"Error al buscar el informe: {str(e)}")
            return False

    def eliminar(self, id: int):
        db = DB_Conn()
        conexion = db.iniciar_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute("DELETE FROM informe WHERE id = %s", (id,))
            conexion.commit()
        except Exception as e:
            print(f"Error al eliminar el informe: {str(e)}")
            conexion.rollback()
            return
        finally:
            cursor.close()
            db.cerrar_conexion()

    