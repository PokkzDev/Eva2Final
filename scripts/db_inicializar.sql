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
    salario DECIMAL(10, 2) NOT NULL CHECK (salario > 0),
    departamento_id INT,
    rol ENUM('admin', 'usuario', 'gerente') NOT NULL
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
    fecha_fin DATE NOT NULL,
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
-- Reload privileges to ensure the new user and permissions are applied
FLUSH PRIVILEGES;

-- Commit transaction (optional in phpMyAdmin, depends on its configuration)
COMMIT;
