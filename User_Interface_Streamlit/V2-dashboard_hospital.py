import streamlit as st
import mysql.connector
from pymongo import MongoClient
import pandas as pd
import plotly.express as px
import time
import random
from datetime import datetime

# --- CONFIGURAÇÕES ---
SQL_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',  # <--- COLOQUE SUA SENHA AQUI
    'database': 'acompanhamento_pacientes_bd'
}

MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB_NAME = "acompanhamento_pacientes_hibrido_db"

# --- FUNÇÕES DE CONEXÃO E UTILITÁRIOS ---
def get_sql_connection():
    return mysql.connector.connect(**SQL_CONFIG)

def get_mongo_client():
    return MongoClient(MONGO_URI)

def gerar_leitura_iot(id_paciente_sql, device_id="MONITOR_WEB_REQ"):
    """Gera uma leitura simulada e insere no MongoDB"""
    client = get_mongo_client()
    db = client[MONGO_DB_NAME]
    
    dados_simulados = {
        "bpm": random.randint(60, 110),
        "saturacao_o2": random.randint(92, 100),
        "pressao_arterial": f"{random.randint(110, 140)}/{random.randint(70, 90)}",
        "temp_pele": round(random.uniform(36.0, 37.5), 1),
        "bateria_sensor": "100% (AC)"
    }

    documento = {
        "id_paciente_sql": id_paciente_sql,
        "id_dispositivo": device_id,
        "timestamp": datetime.now(),
        "tipo_leitura": "LEITURA_SOB_DEMANDA",
        "dados": dados_simulados
    }
    
    db.leituras_equipamentos.insert_one(documento)
    client.close()
    return dados_simulados

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Sistema Hospitalar Híbrido", page_icon="🏥", layout="wide")

