
import faker
from faker.providers import person, phone_number, address, internet
import random
from datetime import datetime, timedelta
import csv

# --- CONFIGURAÇÕES ---
NUM_PROFISSIONAIS = 50
NUM_PACIENTES = 1000
MEDICOES_POR_DISPOSITIVO = 20 # Média de medições por dispositivo
CHANCE_DE_ALERTA = 0.05 # 5% de chance de uma medição gerar um alerta

# --- INICIALIZAÇÃO DO FAKER ---
fake = faker.Faker('pt_BR')
fake.add_provider(person)
fake.add_provider(phone_number)
fake.add_provider(address)
fake.add_provider(internet)

# --- LISTAS DE DADOS ---
especialidades = ['Cardiologia', 'Endocrinologia', 'Pneumologia', 'Clínica Geral', 'Geriatria']
tipos_dispositivos = {
    'Cardiologia': [('Monitor Cardíaco', 'bpm'), ('Monitor de Pressão', 'mmHg')],
    'Endocrinologia': [('Glicosímetro', 'mg/dL')],
    'Pneumologia': [('Oxímetro', '%'), ('Espirometro', 'L/s')],
    'Clínica Geral': [('Termômetro', '°C'), ('Oxímetro', '%')],
    'Geriatria': [('Monitor de Pressão', 'mmHg'), ('Oxímetro', '%'), ('Monitor de Queda', 'status')]
}
niveis_alerta = ['Baixo', 'Médio', 'Alto', 'Crítico']

# --- FUNÇÕES GERADORAS ---
def gerar_crm(uf='SP'):
    return f"CRM/{uf} {random.randint(100000, 999999)}"

def gerar_valor_medicao(tipo):
    if tipo == 'Monitor Cardíaco': return str(random.randint(55, 120))
    if tipo == 'Monitor de Pressão': return f"{random.randint(110, 160)}/{random.randint(70, 100)}"
    if tipo == 'Glicosímetro': return str(random.randint(70, 250))
    if tipo == 'Oxímetro': return str(random.randint(92, 100))
    if tipo == 'Termômetro': return f"{random.uniform(36.1, 39.5):.1f}"
    if tipo == 'Espirometro': return f"{random.uniform(3.0, 5.0):.2f}"
    if tipo == 'Monitor de Queda': return random.choice(['Nenhuma queda detectada', 'Queda detectada'])
    return 'N/A'

# --- GERAÇÃO DOS DADOS ---
with open('dados_monitoramento.sql', 'w', encoding='utf-8') as f:
    f.write("-- Script de Inserção de Dados para o SMRP\n\n")

    # 1. Gerar Profissionais de Saúde
    f.write("-- 1. INSERINDO PROFISSIONAIS DE SAÚDE\n")
    profissionais_ids = list(range(1, NUM_PROFISSIONAIS + 1))
    for i in profissionais_ids:
        nome = fake.name()
        especialidade = random.choice(especialidades)
        crm = gerar_crm()
        email = fake.email()
        f.write(f"INSERT INTO ProfissionaisSaude (NomeCompleto, Especialidade, CRM, TelefoneContato, Email) VALUES ('{nome.replace('\'', '\'\'')}', '{especialidade}', '{crm}', '{fake.phone_number()}', '{email}');\n")
    
    f.write("\n-- 2. INSERINDO PACIENTES E SEUS DISPOSITIVOS\n")
    paciente_ids = list(range(1, NUM_PACIENTES + 1))
    dispositivo_id_counter = 1
    medicao_id_counter = 1
    alerta_id_counter = 1
    
    medicoes_buffer = []
    alertas_buffer = []

    for i in paciente_ids:
        nome_paciente = fake.name()
        cpf = fake.cpf()
        email_paciente = fake.free_email()
        profissional_id = random.choice(profissionais_ids)

        # Inserir Paciente
        f.write(f"INSERT INTO Pacientes (NomeCompleto, DataNascimento, CPF, Endereco, Telefone, Email, ProfissionalResponsavelID) VALUES ('{nome_paciente.replace('\'', '\'\'')}', '{fake.date_of_birth(minimum_age=20, maximum_age=90)}', '{cpf}', '{fake.address().replace('\'', '\'\'').replace('\n', ', ')}', '{fake.phone_number()}', '{email_paciente}', {profissional_id});\n")

        # Inserir Dispositivos para o Paciente
        especialidade_profissional = especialidades[(profissional_id - 1) % len(especialidades)]
        dispositivos_paciente = tipos_dispositivos.get(especialidade_profissional, tipos_dispositivos['Clínica Geral'])

        for tipo_disp, unidade in dispositivos_paciente:
            f.write(f"INSERT INTO Dispositivos (PacienteID, TipoDispositivo, Modelo, NumeroSerie, DataAquisicao) VALUES ({i}, '{tipo_disp}', 'Modelo {random.choice(['X', 'Y', 'Z'])}-{random.randint(100,999)}', '{fake.uuid4()}', '{fake.date_this_decade()}');\n")
            
            # Gerar Medições para o Dispositivo
            for _ in range(MEDICOES_POR_DISPOSITIVO):
                timestamp = fake.date_time_this_year()
                valor = gerar_valor_medicao(tipo_disp)
                medicoes_buffer.append(f"({dispositivo_id_counter}, '{timestamp}', '{tipo_disp}', '{valor}', '{unidade}')")
                
                # Chance de gerar um alerta
                if random.random() < CHANCE_DE_ALERTA:
                    nivel = random.choice(niveis_alerta)
                    descricao = f"Alerta de nível {nivel} para {tipo_disp} com valor {valor}."
                    alertas_buffer.append(f"({medicao_id_counter}, {i}, '{timestamp + timedelta(seconds=5)}', '{nivel}', '{descricao}')")
                    alerta_id_counter += 1
                medicao_id_counter += 1

            dispositivo_id_counter += 1

    # Escrever medições e alertas em lote para melhor performance
    f.write("\n-- 3. INSERINDO MEDIÇÕES DE SAÚDE\n")
    f.write("INSERT INTO MedicoesSaude (DispositivoID, TimestampMedicao, TipoMedicao, ValorMedicao, UnidadeMedida) VALUES\n")
    f.write(',\n'.join(medicoes_buffer) + ';\n')

    if alertas_buffer:
        f.write("\n-- 4. INSERINDO ALERTAS\n")
        f.write("INSERT INTO Alertas (MedicaoID, PacienteID, TimestampAlerta, NivelPrioridade, Descricao) VALUES\n")
        f.write(',\n'.join(alertas_buffer) + ';\n')

print("Arquivo 'dados_monitoramento.sql' gerado com sucesso!")