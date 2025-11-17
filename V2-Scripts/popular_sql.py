import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta

# --- CONFIGURAÇÃO DO BANCO DE DADOS ---
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',        # Seu usuário do MySQL
    'password': '',        # <--- INSIRA SUA SENHA AQUI
    'database': 'acompanhamento_pacientes_bd'
}

fake = Faker('pt_BR') # Gerador de dados brasileiros

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def populate_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    print("Iniciando a população do Banco de Dados Relacional...")

    # 1. Criar Localização (País -> Estado -> Cidade -> Bairro)
    print("- Criando dados geográficos...")
    
    # País
    cursor.execute("INSERT INTO paises (Nome_do_País, Sigla) VALUES (%s, %s)", ('Brasil', 'BR'))
    id_pais = cursor.lastrowid

    # Estados (5 estados aleatórios)
    estados_ids = []
    for _ in range(5):
        estado = fake.state()
        sigla = fake.state_abbr()
        cursor.execute("INSERT INTO estados (Nome_do_Estado, Sigla, Países_idPaises) VALUES (%s, %s, %s)", 
                       (estado, sigla, id_pais))
        estados_ids.append(cursor.lastrowid)

    # Cidades (20 cidades)
    cidades_ids = []
    for _ in range(20):
        cidade = fake.city()
        id_estado = random.choice(estados_ids)
        cursor.execute("INSERT INTO cidades (Nome_da_Cidade, Estados_idEstados) VALUES (%s, %s)", 
                       (cidade, id_estado))
        cidades_ids.append(cursor.lastrowid)

    # Bairros (50 bairros)
    bairros_ids = []
    for _ in range(50):
        bairro = fake.bairro()
        id_cidade = random.choice(cidades_ids)
        cursor.execute("INSERT INTO bairros (Nome_do_Bairro, Cidades_idCidades) VALUES (%s, %s)", 
                       (bairro, id_cidade))
        bairros_ids.append(cursor.lastrowid)

    conn.commit()

    # 2. Criar Profissionais (50 médicos/enfermeiros)
    print("- Criando 50 profissionais de saúde...")
    profissionais_ids = []
    for _ in range(50):
        sql = """INSERT INTO profissionais 
                 (Nome, idade, Data_de_Nascimento, CPF, Email, Telefone, Numero_da_casa, Genero, Status) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        val = (fake.name(), random.randint(25, 65), fake.date_of_birth(minimum_age=25, maximum_age=65),
               fake.cpf(), fake.email(), fake.phone_number(), random.randint(1, 999), 
               random.choice(['M', 'F']), 'A')
        cursor.execute(sql, val)
        profissionais_ids.append(cursor.lastrowid)
    conn.commit()

    # 3. Criar Pacientes (1000 registros)
    print("- Criando 1000 pacientes e dados relacionados...")
    
    for i in range(1000):
        # Inserir Paciente
        id_bairro = random.choice(bairros_ids)
        sql_paciente = """INSERT INTO pacientes 
                          (Nome, idade, Data_de_Nascimento, CPF, Email, Telefone, Numero_da_casa, 
                           Genero, Contato_Emergencial_Nome, Contato_Emergencial_Telefone, 
                           Status, Data_Cadastro, Bairros_idBairros) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        
        # Gerar dados
        genero = random.choice(['M', 'F'])
        nome = fake.name_male() if genero == 'M' else fake.name_female()
        idade = random.randint(18, 90)
        nasc = fake.date_of_birth(minimum_age=18, maximum_age=90)
        
        val_paciente = (nome, idade, nasc, fake.unique.cpf(), fake.unique.email(), fake.phone_number(),
                        random.randint(1, 2000), genero, fake.name(), fake.phone_number(),
                        'A', fake.date_between(start_date='-2y', end_date='today'), id_bairro)
        
        cursor.execute(sql_paciente, val_paciente)
        id_paciente = cursor.lastrowid

        # 3.1 Associar a Profissionais (1 a 3 médicos por paciente)
        num_medicos = random.randint(1, 3)
        medicos_escolhidos = random.sample(profissionais_ids, num_medicos)
        for id_prof in medicos_escolhidos:
            cursor.execute("INSERT INTO pacientes_has_profissionais VALUES (%s, %s)", (id_paciente, id_prof))

        # 3.2 Criar Convênio (80% de chance de ter)
        if random.random() < 0.8:
            sql_conv = "INSERT INTO convenios (nome_convenio, cnpj, registro_ans, Pacientes_idPacientes) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql_conv, (fake.company(), fake.cnpj(), fake.random_number(digits=6), id_paciente))

        # 3.3 Criar Limites de Alerta (Essencial para a lógica do MongoDB depois)
        # Cada paciente tem limites diferentes baseados na idade (simulação simples)
        min_bpm = 50 if idade < 60 else 55
        max_bpm = 100 if idade < 60 else 90
        sql_limites = "INSERT INTO limites_alerta (Valor_minimo, Valor_Maximo, Pacientes_idPacientes) VALUES (%s, %s, %s)"
        cursor.execute(sql_limites, (min_bpm, max_bpm, id_paciente))

        # 3.4 Histórico Médico (Alguns registros aleatórios)
        for _ in range(random.randint(0, 3)):
            sql_hist = "INSERT INTO historico_medico (data_evento, tipo_evento, descrição_detalhada, Pacientes_idPacientes) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql_hist, (fake.date_between(start_date='-5y'), random.choice(['Consulta', 'Exame', 'Cirurgia']), fake.sentence(), id_paciente))

        # Feedback visual a cada 100 registros
        if (i + 1) % 100 == 0:
            print(f"  -- {i + 1} pacientes processados...")
            conn.commit()

    conn.commit()
    cursor.close()
    conn.close()
    print("Sucesso! Banco de dados SQL populado com 1000 pacientes.")

if __name__ == "__main__":
    populate_db()