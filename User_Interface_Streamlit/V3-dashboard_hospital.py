import streamlit as st
import mysql.connector
from pymongo import MongoClient
import pandas as pd
import plotly.express as px
import time
import random
from datetime import datetime, date

# --- CONFIGURAÇÕES ---
SQL_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',  # <--- COLOQUE SUA SENHA AQUI
    'database': 'acompanhamento_pacientes_bd'
}

MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB_NAME = "acompanhamento_pacientes_hibrido_db"

# --- FUNÇÕES DE CONEXÃO ---
def get_sql_connection():
    return mysql.connector.connect(**SQL_CONFIG)

def get_mongo_client():
    return MongoClient(MONGO_URI)

# --- FUNÇÃO: CHAMADA DA STORED PROCEDURE (SQL) ---
def consultar_sql_via_proc(id_paciente, tipo_medicao):
    """Busca a última medição oficial usando a Stored Procedure"""
    conn = get_sql_connection()
    cursor = conn.cursor(dictionary=True)
    resultado = None
    try:
        cursor.callproc('SP_Obter_Ultima_Medicao', [id_paciente, tipo_medicao])
        for res in cursor.stored_results():
            resultado = res.fetchone()
    except mysql.connector.Error as err:
        st.error(f"Erro Procedure: {err}")
    finally:
        cursor.close()
        conn.close()
    return resultado

# --- FUNÇÃO: GERADOR HÍBRIDO (MONGO + SQL TRIGGER) ---
def gerar_leitura_iot(id_paciente_sql, device_id="MONITOR_WEB_REQ"):
    """
    1. Insere no MongoDB (para o gráfico em tempo real).
    2. Insere no SQL (para testar o TRIGGER de alerta crítico).
    """
    client = get_mongo_client()
    db = client[MONGO_DB_NAME]
    
    # Gerar dados (com chance de ser crítico para testar o trigger)
    bpm = random.randint(55, 115) # Limites normais aprox 60-100
    saturacao = random.randint(88, 100) # Crítico abaixo de 90
    
    dados_simulados = {
        "bpm": bpm,
        "saturacao_o2": saturacao,
        "pressao_arterial": f"{random.randint(110, 140)}/{random.randint(70, 90)}",
        "temp_pele": round(random.uniform(36.0, 37.5), 1),
        "bateria_sensor": "100% (AC)"
    }

    # 1. Inserir no MongoDB
    doc_mongo = {
        "id_paciente_sql": id_paciente_sql,
        "id_dispositivo": device_id,
        "timestamp": datetime.now(),
        "tipo_leitura": "SINAIS_VITAIS",
        "dados": dados_simulados
    }
    db.leituras_equipamentos.insert_one(doc_mongo)
    client.close()

    # 2. Inserir no SQL (Isso vai disparar o TRIGGER 'tr_gerar_alerta_critico' se os valores forem ruins)
    try:
        conn = get_sql_connection()
        cursor = conn.cursor()
        # Inserindo BPM
        sql_insert = """INSERT INTO medicao (medicao, tipo_medicao, valor, unidade_medida, Pacientes_idPacientes) 
                        VALUES (NOW(), 'Batimento Cardíaco', %s, 'bpm', %s)"""
        cursor.execute(sql_insert, (bpm, id_paciente_sql))
        # Inserindo Saturação (Opcional, mas bom para registro completo)
        sql_insert_o2 = """INSERT INTO medicao (medicao, tipo_medicao, valor, unidade_medida, Pacientes_idPacientes) 
                           VALUES (NOW(), 'Saturação O2', %s, '%%', %s)"""
        cursor.execute(sql_insert_o2, (saturacao, id_paciente_sql))
        
        conn.commit()
        conn.close()
    except Exception as e:
        st.error(f"Erro SQL: {e}")

    return dados_simulados

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Monitor UTI Pro", page_icon="🏥", layout="wide")

