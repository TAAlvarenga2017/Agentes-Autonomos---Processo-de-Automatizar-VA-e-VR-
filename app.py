import streamlit as st
import pandas as pd
import ollama
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import json
import os
from datetime import datetime, timedelta
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Automação VR/VA - Gemma3",
    page_icon="🍽️",
    layout="wide"
)

# Título da aplicação
st.title("🤖 Automação da Compra de VR/VA com IA")
st.markdown("**Automatização do processo mensal de compra de Vale Refeição/Alimentação**")
st.markdown("---")

# Função para carregar dados Excel
@st.cache_data
def load_excel_data(file_path):
    """Carrega dados de um arquivo Excel"""
    try:
        # Verifica se o arquivo existe
        if not Path(file_path).exists():
            st.error(f"Arquivo não encontrado: {file_path}")
            return None
        
        # Tenta ler com diferentes engines
        try:
            df = pd.read_excel(file_path, engine='openpyxl')
        except:
            try:
                df = pd.read_excel(file_path, engine='xlrd')
            except:
                df = pd.read_excel(file_path, engine='odf')
        
        # Verifica se o DataFrame está vazio
        if df.empty:
            st.warning(f"Arquivo vazio: {file_path}")
            return None
            
        return df
        
    except Exception as e:
        st.error(f"Erro ao carregar {file_path}: {str(e)}")
        st.error(f"Tipo de erro: {type(e).__name__}")
        return None

# Função para consultar o modelo Gemma3
def query_gemma3(prompt, data_context=""):
    """Faz uma consulta ao modelo Gemma3 do Ollama"""
    try:
        client = ollama.Client()
        
        full_prompt = f"""
        Você é um especialista em recursos humanos e benefícios corporativos. 
        Analise os seguintes dados relacionados ao cálculo de VR/VA e responda à pergunta.
        
        Contexto dos dados:
        {data_context}
        
        Pergunta: {prompt}
        
        Responda de forma clara e objetiva em português, fornecendo insights práticos 
        sobre o cálculo de benefícios, regras trabalhistas e otimizações de processo.
        """
        
        response = client.chat(model='gemma3', messages=[
            {
                'role': 'user',
                'content': full_prompt
            }
        ])
        
        return response['message']['content']
    
    except Exception as e:
        return f"Erro ao consultar o modelo: {str(e)}"

# Função para encontrar coluna de matrícula
def find_matricula_column(df):
    """Encontra a coluna de matrícula baseada em padrões comuns"""
    possible_names = ['MATRÍCULA', 'MATRICULA', 'MATRICULA', 'MAT', 'CODIGO', 'ID', 'CPF', 'FUNCIONARIO', 'COLABORADOR']
    
    # Primeiro tenta nomes exatos
    for col in df.columns:
        if any(name in col.upper() for name in possible_names):
            return col
    
    # Se não encontrar, tenta padrões mais flexíveis
    for col in df.columns:
        col_upper = col.upper()
        # Procura por colunas que contenham números (provavelmente matrículas)
        if any(char.isdigit() for char in col):
            continue  # Pula colunas com números no nome
        
        # Procura por colunas que pareçam identificadores
        if len(col) <= 20 and not any(word in col_upper for word in ['VALOR', 'DIAS', 'BASE', 'SINDICATO', 'CARGO', 'NOME']):
            return col
    
    return None

# Função para calcular dias úteis
def calculate_working_days(start_date, end_date, holidays_list):
    """Calcula dias úteis entre duas datas, excluindo feriados"""
    if pd.isna(start_date) or pd.isna(end_date):
        return 0
    
    # Converte para datetime se necessário
    if isinstance(start_date, str):
        start_date = pd.to_datetime(start_date)
    if isinstance(end_date, str):
        end_date = pd.to_datetime(end_date)
    
    # Cria range de datas
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Remove finais de semana e feriados
    working_days = [d for d in date_range if d.weekday() < 5 and d not in holidays_list]
    
    return len(working_days)

