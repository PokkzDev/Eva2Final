-- Start transaction block (optional in phpMyAdmin, phpMyAdmin typically handles transactions automatically)
START TRANSACTION;

-- Drop database and user if they already exist
DROP DATABASE IF EXISTS lc_pa_ba_eva2_2024;
DROP USER IF EXISTS 'lc_pa_ba_eva2_2024'@'localhost';

-- Create new database and user
CREATE DATABASE lc_pa_ba_eva2_2024;
CREATE USER 'lc_pa_ba_eva2_2024'@'localhost' IDENTIFIED BY 'lc_pa_ba_eva2_2024';

-- Grant permissions to the new user
GRANT SELECT, INSERT, UPDATE, DELETE ON lc_pa_ba_eva2_2024.* TO 'lc_pa_ba_eva2_2024'@'localhost';

-- Use the newly created database
USE lc_pa_ba_eva2_2024;

-- Create empleados table
CREATE TABLE empleados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rut VARCHAR(15) NOT NULL UNIQUE,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL,
    direccion VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    fecha_inicio_contrato DATE NOT NULL,
    salario FLOAT NOT NULL CHECK (salario > 0),
    departamento_id INT,
    rol ENUM('admin', 'gerente', 'usuario') NOT NULL
);

-- Create departamento table
CREATE TABLE departamento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion VARCHAR(100) NOT NULL,
    id_gerente INT,
    INDEX (id_gerente),
    FOREIGN KEY (id_gerente) REFERENCES empleados(id) ON DELETE SET NULL
);

-- Create proyectos table
CREATE TABLE proyectos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion VARCHAR(100) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL
);

-- Create empleados_departamento junction table
CREATE TABLE empleados_departamento (
    empleado_id INT NOT NULL,
    departamento_id INT NOT NULL,
    PRIMARY KEY (empleado_id, departamento_id),
    FOREIGN KEY (empleado_id) REFERENCES empleados(id) ON DELETE CASCADE,
    FOREIGN KEY (departamento_id) REFERENCES departamento(id) ON DELETE CASCADE
);

-- Create empleado_proyecto junction table
CREATE TABLE empleado_proyecto (
    empleado_id INT NOT NULL,
    proyecto_id INT NOT NULL,
    PRIMARY KEY (empleado_id, proyecto_id),
    FOREIGN KEY (empleado_id) REFERENCES empleados(id) ON DELETE CASCADE,
    FOREIGN KEY (proyecto_id) REFERENCES proyectos(id) ON DELETE CASCADE,
    INDEX (empleado_id),
    INDEX (proyecto_id)
);

-- Add foreign key constraint to empleados table for departamento_id
ALTER TABLE empleados
ADD CONSTRAINT fk_departamento
FOREIGN KEY (departamento_id) REFERENCES departamento(id) ON DELETE SET NULL;

-- Create informe table
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

-- Create registro_de_tiempo table
CREATE TABLE registro_de_tiempo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empleado_id INT NOT NULL,
    proyecto_id INT NOT NULL,
    fecha DATE NOT NULL,
    horas_trabajadas DOUBLE NOT NULL CHECK (horas_trabajadas > 0),
    descripcion_tareas TEXT,
    FOREIGN KEY (empleado_id) REFERENCES empleados(id) ON DELETE CASCADE,
    FOREIGN KEY (proyecto_id) REFERENCES proyectos(id) ON DELETE CASCADE,
    INDEX (empleado_id),
    INDEX (proyecto_id)
);

-- Insert multiple employees
INSERT INTO empleados (rut, username, password, direccion, telefono, fecha_inicio_contrato, salario, departamento_id, rol)
VALUES 
    ('12345678-9', 'admin', '$2b$10$Zyk/rZJobzzf/iOKoyMgu.5SjVpmVsAtK0cMNHm0NISCjxk3BCu3K', 'Calle Falsa 123', '123456789', '2021-01-01', 1000000, NULL, 'admin'),
    ('12345678-12', 'd.mendez', '$2b$12$WC3gQOL3y.O2IoOPAptkjO9THiTnzDCbstntMy7xQG.p8zNsvRK7O', 'Calle Falsa 123', '123456789', '2021-01-01', 1000000, NULL, 'admin'),
    ('87654321-9', 'usuario', '$2b$10$Zyk/rZJobzzf/iOKoyMgu.5SjVpmVsAtK0cMNHm0NISCjxk3BCu3K', 'Calle Falsa 321', '987654321', '2021-01-01', 500000, NULL, 'usuario'),
    ('123123123', 'b.altamirano', '$2b$10$sIkhFShlAKlg.jDD.fVnT.ghVgG3p1trd7ReJZGphyJxMbG4ATrhK', 'Calle Falsa 123', '123456789', '2021-01-01', 1000000, NULL, 'admin'),
    ('k-k', 'gerente', '$2b$10$D0jX/hLNTrkIKuwnEKbYauJfqtrNsb42Ucysp3dHTBF5a.Y94BwEC', 'Calle Falsa 123', '987654321', '2023-01-01', 700000, NULL, 'gerente');

-- Insert multiple departments
INSERT INTO departamento (nombre, descripcion, id_gerente)
VALUES 
    ('Desarrollo', 'Departamento de desarrollo de software', 5),
    ('Ventas', 'Departamento de ventas', NULL),
    ('Marketing', 'Departamento de marketing', NULL);

-- Insert multiple projects
INSERT INTO proyectos (nombre, descripcion, fecha_inicio, fecha_fin)
VALUES 
    ('Proyecto 1', 'Descripción del proyecto 1', '2021-01-01', '2021-12-31'),
    ('Proyecto 2', 'Descripción del proyecto 2', '2021-01-01', '2021-12-31'),
    ('Proyecto 3', 'Descripción del proyecto 3', '2021-01-01', '2021-12-31');

-- Insert multiple employees into departments
INSERT INTO empleados_departamento (empleado_id, departamento_id)
VALUES 
    (1, 1),
    (2, 1),
    (3, 2),
    (4, 3),
    (5, 1);

-- Insert multiple employees into projects
INSERT INTO empleado_proyecto (empleado_id, proyecto_id)
VALUES 
    (1, 1),
    (2, 1),
    (3, 2),
    (4, 3),
    (5, 1);

-- Insert multiple reports
INSERT INTO informe (titulo, descripcion, fecha, empleado_id, proyecto_id)
VALUES 
    ('Informe 1', 'Descripción del informe 1', '2021-01-01', 1, 1),
    ('Informe 2', 'Descripción del informe 2', '2021-01-01', 2, 1),
    ('Informe 3', 'Descripción del informe 3', '2021-01-01', 3, 2),
    ('Informe 4', 'Descripción del informe 4', '2021-01-01', 4, 3),
    ('Informe 5', 'Descripción del informe 5', '2021-01-01', 5, 1);

-- Insert multiple time records
INSERT INTO registro_de_tiempo (empleado_id, proyecto_id, fecha, horas_trabajadas, descripcion_tareas)
VALUES 
    (1, 1, '2021-01-01', 8, 'Descripción de tareas 1'),
    (2, 1, '2021-01-01', 8, 'Descripción de tareas 2'),
    (3, 2, '2021-01-01', 8, 'Descripción de tareas 3'),
    (4, 3, '2021-01-01', 8, 'Descripción de tareas 4'),
    (5, 1, '2021-01-01', 8, 'Descripción de tareas 5');

-- Reload privileges to ensure the new user and permissions are applied
FLUSH PRIVILEGES;

-- Commit transaction (optional in phpMyAdmin, depends on its configuration)
COMMIT;