st.markdown("""
<style>
    .stButton>button { width: 100%; border-radius: 5px; font-weight: bold; height: 3em; }
    .metric-card { background-color: #262730; padding: 15px; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# --- MENU LATERAL ---
st.sidebar.title("🏥 Monitor Pro")
pagina = st.sidebar.radio("Navegação:", ["Monitoramento em Tempo Real", "Admissão de Paciente"])

# ==============================================================================
# PÁGINA 1: MONITORAMENTO (UI V2 + BACKEND V3)
# ==============================================================================
if pagina == "Monitoramento em Tempo Real":
    
    # --- BUSCA DE PACIENTE (SQL) ---
    conn_sql = get_sql_connection()
    cursor = conn_sql.cursor(dictionary=True)
    cursor.execute("SELECT idPacientes, Nome FROM pacientes ORDER BY Nome")
    opcoes_pacientes = {p['Nome']: p['idPacientes'] for p in cursor.fetchall()}
    conn_sql.close()

    if not opcoes_pacientes:
        st.warning("Sem pacientes no banco.")
        st.stop()

    nome_selecionado = st.sidebar.selectbox("Selecione o Leito/Paciente:", options=list(opcoes_pacientes.keys()))
    id_paciente = opcoes_pacientes[nome_selecionado]

    # --- CABEÇALHO DO PACIENTE ---
    conn_sql = get_sql_connection()
    cursor = conn_sql.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.*, c.Nome_da_Cidade 
        FROM pacientes p
        JOIN bairros b ON p.Bairros_idBairros = b.idBairros
        JOIN cidades c ON b.Cidades_idCidades = c.idCidades
        WHERE p.idPacientes = %s
    """, (id_paciente,))
    dados_p = cursor.fetchone()
    conn_sql.close()

    c1, c2, c3 = st.columns([3, 2, 2])
    with c1:
        st.title(f"🩺 {dados_p['Nome']}")
        st.caption(f"ID: {id_paciente} | CPF: {dados_p['CPF']}")
    with c2:
        st.metric("Idade", f"{dados_p['idade']} Anos")
    with c3:
        # Botão de Ação (Gera dados híbridos)
        if st.button("📡 Simular Sensor (Gerar Leitura)"):
            gerar_leitura_iot(id_paciente)
            st.success("Leitura enviada!")
            time.sleep(0.5)
            st.rerun()

    st.divider()

    # --- VISUALIZAÇÃO (MONGODB) ---
    client = get_mongo_client()
    db = client[MONGO_DB_NAME]
    
    # Buscar últimos 50 registros
    logs_mongo = list(db.leituras_equipamentos.find(
        {"id_paciente_sql": int(id_paciente)}
    ).sort("timestamp", -1).limit(50))
    
    client.close()

    if logs_mongo:
        df = pd.DataFrame([{
            "Hora": d['timestamp'],
            "BPM": d['dados'].get('bpm'),
            "Saturacao": d['dados'].get('saturacao_o2'),
            "Pressao": d['dados'].get('pressao_arterial')
        } for d in logs_mongo]).sort_values(by="Hora")
        
        ultima = logs_mongo[0]['dados']

        # 1. CARDS DE MÉTRICAS
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("BPM (Cardíaco)", f"{ultima.get('bpm')} ❤️", delta_color="inverse")
        m2.metric("Saturação O2", f"{ultima.get('saturacao_o2')}% 🌬️") 
        m3.metric("Pressão Arterial", ultima.get('pressao_arterial'))
        m4.metric("Temp. Pele", f"{ultima.get('temp_pele')} °C")

        # 2. GRÁFICOS
        tab_bpm, tab_o2 = st.tabs(["📈 Monitor Cardíaco", "📉 Oximetria"])
        
        with tab_bpm:
            fig_bpm = px.line(df, x="Hora", y="BPM", markers=True, title="Histórico de Batimentos", height=350)
            fig_bpm.update_traces(line_color='#FF4B4B', line_width=3)
            st.plotly_chart(fig_bpm, use_container_width=True)
            
        with tab_o2:
            fig_o2 = px.area(df, x="Hora", y="Saturacao", markers=True, title="Saturação de Oxigênio (%)", height=350)
            fig_o2.update_traces(line_color='#00CC96')
            fig_o2.update_layout(yaxis_range=[80, 100])
            st.plotly_chart(fig_o2, use_container_width=True)

    else:
        st.info("Nenhuma leitura encontrada. Clique no botão 'Simular Sensor' acima.")

    # --- RODAPÉ TÉCNICO ---
    with st.expander("🔍 Auditoria Técnica & Alertas (Backend SQL)", expanded=True):
        col_proc, col_trig = st.columns(2)
        
        with col_proc:
            st.markdown("#### Último Registro Oficial (Via Stored Procedure)")
            st.caption("Consulta direta ao SQL via `SP_Obter_Ultima_Medicao`")
            
            dado_proc = consultar_sql_via_proc(id_paciente, 'Batimento Cardíaco')
            
            if dado_proc:
                st.info(f"📅 Data: {dado_proc['Timestamp_Medicao']} \n\n ❤️ Valor: **{dado_proc['Valor_Medido']} {dado_proc['Unidade']}**")
            else:
                st.warning("Nenhum registro clínico oficial encontrado.")

        with col_trig:
            st.markdown("#### Alertas Disparados (Via Trigger)")
            st.caption("Alertas gerados automaticamente pelo banco `tr_gerar_alerta_critico`")
            
            conn_sql = get_sql_connection()
            cursor = conn_sql.cursor(dictionary=True)
            cursor.execute("""
                SELECT idAlertas, geracao, nivel_critico, status 
                FROM alertas WHERE Pacientes_idPacientes = %s 
                ORDER BY geracao DESC LIMIT 3
            """, (id_paciente,))
            alertas = cursor.fetchall()
            conn_sql.close()
            
            if alertas:
                st.dataframe(pd.DataFrame(alertas), use_container_width=True, hide_index=True)
            else:
                st.success("Nenhum alerta crítico ativo.")