# Função para processar dados de VR/VA
def process_vr_data():
    """Processa todos os dados para cálculo de VR/VA"""
    
    # Carrega todas as bases
    st.info("🔄 Carregando e processando todas as bases de dados...")
    
    # 1. Base de Ativos
    ativos_df = load_excel_data("ATIVOS.xlsx")
    if ativos_df is None:
        st.error("❌ Erro ao carregar base de ATIVOS")
        return None
    
    # 2. Base de Férias
    ferias_df = load_excel_data("FÉRIAS.xlsx")
    if ferias_df is None:
        st.error("❌ Erro ao carregar base de FÉRIAS")
        return None
    
    # 3. Base de Desligados
    desligados_df = load_excel_data("DESLIGADOS.xlsx")
    if desligados_df is None:
        st.error("❌ Erro ao carregar base de DESLIGADOS")
        return None
    
    # 4. Base de Admissões
    admissao_df = load_excel_data("ADMISSÃO ABRIL.xlsx")
    if admissao_df is None:
        st.error("❌ Erro ao carregar base de ADMISSÃO")
        return None
    
    # 5. Base Sindicato x Valor
    sindicato_df = load_excel_data("Base sindicato x valor.xlsx")
    if sindicato_df is None:
        st.error("❌ Erro ao carregar base de SINDICATO")
        return None
    
    # 6. Base de Dias Úteis
    dias_uteis_df = load_excel_data("Base dias uteis.xlsx")
    if dias_uteis_df is None:
        st.error("❌ Erro ao carregar base de DIAS ÚTEIS")
        return None
    
    # 7. Base de Afastamentos
    afastamentos_df = load_excel_data("AFASTAMENTOS.xlsx")
    if afastamentos_df is None:
        st.error("❌ Erro ao carregar base de AFASTAMENTOS")
        return None
    
    # 8. Base de Exterior
    exterior_df = load_excel_data("EXTERIOR.xlsx")
    if exterior_df is None:
        st.error("❌ Erro ao carregar base de EXTERIOR")
        return None
    
    # 9. Base de Estagiários
    estagio_df = load_excel_data("ESTÁGIO.xlsx")
    if estagio_df is None:
        st.error("❌ Erro ao carregar base de ESTÁGIO")
        return None
    
    # 10. Base de Aprendizes
    aprendiz_df = load_excel_data("APRENDIZ.xlsx")
    if aprendiz_df is None:
        st.error("❌ Erro ao carregar base de APRENDIZ")
        return None
    
    st.success("✅ Todas as bases carregadas com sucesso!")
    
    # Processa os dados
    return {
        'ativos': ativos_df,
        'ferias': ferias_df,
        'desligados': desligados_df,
        'admissao': admissao_df,
        'sindicato': sindicato_df,
        'dias_uteis': dias_uteis_df,
        'afastamentos': afastamentos_df,
        'exterior': exterior_df,
        'estagio': estagio_df,
        'aprendiz': aprendiz_df
    }

# Função para aplicar regras de exclusão
def apply_exclusion_rules(consolidated_df, exclusion_data):
    """Aplica regras de exclusão baseadas nas diretrizes"""
    
    st.info("🔍 Aplicando regras de exclusão...")
    
    # Função para encontrar coluna de matrícula
    def find_matricula_column(df):
        """Encontra a coluna de matrícula baseada em padrões comuns"""
        possible_names = ['MATRÍCULA', 'MATRICULA', 'MATRICULA', 'MAT', 'CODIGO', 'ID', 'CPF']
        for col in df.columns:
            if any(name in col.upper() for name in possible_names):
                return col
        return None
    
    # Lista de matrículas para exclusão
    excluded_matriculas = set()
    
    # 1. Diretores, estagiários e aprendizes
    if 'estagio' in exclusion_data and exclusion_data['estagio'] is not None:
        matricula_col = find_matricula_column(exclusion_data['estagio'])
        if matricula_col:
            excluded_matriculas.update(exclusion_data['estagio'][matricula_col].dropna().tolist())
    
    if 'aprendiz' in exclusion_data and exclusion_data['aprendiz'] is not None:
        matricula_col = find_matricula_column(exclusion_data['aprendiz'])
        if matricula_col:
            excluded_matriculas.update(exclusion_data['aprendiz'][matricula_col].dropna().tolist())
    
    # 2. Afastados em geral
    if 'afastamentos' in exclusion_data and exclusion_data['afastamentos'] is not None:
        matricula_col = find_matricula_column(exclusion_data['afastamentos'])
        if matricula_col:
            excluded_matriculas.update(exclusion_data['afastamentos'][matricula_col].dropna().tolist())
    
    # 3. Profissionais no exterior
    if 'exterior' in exclusion_data and exclusion_data['exterior'] is not None:
        matricula_col = find_matricula_column(exclusion_data['exterior'])
        if matricula_col:
            excluded_matriculas.update(exclusion_data['exterior'][matricula_col].dropna().tolist())
    
    # Encontra coluna de matrícula no DataFrame consolidado
    consolidated_matricula_col = find_matricula_column(consolidated_df)
    if not consolidated_matricula_col:
        st.error("❌ Não foi possível encontrar coluna de matrícula no DataFrame consolidado")
        st.write("Colunas disponíveis:", list(consolidated_df.columns))
        return consolidated_df
    
    # Aplica exclusões
    initial_count = len(consolidated_df)
    if excluded_matriculas:
        consolidated_df = consolidated_df[~consolidated_df[consolidated_matricula_col].isin(excluded_matriculas)]
        final_count = len(consolidated_df)
        st.success(f"✅ Regras de exclusão aplicadas: {initial_count - final_count} registros removidos")
    else:
        st.info("ℹ️ Nenhuma exclusão aplicada (nenhuma matrícula encontrada para exclusão)")
    
    return consolidated_df

