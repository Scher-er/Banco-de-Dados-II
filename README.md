# 🏥 Sistema de Monitoramento Hospitalar Híbrido (SQL + NoSQL)

> Um sistema completo de monitoramento remoto de pacientes utilizando uma arquitetura de banco de dados híbrida para aliar a integridade de dados cadastrais (MySQL) com a escalabilidade de dados de sensores IoT (MongoDB).

![Status](https://img.shields.io/badge/Status-Concluído-brightgreen)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![MySQL](https://img.shields.io/badge/DB-MySQL-orange)
![MongoDB](https://img.shields.io/badge/DB-MongoDB-green)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)

---

## 📖 Sobre o Projeto

Este projeto simula o ecossistema de dados de um hospital moderno. O desafio principal é lidar com dois tipos de dados com requisitos opostos:

1.  **Dados Estruturados (Relacional):** Cadastros de pacientes, médicos, convênios, endereços e regras de negócio. Para isso, usamos **MySQL**.
2.  **Dados de Alta Volumetria (Não Relacional):** Logs de monitoramento contínuo (batimentos cardíacos, oxigenação, pressão) gerados por equipamentos médicos IoT e logs de sistema. Para isso, usamos **MongoDB**.

O sistema inclui scripts de geração de massa de dados (ETL), simulação de dispositivos IoT em tempo real e um Dashboard interativo para a equipe médica.

---

## 🏗️ Arquitetura do Banco de Dados

### 1. Banco Relacional (MySQL)
Responsável pelo "Core Business" do hospital (ACID Compliance).
* **Tabelas Principais:** `Pacientes`, `Profissionais`, `Consultas`, `Alertas`, `Endereços` (Normalizado).
* **Lógica de Banco (Backend):**
    * **Trigger (`trg_auditoria_alerta_delete`):** Auditoria automática que salva alertas deletados em uma tabela de log (`log_alertas_excluidos`), garantindo rastreabilidade.
    * **Stored Procedure (`sp_fechar_alertas_antigos`):** Rotina para limpeza e manutenção automática, fechando alertas ativos há mais de X dias.

### 2. Banco Não Relacional (MongoDB)
Responsável pelo "Big Data", flexibilidade e velocidade de escrita.
* **Coleção `leituras_equipamentos`:** Recebe streams de dados JSON dos sensores. O Schema Validation garante a presença de campos vitais como `timestamp` e chaves estrangeiras do SQL.
* **Coleção `logs_alertas_disparados`:** Armazena o contexto detalhado (JSON complexo) de quando um alerta é gerado.
* **Coleção `logs_aplicacao`:** Auditoria técnica do sistema.

---

## 🚀 Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Banco SQL:** MySQL
* **Banco NoSQL:** MongoDB
* **Bibliotecas Python:**
    * `mysql-connector-python`: Conector nativo para MySQL.
    * `pymongo`: Driver oficial do MongoDB.
    * `faker`: Geração de dados realistas (nomes brasileiros, CPFs, endereços).
    * `streamlit`: Framework para criação da Interface de Usuário (Dashboard).
    * `pandas` & `plotly`: Manipulação e visualização de dados.

---

## 📦 Instalação e Configuração

### Pré-requisitos
* MySQL Server rodando na porta `3306`.
* MongoDB Server rodando na porta `27017`.
* Python instalado.
