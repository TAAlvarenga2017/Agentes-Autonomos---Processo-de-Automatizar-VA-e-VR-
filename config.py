# ========================================
#    CONFIGURAÇÃO DA APLICAÇÃO VR/VA
# ========================================

# Configurações de cálculo
CALCULATION_CONFIG = {
    # Percentuais de custo
    'EMPRESA_PERCENTAGE': 80,  # 80% custo empresa
    'FUNCIONARIO_PERCENTAGE': 20,  # 20% desconto funcionário
    
    # Dias úteis padrão
    'DEFAULT_WORKING_DAYS': 22,
    
    # Regras de desligamento
    'DESLIGAMENTO_CUTOFF_DAY': 15,  # Dia limite para considerar desligamento
    
    # Configurações de férias
    'FERIAS_EXCLUSION': True,  # Excluir períodos de férias
    
    # Configurações de afastamento
    'AFASTAMENTO_EXCLUSION': True,  # Excluir afastamentos
}

# Configurações de exclusão
EXCLUSION_CONFIG = {
    # Cargos para exclusão automática
    'EXCLUDED_CARGOS': [
        'DIRETOR',
        'DIRETORA',
        'PRESIDENTE',
        'VICE-PRESIDENTE',
        'CEO',
        'CFO',
        'CTO'
    ],
    
    # Tipos de funcionário para exclusão
    'EXCLUDED_TYPES': [
        'ESTAGIARIO',
        'ESTAGIARIA',
        'APRENDIZ',
        'APRENDIZA'
    ],
    
    # Status para exclusão
    'EXCLUDED_STATUS': [
        'AFASTADO',
        'LICENCA',
        'MATERNIDADE',
        'PATERNIDADE',
        'EXTERIOR'
    ]
}

# Configurações de validação
VALIDATION_CONFIG = {
    # Campos obrigatórios
    'REQUIRED_FIELDS': [
        'MATRÍCULA',
        'NOME',
        'CARGO',
        'SINDICATO'
    ],
    
    # Validações de data
    'DATE_VALIDATION': {
        'MIN_DATE': '2020-01-01',
        'MAX_DATE': '2030-12-31',
        'CHECK_FUTURE_DATES': True
    },
    
    # Validações de valor
    'VALUE_VALIDATION': {
        'MIN_VR_VALUE': 0.0,
        'MAX_VR_VALUE': 10000.0,
        'MIN_DAYS': 1,
        'MAX_DAYS': 31
    }
}

# Configurações de relatório
REPORT_CONFIG = {
    # Formato de data
    'DATE_FORMAT': '%d/%m/%Y',
    
    # Formato de moeda
    'CURRENCY_FORMAT': 'R$ {:.2f}',
    
    # Colunas do relatório final
    'FINAL_REPORT_COLUMNS': [
        'MATRICULA',
        'NOME',
        'CARGO',
        'SINDICATO',
        'DIAS_UTEIS',
        'VALOR_VR',
        'CUSTO_EMPRESA',
        'DESCONTO_FUNCIONARIO',
        'ADMISSAO',
        'COMPETENCIA',
        'OBS_GERAL'
    ],
    
    # Abas do Excel
    'EXCEL_SHEETS': [
        'VR_VA_Calculado',
        'Resumo',
        'Validações',
        'Exclusões'
    ]
}

# Configurações de IA
AI_CONFIG = {
    # Modelo Ollama
    'OLLAMA_MODEL': 'gemma3',
    
    # Configurações de prompt
    'PROMPT_TEMPLATE': """
    Você é um especialista em recursos humanos e benefícios corporativos.
    Analise os seguintes dados relacionados ao cálculo de VR/VA e responda à pergunta.
    
    Contexto dos dados:
    {data_context}
    
    Pergunta: {user_question}
    
    Responda de forma clara e objetiva em português, fornecendo insights práticos 
    sobre o cálculo de benefícios, regras trabalhistas e otimizações de processo.
    """,
    
    # Perguntas sugeridas
    'SUGGESTED_QUESTIONS': [
        "Quais são os principais insights sobre a distribuição de VR/VA?",
        "Existe algum padrão nos valores de VR/VA por colaborador?",
        "Como otimizar o processo de cálculo de VR/VA?",
        "Quais validações adicionais seriam úteis?",
        "Como melhorar a precisão dos cálculos?",
        "Quais são as possíveis inconsistências nos dados?",
        "Como aplicar melhor as regras sindicais?",
        "Quais otimizações de processo você recomendaria?"
    ]
}

