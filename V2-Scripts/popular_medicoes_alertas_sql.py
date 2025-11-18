import mysql.connector
import random
from datetime import datetime, timedelta

# --- CONFIGURAÇÃO DO BANCO DE DADOS ---
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',        # Seu usuário do MySQL
    'password': '',        # <--- INSIRA SUA SENHA AQUI
    'database': 'acompanhamento_pacientes_bd'
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def popular_medicoes_alertas():
    conn = get_connection()
    cursor = conn.cursor()
    
    print("Iniciando a população de Medições e Alertas no SQL...")

    # 1. Buscar todos os IDs de pacientes existentes
    cursor.execute("SELECT idPacientes FROM pacientes")
    pacientes = cursor.fetchall() # Retorna lista de tuplas [(1,), (2,), ...]
    
    if not pacientes:
        print("Erro: Nenhum paciente encontrado. Rode o script 'popular_sql.py' primeiro.")
        return

    total_pacientes = len(pacientes)
    print(f"Encontrados {total_pacientes} pacientes. Gerando histórico...")

    lista_medicoes = []
    lista_alertas = []

    tipos_medicao = [
        ('Batimento Cardíaco', 'bpm', 60, 100),
        ('Saturação O2', '%', 90, 100),
        ('Temperatura', '°C', 36.0, 37.5),
        ('Glicemia', 'mg/dL', 70, 140)
    ]

    niveis_alerta = ['BAIXO', 'MEDIO', 'CRITICO']

    for count, (id_paciente,) in enumerate(pacientes):
        
        # --- Gerar Medições (5 a 10 registros por paciente) ---
        qtd_medicoes = random.randint(5, 10)
        for _ in range(qtd_medicoes):
            # Data aleatória nos últimos 30 dias
            data_med = datetime.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
            
            tipo, unidade, min_val, max_val = random.choice(tipos_medicao)
            
            # Gera um valor (float com 2 casas decimais)
            if tipo == 'Temperatura':
                valor = round(random.uniform(min_val, 39.0), 2) # Chance de febre
            else:
                valor = random.randint(min_val - 10, max_val + 10) # Variação maior

            # Adiciona à lista de batch insert
            # Schema: medicao, tipo_medicao, valor, unidade_medida, Pacientes_idPacientes
            lista_medicoes.append((data_med, tipo, valor, unidade, id_paciente))

        # --- Gerar Alertas (30% de chance do paciente ter alertas no histórico) ---
        if random.random() < 0.30:
            qtd_alertas = random.randint(1, 3)
            for _ in range(qtd_alertas):
                data_alerta = datetime.now() - timedelta(days=random.randint(0, 30))
                nivel = random.choice(niveis_alerta)
                status = random.choice(['A', 'R']) # Ativo ou Resolvido (supondo R=Resolvido)
                
                # Schema: geracao, nivel_critico, status, Pacientes_idPacientes
                lista_alertas.append((data_alerta, nivel, status, id_paciente))
        
        # Feedback visual
        if (count + 1) % 100 == 0:
            print(f"  Processado dados para {count + 1} pacientes...")

    # --- INSERÇÃO EM LOTE (BATCH) PARA VELOCIDADE ---
    print("Inserindo medições no banco...")
    sql_medicao = """INSERT INTO medicao (medicao, tipo_medicao, valor, unidade_medida, Pacientes_idPacientes) 
                     VALUES (%s, %s, %s, %s, %s)"""
    cursor.executemany(sql_medicao, lista_medicoes)
    conn.commit()

    print("Inserindo alertas no banco...")
    sql_alerta = """INSERT INTO alertas (geracao, nivel_critico, status, Pacientes_idPacientes) 
                    VALUES (%s, %s, %s, %s)"""
    cursor.executemany(sql_alerta, lista_alertas)
    conn.commit()

    cursor.close()
    conn.close()
    print(f"Sucesso! Foram inseridas {len(lista_medicoes)} medições e {len(lista_alertas)} alertas.")

if __name__ == "__main__":

    popular_medicoes_alertas()
