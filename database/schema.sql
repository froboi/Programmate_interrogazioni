-- Script SQL per creare il database MySQL per l'applicazione di gestione interrogazioni
-- Eseguire questo script per configurare il database

-- Creazione del database
CREATE DATABASE IF NOT EXISTS interrogazioni_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE interrogazioni_db;

-- Tabella degli studenti
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    registro_num INT NOT NULL UNIQUE,
    nome VARCHAR(100) NOT NULL,
    cognome VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_registro_num (registro_num),
    INDEX idx_nome_cognome (nome, cognome)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabella delle interrogazioni
CREATE TABLE IF NOT EXISTS interrogations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    materia VARCHAR(100) NOT NULL,
    student_id INT NOT NULL,
    lezione_num INT NOT NULL,
    data_lezione DATE NULL,
    ordine INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    INDEX idx_materia (materia),
    INDEX idx_lezione (lezione_num),
    INDEX idx_student (student_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabella delle configurazioni del calendario
CREATE TABLE IF NOT EXISTS calendar_configurations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    materia VARCHAR(100) NOT NULL,
    num_lezioni INT NOT NULL,
    distribuzione TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_materia (materia)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Inserimento dati di esempio (opzionale)
-- INSERT INTO students (registro_num, nome, cognome) VALUES
-- (1, 'Mario', 'Rossi'),
-- (2, 'Luca', 'Bianchi'),
-- (3, 'Anna', 'Verdi');

-- Verifica delle tabelle create
SHOW TABLES;

-- Descrizione delle tabelle
DESCRIBE students;
DESCRIBE interrogations;
DESCRIBE calendar_configurations;