# Configurações de interface
UI_CONFIG = {
    # Título da aplicação
    'APP_TITLE': '🤖 Automação da Compra de VR/VA com IA',
    
    # Ícone da página
    'PAGE_ICON': '🍽️',
    
    # Layout
    'LAYOUT': 'wide',
    
    # Cores do tema
    'THEME_COLORS': {
        'primary': '#FF6B6B',
        'secondary': '#4ECDC4',
        'success': '#45B7D1',
        'warning': '#FFA07A',
        'error': '#FF6B6B'
    }
}

# Configurações de arquivos
FILE_CONFIG = {
    # Arquivos de entrada
    'INPUT_FILES': [
        'ATIVOS.xlsx',
        'FÉRIAS.xlsx',
        'DESLIGADOS.xlsx',
        'ADMISSÃO ABRIL.xlsx',
        'Base sindicato x valor.xlsx',
        'Base dias uteis.xlsx',
        'AFASTAMENTOS.xlsx',
        'EXTERIOR.xlsx',
        'ESTÁGIO.xlsx',
        'APRENDIZ.xlsx'
    ],
    
    # Extensões suportadas
    'SUPPORTED_EXTENSIONS': ['.xlsx', '.xls'],
    
    # Encoding padrão
    'DEFAULT_ENCODING': 'utf-8'
}

# Configurações de logging
LOGGING_CONFIG = {
    # Nível de log
    'LOG_LEVEL': 'INFO',
    
    # Formato do log
    'LOG_FORMAT': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    
    # Arquivo de log
    'LOG_FILE': 'vr_va_automation.log'
}

# Configurações de performance
PERFORMANCE_CONFIG = {
    # Cache de dados
    'ENABLE_CACHE': True,
    
    # Tamanho máximo do cache
    'MAX_CACHE_SIZE': 1000,
    
    # Timeout para operações
    'DEFAULT_TIMEOUT': 30,
    
    # Processamento em lotes
    'BATCH_SIZE': 100
}

# Função para obter configuração
def get_config(section, key=None):
    """Obtém configuração específica ou toda a seção"""
    config_sections = {
        'calculation': CALCULATION_CONFIG,
        'exclusion': EXCLUSION_CONFIG,
        'validation': VALIDATION_CONFIG,
        'report': REPORT_CONFIG,
        'ai': AI_CONFIG,
        'ui': UI_CONFIG,
        'file': FILE_CONFIG,
        'logging': LOGGING_CONFIG,
        'performance': PERFORMANCE_CONFIG
    }
    
    if section not in config_sections:
        raise ValueError(f"Seção '{section}' não encontrada")
    
    if key is None:
        return config_sections[section]
    
    if key not in config_sections[section]:
        raise ValueError(f"Chave '{key}' não encontrada na seção '{section}'")
    
    return config_sections[section][key]

# Função para validar configuração
def validate_config():
    """Valida se todas as configurações estão corretas"""
    errors = []
    
    # Valida percentuais
    emp_percent = get_config('calculation', 'EMPRESA_PERCENTAGE')
    func_percent = get_config('calculation', 'FUNCIONARIO_PERCENTAGE')
    
    if emp_percent + func_percent != 100:
        errors.append(f"Percentuais devem somar 100% (atual: {emp_percent}% + {func_percent}%)")
    
    # Valida dias
    min_days = get_config('validation', 'VALUE_VALIDATION')['MIN_DAYS']
    max_days = get_config('validation', 'VALUE_VALIDATION')['MAX_DAYS']
    
    if min_days >= max_days:
        errors.append(f"MIN_DAYS deve ser menor que MAX_DAYS (atual: {min_days} >= {max_days})")
    
    # Valida arquivos
    required_files = get_config('file', 'INPUT_FILES')
    for file in required_files:
        if not file.endswith(('.xlsx', '.xls')):
            errors.append(f"Arquivo deve ter extensão .xlsx ou .xls: {file}")
    
    if errors:
        raise ValueError(f"Configuração inválida:\n" + "\n".join(errors))
    
    return True

# Executa validação ao importar
if __name__ == "__main__":
    try:
        validate_config()
        print("✅ Configuração válida!")
    except ValueError as e:
        print(f"❌ {e}")
else:
    # Validação silenciosa ao importar
    try:
        validate_config()
    except ValueError:
        pass  # Ignora erros de validação ao importar 