st.markdown("""
<style>
    .stButton>button { width: 100%; border-radius: 5px; font-weight: bold;}
    .success-msg { color: #00CC96; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- MENU LATERAL ---
st.sidebar.title("🏥 Menu Hospitalar")
pagina = st.sidebar.radio("Ir para:", ["Monitoramento UTI", "Cadastrar Paciente"])

# ==============================================================================
# PÁGINA 1: MONITORAMENTO (COM GERADOR DE LOGS)
# ==============================================================================
if pagina == "Monitoramento UTI":
    st.title("📊 Monitoramento de Pacientes")

    conn_sql = get_sql_connection()
    cursor = conn_sql.cursor(dictionary=True)

    # SelectBox de Pacientes
    cursor.execute("SELECT idPacientes, Nome FROM pacientes ORDER BY Nome")
    pacientes_list = cursor.fetchall()
    opcoes_pacientes = {p['Nome']: p['idPacientes'] for p in pacientes_list}

    if not opcoes_pacientes:
        st.warning("Nenhum paciente encontrado no banco SQL.")
        st.stop()

    nome_selecionado = st.selectbox("Buscar Paciente:", options=list(opcoes_pacientes.keys()))
    id_paciente_selecionado = opcoes_pacientes[nome_selecionado]

    # --- DADOS CADASTRAIS (SQL) ---
    cursor.execute("""
        SELECT p.*, b.Nome_do_Bairro, c.Nome_da_Cidade 
        FROM pacientes p
        JOIN bairros b ON p.Bairros_idBairros = b.idBairros
        JOIN cidades c ON b.Cidades_idCidades = c.idCidades
        WHERE p.idPacientes = %s
    """, (id_paciente_selecionado,))
    dados_sql = cursor.fetchone()
    conn_sql.close()

    # Badge e Info
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.markdown(f"### Paciente: **{dados_sql['Nome']}**")
        st.caption(f"CPF: {dados_sql['CPF']} | Idade: {dados_sql['idade']} anos")
    with col2:
        st.write(f"**Cidade:** {dados_sql['Nome_da_Cidade']}")
    with col3:
        status = dados_sql['Status']
        cor = "green" if status == 'A' else "red"
        st.markdown(f"### Status: :{cor}[{'ATIVO' if status == 'A' else 'INATIVO'}]")

    st.divider()

    # --- ÁREA DE AÇÃO: GERAR LOGS (MONGODB) ---
    col_btn, col_info = st.columns([1, 3])
    with col_btn:
        if st.button("📡 Gerar Nova Leitura Agora"):
            novos_dados = gerar_leitura_iot(id_paciente_selecionado)
            st.success("Dados enviados ao MongoDB!")
            time.sleep(0.5) # Pequeno delay para garantir que o Mongo processe
            st.rerun() # Recarrega a página para mostrar o gráfico atualizado
    with col_info:
        st.caption("Clique para simular o envio de dados de um monitor cardíaco em tempo real.")

    # --- GRÁFICOS (NOSQL) ---
    client = get_mongo_client()
    db = client[MONGO_DB_NAME]
    
    # Buscar logs
    cursor_mongo = db.leituras_equipamentos.find(
        {"id_paciente_sql": int(id_paciente_selecionado)}
    ).sort("timestamp", -1).limit(50) # Pegar últimos 50

    dados_mongo = list(cursor_mongo)
    client.close()

    if dados_mongo:
        df_leituras = pd.DataFrame([
            {
                "Hora": d['timestamp'],
                "BPM": d['dados'].get('bpm'),
                "Saturacao": d['dados'].get('saturacao_o2')
            } for d in dados_mongo
        ]).sort_values(by="Hora")

        # Métricas atuais
        ultima = dados_mongo[0]['dados']
        m1, m2, m3 = st.columns(3)
        m1.metric("BPM Atual", ultima.get('bpm'))
        m2.metric("Saturação O2", f"{ultima.get('saturacao_o2')}%")
        m3.metric("Pressão", ultima.get('pressao_arterial'))

        # Gráficos
        tab1, tab2 = st.tabs(["Monitor Cardíaco", "Oximetria"])
        with tab1:
            fig = px.line(df_leituras, x="Hora", y="BPM", markers=True, title="Batimentos por Minuto")
            fig.update_traces(line_color='#FF4B4B')
            st.plotly_chart(fig, use_container_width=True)
        with tab2:
            fig2 = px.area(df_leituras, x="Hora", y="Saturacao", markers=True, title="Saturação %")
            fig2.update_traces(line_color='#00CC96')
            fig2.update_layout(yaxis_range=[80, 100])
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Sem dados recentes. Clique no botão acima para gerar.")

# ==============================================================================
# PÁGINA 2: CADASTRO DE PACIENTE (SQL)
# ==============================================================================
elif pagina == "Cadastrar Paciente":
    st.title("📝 Novo Cadastro de Paciente")
    st.markdown("Os dados serão salvos no banco **Relacional (SQL)**.")

    # Buscar Bairros para o Dropdown (Necessário para a FK)
    conn_sql = get_sql_connection()
    cursor = conn_sql.cursor()
    cursor.execute("SELECT idBairros, Nome_do_Bairro FROM bairros LIMIT 50") # Limitando p/ demo
    bairros = cursor.fetchall()
    dict_bairros = {b[1]: b[0] for b in bairros}
    conn_sql.close()

    with st.form("form_cadastro"):
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input("Nome Completo")
            cpf = st.text_input("CPF (somente números)")
            email = st.text_input("Email")
            telefone = st.text_input("Telefone")
        
        with col2:
            data_nasc = st.date_input("Data de Nascimento")
            genero = st.selectbox("Gênero", ["M", "F"])
            bairro_nome = st.selectbox("Bairro", list(dict_bairros.keys()))
            numero_casa = st.number_input("Número da Casa", min_value=1, step=1)
        
        st.divider()
        st.subheader("Contato de Emergência")
        ce_nome = st.text_input("Nome do Contato")
        ce_tel = st.text_input("Telefone do Contato")

        submitted = st.form_submit_button("💾 Salvar Paciente no SQL")

        if submitted:
            if nome and cpf and bairro_nome:
                try:
                    conn = get_sql_connection()
                    cursor = conn.cursor()
                    
                    # Lógica simplificada de idade
                    idade = datetime.now().year - data_nasc.year
                    id_bairro = dict_bairros[bairro_nome]

                    sql = """INSERT INTO pacientes 
                             (Nome, idade, Data_de_Nascimento, CPF, Email, Telefone, Numero_da_casa, 
                              Genero, Contato_Emergencial_Nome, Contato_Emergencial_Telefone, 
                              Status, Data_Cadastro, Bairros_idBairros) 
                             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    
                    val = (nome, idade, data_nasc, cpf, email, telefone, numero_casa, 
                           genero, ce_nome, ce_tel, 'A', datetime.now(), id_bairro)
                    
                    cursor.execute(sql, val)
                    conn.commit()
                    
                    # Inserir limites de alerta padrão automaticamente
                    id_novo_paciente = cursor.lastrowid
                    cursor.execute("INSERT INTO limites_alerta (Valor_minimo, Valor_Maximo, Pacientes_idPacientes) VALUES (60, 100, %s)", (id_novo_paciente,))
                    conn.commit()

                    conn.close()
                    st.success(f"Paciente {nome} cadastrado com sucesso! (ID: {id_novo_paciente})")
                    st.balloons()
                except mysql.connector.Error as err:
                    st.error(f"Erro ao salvar no SQL: {err}")
            else:
                st.error("Por favor, preencha os campos obrigatórios (Nome, CPF, Bairro).")