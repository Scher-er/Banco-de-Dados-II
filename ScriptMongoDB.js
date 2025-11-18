// --- 1. Limpeza: Remove as coleções antigas se elas existirem ---
// Isso evita o erro "NamespaceExists"
db.leituras_equipamentos.drop();
db.logs_alertas_disparados.drop();
db.logs_aplicacao.drop();

// --- 2. Criar a coleção 'leituras_equipamentos' ---
db.createCollection("leituras_equipamentos", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      title: "Validação de Leituras de Equipamentos",
      required: ["id_paciente_sql", "id_dispositivo", "timestamp", "dados"],
      properties: {
        id_paciente_sql: {
          bsonType: "int",
          description: "Chave estrangeira obrigatória para 'pacientes.idPacientes' no SQL"
        },
        id_dispositivo: {
          bsonType: "string",
          description: "ID/Serial do equipamento que enviou o dado"
        },
        timestamp: {
          bsonType: "date",
          description: "Data e hora exata da medição"
        },
        tipo_leitura: {
          bsonType: "string",
          description: "Tipo de leitura (ex: SINAIS_VITAIS, GLICEMIA)"
        },
        dados: {
          bsonType: "object",
          description: "Objeto flexível com os pares de 'medida: valor'"
        }
      }
    }
  }
});

// --- 3. Criar a coleção 'logs_alertas_disparados' ---
db.createCollection("logs_alertas_disparados", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      title: "Validação de Logs de Alertas",
      required: ["id_alerta_sql", "id_paciente_sql", "timestamp", "mensagem", "nivel_critico"],
      properties: {
        id_alerta_sql: {
          bsonType: "int",
          description: "Chave estrangeira obrigatória para 'alertas.idAlertas' no SQL"
        },
        id_paciente_sql: {
          bsonType: "int",
          description: "Chave estrangeira para 'pacientes.idPacientes' no SQL"
        },
        timestamp: {
          bsonType: "date",
          description: "Data e hora que o alerta foi disparado"
        },
        nivel_critico: {
          bsonType: "string",
          description: "Nível do alerta (ex: ALTO, MEDIO, BAIXO)"
        },
        mensagem: {
          bsonType: "string",
          description: "Descrição do alerta"
        },
        dados_trigger: {
          bsonType: "object",
          description: "Valores exatos que causaram o disparo do alerta"
        },
        status_notificacao: {
          bsonType: "string",
          description: "Status do envio (ex: ENVIADO_MEDICO, PENDENTE)"
        }
      }
    }
  }
});

// --- 4. Criar a coleção 'logs_aplicacao' ---
db.createCollection("logs_aplicacao", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      title: "Validação de Logs da Aplicação",
      required: ["timestamp", "nivel_log", "mensagem"],
      properties: {
        timestamp: {
          bsonType: "date",
          description: "Data e hora do evento de log"
        },
        nivel_log: {
          bsonType: "string",
          description: "Nível (ex: INFO, WARN, ERROR, DEBUG)"
        },
        servico: {
          bsonType: "string",
          description: "Módulo/Serviço da aplicação que gerou o log"
        },
        mensagem: {
          bsonType: "string",
          description: "Mensagem de log"
        },
        detalhes: {
          bsonType: "object",
          description: "Contexto adicional, stack trace, etc."
        }
      }
    }
  }
});

// --- 5. Criar Índices Essenciais para Performance ---
db.leituras_equipamentos.createIndex({ id_paciente_sql: 1, timestamp: -1 });
db.logs_alertas_disparados.createIndex({ id_paciente_sql: 1, timestamp: -1 });
db.logs_aplicacao.createIndex({ timestamp: -1 });

print("Banco de dados limpo e recriado com sucesso!");