# ==============================================================================
# PÁGINA 2: CADASTRO (COMPLETO)
# ==============================================================================
elif pagina == "Admissão de Paciente":
    st.title("📝 Admissão de Paciente (SQL)")
    st.markdown("Preencha todos os campos obrigatórios para o cadastro no sistema hospitalar.")
    
    conn = get_sql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT idBairros, Nome_do_Bairro FROM bairros LIMIT 50")
    bairros = {b[1]: b[0] for b in cursor.fetchall()}
    conn.close()

    with st.form("cadastro"):
        col1, col2 = st.columns(2)
        
        # Coluna 1
        with col1:
            nome = st.text_input("Nome Completo *")
            cpf = st.text_input("CPF *")
            email = st.text_input("E-mail *")
            telefone = st.text_input("Telefone *")
            nasc = st.date_input("Data Nascimento *", min_value=date(1900, 1, 1), max_value=datetime.now())
        
        # Coluna 2
        with col2:
            bairro = st.selectbox("Bairro *", list(bairros.keys()))
            num_casa = st.number_input("Número da Casa *", min_value=1, step=1)
            genero = st.selectbox("Gênero", ["M", "F"])
            st.divider()
            st.markdown("**Contato de Emergência**")
            emerg_nome = st.text_input("Nome do Contato *")
            emerg_tel = st.text_input("Telefone Emergência *")
        
        submitted = st.form_submit_button("💾 Salvar Paciente")
        
        if submitted:
            # Validação simples para campos vazios
            if not nome or not cpf or not email or not telefone or not emerg_nome:
                st.error("Preencha todos os campos obrigatórios.")
            else:
                try:
                    conn = get_sql_connection()
                    cursor = conn.cursor()
                    idade = datetime.now().year - nasc.year
                    
                    # Query completa com todos os campos
                    sql = """INSERT INTO pacientes 
                        (Nome, idade, Data_de_Nascimento, CPF, Email, Telefone, Numero_da_casa, Genero, 
                         Contato_Emergencial_Nome, Contato_Emergencial_Telefone, Status, Data_Cadastro, Bairros_idBairros) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'A', NOW(), %s)"""
                    
                    valores = (nome, idade, nasc, cpf, email, telefone, num_casa, genero, emerg_nome, emerg_tel, bairros[bairro])
                    
                    cursor.execute(sql, valores)
                    novo_id = cursor.lastrowid
                    
                    # Inserir limites padrão para o trigger funcionar
                    cursor.execute("INSERT INTO limites_alerta VALUES (NULL, 60, 100, %s)", (novo_id,))
                    
                    conn.commit()
                    conn.close()
                    st.success(f"Paciente {nome} cadastrado com sucesso! ID: {novo_id}")
                    st.balloons()
                except mysql.connector.Error as err:
                    st.error(f"Erro ao salvar no Banco de Dados: {err}")