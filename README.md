# Banco-de-Dados-II
📊 Projeto de demonstração de uma arquitetura de dados híbrida, usando um banco de dados relacional e um NoSQL em uma mesma aplicação para otimizar consistência e escalabilidade.

# Projeto de BD: Monitoramento Remoto de Pacientes (Híbrido)

> Este repositório contém a arquitetura e o schema de um sistema de banco de dados híbrido (SQL + NoSQL) projetado para o monitoramento remoto de pacientes hospitalares.

O objetivo deste projeto é criar uma infraestrutura de banco de dados robusta, escalável e eficiente, capaz de gerenciar tanto os dados cadastrais e relacionais dos pacientes quanto o grande volume de dados não estruturados gerados por dispositivos de monitoramento (IoT).

---

## 🚀 A Arquitetura Híbrida

Para otimizar o desempenho, a integridade e a flexibilidade, o sistema utiliza dois tipos de bancos de dados:

### 1. Banco de Dados Relacional (MySQL)

Utilizado para armazenar dados **estruturados**, **transacionais** e que exigem alta **integridade referencial** (ACID). É o "coração" cadastral do sistema.

* **O que armazena:**
    * Dados cadastrais de `Pacientes`.
    * Dados cadastrais de `Profissionais` (médicos, enfermeiros).
    * Relacionamentos (ex: qual profissional atende qual paciente).
    * Endereços normalizados (País, Estado, Cidade, Bairro).
    * Metadados de `Alertas` e `Medições` (ex: limites críticos, tipo de medição).
    * `Historico_Medico` estruturado e `Convenios`.
* **Tecnologia:** MySQL / MariaDB
* **Schema:** O script SQL para criação do banco (`acompanhamento_pacientes_bd.sql`) está [incluído neste repositório](caminho/para/seu/arquivo.sql).

### 2. Banco de Dados Não Relacional (MongoDB)

Utilizado para armazenar dados **não estruturados**, **semiestruturados** ou de **grande volume** (Big Data), que não exigem um schema rígido e se beneficiam de escalabilidade horizontal.

* **O que armazena:**
    * **Logs de Equipamentos:** *Streams* de dados brutos gerados pelos dispositivos de monitoramento (ex: monitores cardíacos, oxímetros) em formato JSON.
    * **Logs da Aplicação:** Logs de auditoria, erros e eventos do sistema.
    * **Arquivos e Documentos:** (Opcional) Usando o GridFS do MongoDB, é possível armazenar arquivos binários como exames (PDFs, imagens médicas) associados aos pacientes.
* **Tecnologia:** MongoDB

---

## 🗂️ Estrutura do Banco de Dados

### Banco Relacional (SQL)

O schema SQL (baseado no arquivo dump) é centrado na entidade `Pacientes` e suas relações:

* **Entidades Principais:**
    * `Pacientes`: Dados cadastrais, contato de emergência e status.
    * `Profissionais`: Dados da equipe médica.
* **Relação N:M:**
    * `Pacientes_has_Profissionais`: Vincula pacientes aos profissionais responsáveis.
* **Dados de Monitoramento (Estruturados):**
    * `Medicao`: Registros de medições vitais (ex: tipo="pressão", valor="120/80").
    * `Alertas`: Gatilhos gerados quando uma medição excede os limites.
    * `Limites_Alerta`: Limites (mín/máx) personalizados para cada paciente.
* **Dados Complementares:**
    * `Historico_Medico`: Eventos de saúde do paciente.
    * `Convenios`: Informações do plano de saúde.
* **Endereçamento (Normalizado):**
    * `Paises` -> `Estados` -> `Cidades` -> `Bairros`

### Banco Não Relacional (NoSQL)

A estrutura no MongoDB é flexível e baseada em coleções. Um exemplo de documento para um log de equipamento poderia ser:

**Coleção: `leituras_equipamentos`**
```json
{
  "id_paciente_sql": 1, // Chave para relacionar com o paciente no SQL
  "id_dispositivo": "MONITOR_CARDIACO_A45B",
  "timestamp": "2025-11-15T11:45:02.123Z",
  "tipo_leitura": "ECG",
  "dados": {
    "bpm": 82,
    "saturacao_o2": 98,
    "pressao_sistolica": 122,
    "pressao_diastolica": 79,
    "status_bateria_dispositivo": "75%"
  }
}
