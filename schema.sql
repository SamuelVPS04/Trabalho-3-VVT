-- Schema de criação do banco de dados e tabela para o Trabalho 2
-- Banco: db_produtos

DROP DATABASE IF EXISTS db_produtos;
CREATE DATABASE db_produtos CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE db_produtos;

DROP TABLE IF EXISTS produtos;
CREATE TABLE produtos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  codigo VARCHAR(8) NOT NULL UNIQUE,
  sec INT NOT NULL,
  Grupo CHAR(1) NOT NULL,
  Tipo_Alimento CHAR(1) NOT NULL,
  Pais CHAR(2) NOT NULL
);

-- Dados de exemplo fornecidos na descrição do problema
INSERT INTO produtos (codigo, sec, Grupo, Tipo_Alimento, Pais) VALUES
  ('BRC0001A', 1, 'C', 'A', 'BR'),
  ('BRD0001I', 1, 'D', 'I', 'BR'),
  ('BRA0001K', 1, 'A', 'K', 'BR'),
  ('BRF0001F', 1, 'F', 'F', 'BR'),
  ('BRG0001A', 1, 'G', 'A', 'BR'),
  ('BRC0002A', 2, 'C', 'A', 'BR'),
  ('BRD0002K', 2, 'D', 'K', 'BR'),
  ('BRF0002A', 2, 'F', 'A', 'BR'),
  ('BRC0003C', 3, 'C', 'C', 'BR');