# Função para calcular VR/VA
def calculate_vr_va(consolidated_df, sindicato_data, dias_uteis_data, all_data):
    """Calcula VR/VA para cada colaborador"""
    
    st.info("🧮 Calculando VR/VA para cada colaborador...")
    
    # Função para encontrar coluna de matrícula
    def find_matricula_column(df):
        """Encontra a coluna de matrícula baseada em padrões comuns"""
        possible_names = ['MATRÍCULA', 'MATRICULA', 'MATRICULA', 'MAT', 'CODIGO', 'ID', 'CPF']
        for col in df.columns:
            if any(name in col.upper() for name in possible_names):
                return col
        return None
    
    # Função para encontrar coluna de valor VR
    def find_vr_column(df):
        """Encontra a coluna de valor VR"""
        possible_names = ['VALOR_VR', 'VALOR', 'VR', 'VALOR_REF', 'REFEICAO']
        for col in df.columns:
            if any(name in col.upper() for name in possible_names):
                return col
        return None
    
    # Função para encontrar coluna de dias úteis
    def find_dias_column(df):
        """Encontra a coluna de dias úteis"""
        possible_names = ['DIAS_UTEIS', 'DIAS', 'DIAS_TRABALHADOS', 'DIAS_UTEIS']
        for col in df.columns:
            if any(name in col.upper() for name in possible_names):
                return col
        return None
    
    # Encontra colunas necessárias
    consolidated_matricula_col = find_matricula_column(consolidated_df)
    sindicato_vr_col = find_vr_column(sindicato_data) if sindicato_data is not None else None
    dias_dias_col = find_dias_column(dias_uteis_data) if dias_uteis_data is not None else None
    
    # Como as bases de sindicato e dias úteis não têm matrículas,
    # vamos usar a base consolidada como referência
    st.info("ℹ️ Bases de sindicato e dias úteis não têm colunas de matrícula. Usando valores padrão por sindicato.")
    
    # Mostra informações sobre as colunas encontradas
    st.subheader("🔍 Colunas Identificadas")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**DataFrame Consolidado:**")
        st.write(f"- Coluna Matrícula: {consolidated_matricula_col}")
        st.write(f"- Total registros: {len(consolidated_df)}")
        st.write(f"- Todas as colunas: {list(consolidated_df.columns)}")
        
        st.write("**Base Sindicato:**")
        if sindicato_data is not None:
            st.write(f"- Coluna Valor VR: {sindicato_vr_col}")
            st.write(f"- Total registros: {len(sindicato_data)}")
            st.write(f"- Todas as colunas: {list(sindicato_data.columns)}")
            if sindicato_vr_col:
                st.write(f"- Valores únicos: {sindicato_data[sindicato_vr_col].nunique()}")
        else:
            st.write("- Base não disponível")
    
    with col2:
        st.write("**Base Dias Úteis:**")
        if dias_uteis_data is not None:
            st.write(f"- Coluna Dias: {dias_dias_col}")
            st.write(f"- Total registros: {len(dias_uteis_data)}")
            st.write(f"- Todas as colunas: {list(dias_uteis_data.columns)}")
            if dias_dias_col:
                st.write(f"- Valores únicos: {dias_uteis_data[dias_dias_col].nunique()}")
        else:
            st.write("- Base não disponível")
    
    # Verifica se encontrou as colunas necessárias
    if not consolidated_matricula_col:
        st.error("❌ Não foi possível encontrar coluna de matrícula no DataFrame consolidado")
        st.write("Colunas disponíveis:", list(consolidated_df.columns))
        return consolidated_df
    
    # Adiciona colunas de cálculo
    consolidated_df['DIAS_UTEIS'] = 0
    consolidated_df['VALOR_VR'] = 0.0
    consolidated_df['CUSTO_EMPRESA'] = 0.0
    consolidated_df['DESCONTO_FUNCIONARIO'] = 0.0
    
    # Adiciona colunas de controle e observações
    consolidated_df['ADMISSAO'] = 'N/A'
    consolidated_df['COMPETENCIA'] = '05/2025'  # Competência fixa para todo o período
    consolidated_df['OBS_GERAL'] = ''
    
    # Processa cada colaborador
    processed_count = 0
    debug_info = []
    
    # Cria mapeamento de sindicato para valor VR
    sindicato_valor_map = {}
    if sindicato_data is not None and sindicato_vr_col:
        # Assumindo que a primeira coluna é o sindicato
        sindicato_col = sindicato_data.columns[0]
        
        # Debug: mostra as primeiras linhas da base de sindicato
        st.write("🔍 **DEBUG: Primeiras linhas da base de sindicato:**")
        st.write(sindicato_data.head())
        st.write(f"**Coluna sindicato:** {sindicato_col}")
        st.write(f"**Coluna valor:** {sindicato_vr_col}")
        
        for idx, row in sindicato_data.iterrows():
            sindicato = row[sindicato_col]
            valor = row[sindicato_vr_col]
            
            st.write(f"**Linha {idx}:** Sindicato = '{sindicato}', Valor = '{valor}' (tipo: {type(valor)})")
            
            # Converte valor para float
            try:
                if isinstance(valor, str):
                    # Remove caracteres não numéricos e converte
                    valor_limpo = str(valor).replace('R$', '').replace(' ', '').replace(',', '.').strip()
                    valor_float = float(valor_limpo)
                    st.write(f"  ✅ Convertido: '{valor}' → '{valor_limpo}' → {valor_float}")
                else:
                    valor_float = float(valor)
                    st.write(f"  ✅ Convertido: {valor} → {valor_float}")
                
                sindicato_valor_map[sindicato] = valor_float
            except (ValueError, TypeError) as e:
                st.error(f"❌ Erro ao converter valor '{valor}' para sindicato '{sindicato}': {e}")
                sindicato_valor_map[sindicato] = 0.0
        
        st.write(f"**Mapeamento final:** {sindicato_valor_map}")
        
        # Cria mapeamento inteligente por estado
        mapeamento_estado = {
            'SP': 37.5,  # São Paulo
            'RS': 35.0,  # Rio Grande do Sul
            'RJ': 35.0,  # Rio de Janeiro
            'PR': 35.0,  # Paraná
        }
        
        # Mapeamento por palavras-chave nos nomes dos sindicatos
        mapeamento_palavras = {
            'SINDPD SP': 37.5,      # São Paulo
            'SINDPPD RS': 35.0,     # Rio Grande do Sul
            'SINDPPD RJ': 35.0,     # Rio de Janeiro
            'SINDPPD PR': 35.0,     # Paraná
            'SINDPPD SP': 37.5,     # São Paulo
        }
        
        st.write(f"**Mapeamento por estado criado:** {mapeamento_estado}")
        st.write(f"**Mapeamento por palavras-chave criado:** {mapeamento_palavras}")
        
        debug_info.append(f"📊 Mapeamento de sindicatos criado:")
        for sindicato, valor in sindicato_valor_map.items():
            debug_info.append(f"  - {sindicato}: R$ {valor:.2f}")
        debug_info.append("")
    else:
        st.error("❌ Base de sindicato não disponível ou coluna de valor não encontrada")
        st.write(f"sindicato_data: {sindicato_data is not None}")
        st.write(f"sindicato_vr_col: {sindicato_vr_col}")
    
    for idx, row in consolidated_df.iterrows():
        matricula = row[consolidated_matricula_col]
        sindicato = row['Sindicato'] if 'Sindicato' in consolidated_df.columns else 'PADRÃO'
        
        # Debug: mostra o que está sendo processado
        if processed_count < 5:  # Mostra apenas os primeiros 5 para debug
            debug_info.append(f"Processando matrícula: {matricula}, Sindicato: {sindicato}")
        
        # Busca valor do sindicato usando múltiplas estratégias
        valor_sindicato = 0
        
        # Estratégia 1: Busca direta no mapeamento original
        valor_sindicato = sindicato_valor_map.get(sindicato, 0)
        
        # Estratégia 2: Busca por palavras-chave
        if valor_sindicato == 0:
            for palavra_chave, valor in mapeamento_palavras.items():
                if palavra_chave in sindicato.upper():
                    valor_sindicato = valor
                    break
        
        # Estratégia 3: Busca por estado (SP, RS, RJ, PR)
        if valor_sindicato == 0:
            for estado, valor in mapeamento_estado.items():
                if estado in sindicato.upper():
                    valor_sindicato = valor
                    break
        
        # Debug detalhado para os primeiros registros
        if processed_count < 5:
            st.write(f"🔍 **DEBUG Matrícula {matricula}:**")
            st.write(f"  - Sindicato encontrado: '{sindicato}'")
            st.write(f"  - Mapeamento original disponível: {sindicato_valor_map}")
            st.write(f"  - Mapeamento por palavras-chave: {mapeamento_palavras}")
            st.write(f"  - Mapeamento por estado: {mapeamento_estado}")
            st.write(f"  - Valor encontrado: {valor_sindicato}")
        
        # Converte para float se for string
        try:
            if isinstance(valor_sindicato, str):
                # Remove caracteres não numéricos e converte
                valor_sindicato = float(str(valor_sindicato).replace('R$', '').replace(' ', '').replace(',', '.'))
            else:
                valor_sindicato = float(valor_sindicato)
        except (ValueError, TypeError):
            valor_sindicato = 0.0
        
        if processed_count < 5:
            if valor_sindicato > 0:
                debug_info.append(f"  - Valor sindicato encontrado: R$ {valor_sindicato}")
                st.write(f"  ✅ Valor final: R$ {valor_sindicato}")
            else:
                debug_info.append(f"  - Valor sindicato NÃO encontrado para sindicato '{sindicato}'")
                st.write(f"  ❌ Valor NÃO encontrado para sindicato '{sindicato}'")
                st.write(f"  🔍 Sindicatos disponíveis: {list(sindicato_valor_map.keys())}")
                st.write(f"  🔍 Tentando mapeamento inteligente...")
        
        # Busca dias úteis
        dias_uteis = 22  # Padrão mensal
        if dias_uteis_data is not None and dias_dias_col:
            # Usa o valor padrão de dias úteis da base
            dias_uteis_raw = dias_uteis_data[dias_dias_col].iloc[0] if len(dias_uteis_data) > 0 else 22
            
            # Converte para int se for string
            try:
                if isinstance(dias_uteis_raw, str):
                    # Remove caracteres não numéricos e converte
                    dias_uteis = int(str(dias_uteis_raw).replace(' ', '').replace(',', '.').split('.')[0])
                else:
                    dias_uteis = int(float(dias_uteis_raw))
            except (ValueError, TypeError):
                dias_uteis = 22  # Usa valor padrão se não conseguir converter
                st.warning(f"⚠️ Valor inválido para dias úteis: {dias_uteis_raw}, usando padrão: 22")
            
            if processed_count < 5:
                debug_info.append(f"  - Dias úteis: {dias_uteis} (valor da base)")
        else:
            if processed_count < 5:
                debug_info.append(f"  - Dias úteis: {dias_uteis} (valor padrão)")
        
        # Verifica se os valores são numéricos antes do cálculo
        if not isinstance(valor_sindicato, (int, float)) or not isinstance(dias_uteis, (int, float)):
            st.error(f"❌ Erro: valores não numéricos - valor_sindicato: {type(valor_sindicato)} = {valor_sindicato}, dias_uteis: {type(dias_uteis)} = {dias_uteis}")
            valor_sindicato = 0.0
            dias_uteis = 22
        
        # Calcula valores
        valor_total = valor_sindicato * dias_uteis
        custo_empresa = valor_total * 0.8  # 80%
        desconto_funcionario = valor_total * 0.2  # 20%
        
        if processed_count < 5:
            debug_info.append(f"  - Cálculo: R$ {valor_sindicato} × {dias_uteis} = R$ {valor_total}")
            debug_info.append(f"  - Custo empresa: R$ {valor_total} × 0.8 = R$ {custo_empresa}")
            debug_info.append(f"  - Desconto funcionário: R$ {valor_total} × 0.2 = R$ {desconto_funcionario}")
            debug_info.append("")
        
        # Atualiza DataFrame
        consolidated_df.at[idx, 'DIAS_UTEIS'] = dias_uteis
        consolidated_df.at[idx, 'VALOR_VR'] = valor_total
        consolidated_df.at[idx, 'CUSTO_EMPRESA'] = custo_empresa
        consolidated_df.at[idx, 'DESCONTO_FUNCIONARIO'] = desconto_funcionario
        
        # Adiciona colunas de admissão e competência
        consolidated_df.at[idx, 'ADMISSAO'] = 'N/A'
        consolidated_df.at[idx, 'COMPETENCIA'] = '05/2025'  # Competência fixa para todo o período
        consolidated_df.at[idx, 'OBS_GERAL'] = ''
        
        # Busca dados de admissão se disponível
        if 'admissao' in all_data and all_data['admissao'] is not None:
            admissao_df = all_data['admissao']
            # Procura por coluna de matrícula na base de admissão
            admissao_matricula_col = find_matricula_column(admissao_df)
            if admissao_matricula_col:
                admissao_info = admissao_df[admissao_df[admissao_matricula_col] == matricula]
                if not admissao_info.empty:
                    # Procura por coluna de data de admissão
                    for col in admissao_df.columns:
                        if any(palavra in col.upper() for palavra in ['ADMISSAO', 'ADMISSAO', 'DATA', 'INICIO', 'ENTRADA']):
                            data_admissao = admissao_info.iloc[0][col]
                            if pd.notna(data_admissao):
                                try:
                                    if isinstance(data_admissao, str):
                                        data_admissao = pd.to_datetime(data_admissao)
                                    consolidated_df.at[idx, 'ADMISSAO'] = data_admissao.strftime('%d/%m/%Y')
                                except:
                                    consolidated_df.at[idx, 'ADMISSAO'] = str(data_admissao)
                            break
        
        # Gera observações baseadas nos dados
        obs_list = []
        
        # Verifica se é admissão recente
        if consolidated_df.at[idx, 'ADMISSAO'] != 'N/A':
            obs_list.append("Admissão recente")
        
        # Verifica se tem valor VR zero
        if valor_total == 0:
            obs_list.append("Valor VR zero - verificar sindicato")
        
        # Verifica se usa dias úteis padrão
        if dias_uteis == 22:
            obs_list.append("Dias úteis padrão (22)")
        
        # Verifica se é funcionário ativo
        if 'DESC. SITUACAO' in consolidated_df.columns:
            situacao = row['DESC. SITUACAO']
            if 'Férias' in str(situacao):
                obs_list.append("Em férias")
            elif 'Desligado' in str(situacao):
                obs_list.append("Desligado")
        
        # Adiciona observações gerais
        if obs_list:
            consolidated_df.at[idx, 'OBS_GERAL'] = '; '.join(obs_list)
        else:
            consolidated_df.at[idx, 'OBS_GERAL'] = 'OK'
        
        processed_count += 1
    
    # Mostra informações de debug
    if debug_info:
        st.subheader("🔍 Debug do Cálculo (Primeiros 5 registros)")
        for info in debug_info:
            st.text(info)
    
    st.success("✅ Cálculos de VR/VA concluídos!")
    
    return consolidated_df

