import mysql.connector
from pymongo import MongoClient
import random
from datetime import datetime, timedelta
import time

# --- CONFIGURAÇÃO DO SQL (MySQL) ---
SQL_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',        # <--- INSIRA SUA SENHA DO MYSQL AQUI
    'database': 'acompanhamento_pacientes_bd'
}

# --- CONFIGURAÇÃO DO NOSQL (MongoDB) ---
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB_NAME = "acompanhamento_pacientes_hibrido_db"

def get_sql_connection():
    return mysql.connector.connect(**SQL_CONFIG)

def gerar_dados_hibridos():
    print("--- INICIANDO SIMULAÇÃO DE SISTEMA HÍBRIDO ---")
    
    # 1. Conexões
    try:
        conn_sql = get_sql_connection()
        cursor_sql = conn_sql.cursor()
        
        client_mongo = MongoClient(MONGO_URI)
        db_mongo = client_mongo[MONGO_DB_NAME]
        
        print("Conectado ao MySQL e MongoDB com sucesso.")
    except Exception as e:
        print(f"Erro de conexão: {e}")
        return

    # ==============================================================================
    # ETAPA 1: GERAR LEITURAS DE EQUIPAMENTOS (IoT)
    # Baseado nos pacientes existentes no SQL
    # ==============================================================================
    print("\n[1/3] Gerando streams de dados de equipamentos (IoT)...")
    
    # Buscar ID e Nome para feedback visual
    cursor_sql.execute("SELECT idPacientes, Nome FROM pacientes")
    pacientes = cursor_sql.fetchall()

    leituras_batch = []
    
    for i, (id_paciente, nome) in enumerate(pacientes):
        # Simula que cada paciente tem um monitor multiparamétrico
        device_id = f"MONITOR_UTI_{random.randint(1000, 9999)}"
        
        # Gerar 50 leituras por paciente (simulando 1 leitura a cada minuto/hora)
        qtd_leituras = 50
        
        for _ in range(qtd_leituras):
            data_leitura = datetime.now() - timedelta(minutes=random.randint(0, 10000))
            
            # Simulação de dados vitais variados
            dados_simulados = {
                "bpm": random.randint(50, 120),
                "saturacao_o2": random.randint(85, 100),
                "pressao_arterial": f"{random.randint(90, 160)}/{random.randint(60, 100)}",
                "temp_pele": round(random.uniform(35.5, 39.5), 1),
                "bateria_sensor": f"{random.randint(10, 100)}%"
            }

            documento = {
                "id_paciente_sql": id_paciente,
                "id_dispositivo": device_id,
                "timestamp": data_leitura,
                "tipo_leitura": "MULTIPARAMETRO_VITAIS",
                "dados": dados_simulados
            }
            leituras_batch.append(documento)
        
        # Feedback visual para os nomes "peculiares"
        if i < 5: 
            print(f"  -> Gerando dados IoT para: {nome} (ID: {id_paciente})")
        elif i == 5:
            print("  -> ... e para os outros 995 pacientes.")

    # Inserção em massa no MongoDB
    if leituras_batch:
        db_mongo.leituras_equipamentos.insert_many(leituras_batch)
        print(f"  Sucesso: {len(leituras_batch)} documentos inseridos em 'leituras_equipamentos'.")

    # ==============================================================================
    # ETAPA 2: SINCRONIZAR DETALHES DE ALERTAS
    # Lê os alertas do SQL e cria o log detalhado (JSON) no MongoDB
    # ==============================================================================
    print("\n[2/3] Migrando detalhes de Alertas para Logs NoSQL...")
    
    # Busca alertas já existentes no SQL para criar o "espelho" de log no Mongo
    cursor_sql.execute("""
        SELECT idAlertas, Pacientes_idPacientes, geracao, nivel_critico 
        FROM alertas
    """)
    alertas_sql = cursor_sql.fetchall()
    
    logs_alertas_batch = []
    
    for (id_alerta, id_paciente, data_geracao, nivel) in alertas_sql:
        # Cria o documento detalhado que o SQL não suporta bem
        log_doc = {
            "id_alerta_sql": id_alerta,
            "id_paciente_sql": id_paciente,
            "timestamp": data_geracao, # Mesma data do SQL
            "nivel_critico": nivel,
            "mensagem": f"O paciente apresentou instabilidade de nível {nivel}.",
            "dados_trigger": {
                "valor_detectado": random.randint(100, 150) if nivel == 'CRITICO' else random.randint(80, 100),
                "limite_configurado": 100,
                "sensor_responsavel": "SENSOR_BPM_OPTICO"
            },
            "status_notificacao": "ENVIADO_PARA_MOBILE_MEDICO"
        }
        logs_alertas_batch.append(log_doc)

    if logs_alertas_batch:
        db_mongo.logs_alertas_disparados.insert_many(logs_alertas_batch)
        print(f"  Sucesso: {len(logs_alertas_batch)} logs detalhados de alertas criados.")

    # ==============================================================================
    # ETAPA 3: GERAR LOGS DE APLICAÇÃO
    # Logs gerais do sistema (não vinculados diretamente a pacientes)
    # ==============================================================================
    print("\n[3/3] Gerando Logs de Sistema (Auditoria)...")
    
    logs_app = []
    servicos = ['API_Gateway', 'Auth_Service', 'Data_Processor_Worker', 'Notification_Service']
    mensagens = [
        'Início do processamento em lote', 
        'Backup realizado com sucesso', 
        'Tentativa de login falha - senha incorreta', 
        'Conexão com sensor perdida e restabelecida',
        'Consulta lenta detectada no endpoint /pacientes'
    ]
    niveis = ['INFO', 'DEBUG', 'WARN', 'ERROR']

    for _ in range(200):
        logs_app.append({
            "timestamp": datetime.now() - timedelta(minutes=random.randint(0, 5000)),
            "nivel_log": random.choice(niveis),
            "servico": random.choice(servicos),
            "mensagem": random.choice(mensagens),
            "detalhes": {
                "cpu_usage": f"{random.randint(20, 90)}%",
                "memory_free": f"{random.randint(1024, 4096)}MB"
            }
        })

    db_mongo.logs_aplicacao.insert_many(logs_app)
    print(f"  Sucesso: {len(logs_app)} logs de aplicação inseridos.")

    # Encerramento
    cursor_sql.close()
    conn_sql.close()
    client_mongo.close()
    print("\n--- PROCESSO CONCLUÍDO ---")
    print("Seu banco de dados híbrido está populado e pronto para uso!")

if __name__ == "__main__":
    gerar_dados_hibridos()