# Interface principal
def main():
    
    # Sidebar
    st.sidebar.header("🍽️ Automação VR/VA")
    
    # Menu de opções
    menu_option = st.sidebar.selectbox(
        "Escolha uma opção:",
        [
            "🏠 Visão Geral",
            "📊 Processar Dados",
            "🧮 Calcular VR/VA",
            "📋 Relatório Final",
            "🤖 Análise com IA",
            "⚙️ Configurações"
        ]
    )
    
    if menu_option == "🏠 Visão Geral":
        show_overview()
    
    elif menu_option == "📊 Processar Dados":
        show_data_processing()
    
    elif menu_option == "🧮 Calcular VR/VA":
        show_vr_calculation()
    
    elif menu_option == "📋 Relatório Final":
        show_final_report()
    
    elif menu_option == "🤖 Análise com IA":
        show_ai_analysis()
    
    elif menu_option == "⚙️ Configurações":
        show_settings()

def show_overview():
    """Mostra visão geral da aplicação"""
    
    st.header("🏠 Visão Geral da Automação VR/VA")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🎯 Objetivo
        Automatizar o processo mensal de compra de VR (Vale Refeição), garantindo que cada colaborador 
        receba o valor correto, considerando ausências, férias e datas de admissão ou desligamento.
        
        ### 🔄 Processo Atual
        - Cálculo manual a partir de planilhas
        - Conferência manual de datas de contrato
        - Exclusão manual de colaboradores em férias
        - Ajustes manuais para datas quebradas
        - Cálculo manual de dias úteis
        
        ### 🚀 Solução Proposta
        - **Automação completa** do processo
        - **Integração** de múltiplas bases
        - **Validação automática** de dados
        - **Cálculo preciso** de VR/VA
        - **Relatórios automáticos** para fornecedor
        """)
    
    with col2:
        st.markdown("""
        ### 📊 Bases Integradas
        - ✅ ATIVOS
        - ✅ FÉRIAS  
        - ✅ DESLIGADOS
        - ✅ ADMISSÃO
        - ✅ SINDICATO
        - ✅ DIAS ÚTEIS
        - ✅ AFASTAMENTOS
        - ✅ EXTERIOR
        - ✅ ESTÁGIO
        - ✅ APRENDIZ
        
        ### 🤖 Tecnologias
        - **Python** + **Pandas**
        - **Streamlit** (Interface)
        - **Ollama Gemma3** (IA)
        - **Plotly** (Gráficos)
        """)
    
    # Estatísticas dos arquivos
    st.subheader("📈 Estatísticas dos Arquivos")
    
    excel_files = [
        "ATIVOS.xlsx", "FÉRIAS.xlsx", "DESLIGADOS.xlsx", "ADMISSÃO ABRIL.xlsx",
        "Base sindicato x valor.xlsx", "Base dias uteis.xlsx", "AFASTAMENTOS.xlsx",
        "EXTERIOR.xlsx", "ESTÁGIO.xlsx", "APRENDIZ.xlsx"
    ]
    
    stats_data = []
    for file in excel_files:
        file_path = Path(file)
        if file_path.exists():
            try:
                # Tenta diferentes engines
                df = None
                engine_used = "N/A"
                
                for engine in ['openpyxl', 'xlrd', 'odf']:
                    try:
                        df = pd.read_excel(file, engine=engine)
                        engine_used = engine
                        break
                    except Exception as e:
                        continue
                
                if df is not None and not df.empty:
                    stats_data.append({
                        'Arquivo': file,
                        'Linhas': len(df),
                        'Colunas': len(df.columns),
                        'Tamanho': f"{file_path.stat().st_size / 1024:.1f} KB",
                        'Status': '✅ Carregado',
                        'Engine': engine_used
                    })
                else:
                    stats_data.append({
                        'Arquivo': file,
                        'Linhas': 0,
                        'Colunas': 0,
                        'Tamanho': f"{file_path.stat().st_size / 1024:.1f} KB",
                        'Status': '⚠️ Vazio',
                        'Engine': 'N/A'
                    })
                    
            except Exception as e:
                stats_data.append({
                    'Arquivo': file,
                    'Linhas': 0,
                    'Colunas': 0,
                    'Tamanho': f"{file_path.stat().st_size / 1024:.1f} KB" if file_path.exists() else "N/A",
                    'Status': f'❌ Erro: {str(e)[:30]}...',
                    'Engine': 'N/A'
                })
        else:
            stats_data.append({
                'Arquivo': file,
                'Linhas': 0,
                'Colunas': 0,
                'Tamanho': 'N/A',
                'Status': '❌ Não encontrado',
                'Engine': 'N/A'
            })
    
    if stats_data:
        stats_df = pd.DataFrame(stats_data)
        st.dataframe(stats_df, use_container_width=True)
        
        # Resumo dos problemas
        error_count = len([s for s in stats_data if '❌' in s['Status']])
        warning_count = len([s for s in stats_data if '⚠️' in s['Status']])
        success_count = len([s for s in stats_data if '✅' in s['Status']])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("✅ Sucessos", success_count)
        with col2:
            st.metric("⚠️ Avisos", warning_count)
        with col3:
            st.metric("❌ Erros", error_count)

def show_data_processing():
    """Mostra processamento de dados"""
    
    st.header("📊 Processamento de Dados")
    
    if st.button("🔄 Processar Todas as Bases"):
        with st.spinner("Processando bases de dados..."):
            data = process_vr_data()
            
            if data:
                st.session_state['processed_data'] = data
                st.success("✅ Dados processados com sucesso!")
                
                # Mostra resumo dos dados
                st.subheader("📋 Resumo dos Dados Processados")
                
                summary_data = []
                for key, df in data.items():
                    if df is not None:
                        summary_data.append({
                            'Base': key.upper(),
                            'Registros': len(df),
                            'Colunas': len(df.columns),
                            'Colunas Principais': ', '.join(df.columns[:3])
                        })
                
                summary_df = pd.DataFrame(summary_data)
                st.dataframe(summary_df, use_container_width=True)
                
                # Mostra detalhes das colunas
                st.subheader("🔍 Detalhes das Colunas por Base")
                
                for key, df in data.items():
                    if df is not None:
                        with st.expander(f"📊 {key.upper()} - {len(df.columns)} colunas"):
                            col_info = pd.DataFrame({
                                'Coluna': df.columns,
                                'Tipo': df.dtypes,
                                'Valores Únicos': df.nunique(),
                                'Valores Nulos': df.isnull().sum(),
                                'Exemplo': [str(df[col].dropna().iloc[0]) if len(df[col].dropna()) > 0 else 'N/A' for col in df.columns]
                            })
                            st.dataframe(col_info, use_container_width=True)
                
                # Salva dados na sessão
                st.session_state['data_summary'] = summary_data
            else:
                st.error("❌ Erro no processamento dos dados")
    
    # Mostra dados processados se disponível
    if 'processed_data' in st.session_state:
        st.subheader("🔍 Visualização dos Dados Processados")
        
        # Seletor de base
        base_option = st.selectbox(
            "Selecione uma base para visualizar:",
            list(st.session_state['processed_data'].keys())
        )
        
        if base_option:
            df = st.session_state['processed_data'][base_option]
            st.write(f"**Base: {base_option.upper()}** - {len(df)} registros")
            st.dataframe(df.head(10), use_container_width=True)

def show_vr_calculation():
    """Mostra cálculo de VR/VA"""
    
    st.header("🧮 Cálculo de VR/VA")
    
    if 'processed_data' not in st.session_state:
        st.warning("⚠️ Processe os dados primeiro na aba 'Processar Dados'")
        return
    
    if st.button("🧮 Calcular VR/VA"):
        with st.spinner("Calculando VR/VA para todos os colaboradores..."):
            
            data = st.session_state['processed_data']
            
            # 1. Consolida dados
            st.info("📊 Consolidando dados...")
            
            # Usa base de ativos como principal
            consolidated_df = data['ativos'].copy()
            
            # 2. Aplica regras de exclusão
            consolidated_df = apply_exclusion_rules(consolidated_df, data)
            
            # 3. Calcula VR/VA
            consolidated_df = calculate_vr_va(consolidated_df, data['sindicato'], data['dias_uteis'], data)
            
            # Salva resultado
            st.session_state['final_calculation'] = consolidated_df
            
            st.success("✅ Cálculo de VR/VA concluído!")
            
            # Mostra resumo
            st.subheader("📊 Resumo do Cálculo")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Colaboradores", len(consolidated_df))
            
            with col2:
                total_vr = consolidated_df['VALOR_VR'].sum()
                st.metric("Total VR/VA", f"R$ {total_vr:,.2f}")
            
            with col3:
                total_empresa = consolidated_df['CUSTO_EMPRESA'].sum()
                st.metric("Custo Empresa", f"R$ {total_empresa:,.2f}")
            
            with col4:
                total_funcionario = consolidated_df['DESCONTO_FUNCIONARIO'].sum()
                st.metric("Desconto Funcionário", f"R$ {total_funcionario:,.2f}")
    
    # Mostra resultados se disponível
    if 'final_calculation' in st.session_state:
        st.subheader("📋 Resultados do Cálculo")
        
        df = st.session_state['final_calculation']
        
        # Filtros
        col1, col2 = st.columns(2)
        
        with col1:
            min_vr = st.number_input("VR Mínimo", value=0.0, step=1.0)
        
        with col2:
            max_vr = st.number_input("VR Máximo", value=10000.0, step=100.0)
        
        # Aplica filtros
        filtered_df = df[(df['VALOR_VR'] >= min_vr) & (df['VALOR_VR'] <= max_vr)]
        
        st.write(f"**Resultados filtrados:** {len(filtered_df)} de {len(df)} registros")
        st.dataframe(filtered_df, use_container_width=True)

def show_final_report():
    """Mostra relatório final"""
    
    st.header("📋 Relatório Final")
    
    if 'final_calculation' not in st.session_state:
        st.warning("⚠️ Calcule o VR/VA primeiro na aba 'Calcular VR/VA'")
        return
    
    df = st.session_state['final_calculation']
    
    # Estatísticas finais
    st.subheader("📊 Estatísticas Finais")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribuição por faixa de VR
        vr_ranges = pd.cut(df['VALOR_VR'], bins=5)
        vr_distribution = vr_ranges.value_counts().sort_index()
        
        fig = px.bar(
            x=vr_distribution.index.astype(str),
            y=vr_distribution.values,
            title="Distribuição de VR/VA por Faixa",
            labels={'x': 'Faixa de VR', 'y': 'Quantidade de Colaboradores'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Resumo estatístico
        st.dataframe(df.describe(), use_container_width=True)
    
    # Download do relatório
    st.subheader("💾 Download do Relatório")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Download Excel"):
            output_file = f"Relatorio_VR_VA_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='VR_VA_Calculado', index=False)
                
                # Aba de resumo
                summary_data = {
                    'Métrica': ['Total Colaboradores', 'Total VR/VA', 'Custo Empresa', 'Desconto Funcionário'],
                    'Valor': [
                        len(df),
                        f"R$ {df['VALOR_VR'].sum():,.2f}",
                        f"R$ {df['CUSTO_EMPRESA'].sum():,.2f}",
                        f"R$ {df['DESCONTO_FUNCIONARIO'].sum():,.2f}"
                    ]
                }
                
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Resumo', index=False)
            
            # Download
            with open(output_file, "rb") as file:
                st.download_button(
                    label="Clique para baixar Excel",
                    data=file.read(),
                    file_name=output_file,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            # Remove arquivo temporário
            os.remove(output_file)
    
    with col2:
        if st.button("📥 Download CSV"):
            csv_data = df.to_csv(index=False)
            st.download_button(
                label="Clique para baixar CSV",
                data=csv_data,
                file_name=f"Relatorio_VR_VA_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

def show_ai_analysis():
    """Mostra análise com IA"""
    
    st.header("🤖 Análise com IA - Modelo Gemma3")
    
    if 'final_calculation' not in st.session_state:
        st.warning("⚠️ Calcule o VR/VA primeiro para usar a análise com IA")
        return
    
    df = st.session_state['final_calculation']
    
    # Contexto dos dados para IA
    data_context = f"""
    Análise de VR/VA para {len(df)} colaboradores:
    - Total VR/VA: R$ {df['VALOR_VR'].sum():,.2f}
    - Custo empresa: R$ {df['CUSTO_EMPRESA'].sum():,.2f}
    - Desconto funcionário: R$ {df['DESCONTO_FUNCIONARIO'].sum():,.2f}
    - Média de dias úteis: {df['DIAS_UTEIS'].mean():.1f}
    - Distribuição de VR: Min R$ {df['VALOR_VR'].min():.2f}, Max R$ {df['VALOR_VR'].max():.2f}
    """
    
    # Campo para perguntas
    user_question = st.text_area(
        "Faça uma pergunta sobre os dados de VR/VA:",
        placeholder="Ex: Quais são os principais insights sobre a distribuição de VR/VA?",
        height=100
    )
    
    if st.button("🔍 Analisar com IA"):
        if user_question:
            with st.spinner("Consultando o modelo Gemma3..."):
                ai_response = query_gemma3(user_question, data_context)
                
                st.subheader("💡 Resposta da IA:")
                st.write(ai_response)
        else:
            st.warning("Por favor, digite uma pergunta para analisar.")
    
    # Perguntas sugeridas
    st.subheader("💭 Perguntas Sugeridas")
    
    suggested_questions = [
        "Quais são os principais insights sobre a distribuição de VR/VA?",
        "Existe algum padrão nos valores de VR/VA por colaborador?",
        "Como otimizar o processo de cálculo de VR/VA?",
        "Quais validações adicionais seriam úteis?",
        "Como melhorar a precisão dos cálculos?"
    ]
    
    for i, question in enumerate(suggested_questions):
        if st.button(f"❓ {question}", key=f"ai_q{i}"):
            with st.spinner("Consultando o modelo Gemma3..."):
                ai_response = query_gemma3(question, data_context)
                
                st.subheader("💡 Resposta da IA:")
                st.write(ai_response)

def show_settings():
    """Mostra configurações"""
    
    st.header("⚙️ Configurações")
    
    # Verificação de status do Ollama
    st.subheader("🔍 Status do Ollama")
    
    if st.button("🔍 Verificar Status Ollama"):
        try:
            client = ollama.Client()
            models = client.list()
            st.success("✅ Ollama está funcionando!")
            
            st.write("**Modelos disponíveis:**")
            for model in models['models']:
                st.write(f"- {model['name']}")
                
        except Exception as e:
            st.error(f"❌ Erro ao conectar com Ollama: {str(e)}")
            st.info("Certifique-se de que o Ollama está rodando e o modelo Gemma3 está instalado.")
    
    # Configurações de cálculo
    st.subheader("🧮 Configurações de Cálculo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.number_input("Percentual Empresa (%)", value=80, min_value=0, max_value=100, step=5)
        st.number_input("Dias Úteis Padrão", value=22, min_value=1, max_value=31, step=1)
    
    with col2:
        st.number_input("Percentual Funcionário (%)", value=20, min_value=0, max_value=100, step=5)
        st.date_input("Data de Referência", value=datetime.now())
    
    # Instruções
    st.subheader("📋 Instruções de Uso")
    
    with st.expander("ℹ️ Como usar esta aplicação"):
        st.markdown("""
        ### 📋 Fluxo de Trabalho:
        
        1. **Processar Dados**: Carregue e consolide todas as bases
        2. **Calcular VR/VA**: Execute os cálculos automáticos
        3. **Relatório Final**: Visualize e exporte os resultados
        4. **Análise com IA**: Use IA para insights adicionais
        
        ### 🔧 Requisitos:
        - Ollama rodando localmente
        - Modelo Gemma3 instalado
        - Todas as bases Excel disponíveis
        
        ### 💡 Dicas:
        - Verifique o status do Ollama antes de usar IA
        - Processe os dados antes de calcular VR/VA
        - Use filtros para analisar resultados específicos
        """)

# Executa aplicação
if __name__ == "__main__":
    main()
