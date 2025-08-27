
# 🤖 Automação da Compra de VR/VA com IA - Modelo Gemma3

Esta aplicação automatiza completamente o processo mensal de compra de VR (Vale Refeição) e VA (Vale Alimentação), utilizando o modelo **Gemma3** do Ollama para análise inteligente e otimização dos processos.

## 🎯 Objetivo

Automatizar o processo mensal de compra de VR/VA, garantindo que cada colaborador receba o valor correto, considerando:
- ✅ Ausências e férias
- ✅ Datas de admissão ou desligamento
- ✅ Calendário de feriados
- ✅ Regras sindicais específicas
- ✅ Cálculo proporcional para datas quebradas

## 🚀 Funcionalidades Implementadas

### 📊 Processamento Automático de Dados
- **Consolidação automática** de 10 bases de dados separadas
- **Validação automática** de dados inconsistentes
- **Tratamento de exclusões** (diretores, estagiários, aprendizes, afastados, exterior)
- **Detecção automática** de nomes de colunas
- **Conversão automática** de tipos de dados

### 🧮 Cálculo Inteligente de VR/VA
- **Cálculo automático** de dias úteis por colaborador
- **Mapeamento inteligente** de sindicatos por estado e palavras-chave
- **Aplicação automática** de regras sindicais
- **Cálculo proporcional** para admissões/desligamentos
- **Validação de regras** de desligamento (antes/depois do dia 15)

### 📋 Relatórios e Exportação
- **Relatório consolidado** para envio à operadora
- **Cálculo automático** de custos (80% empresa, 20% funcionário)
- **Exportação** em Excel e CSV
- **Validações automáticas** conforme regras estabelecidas
- **Debug detalhado** para identificação de problemas

### 🤖 Análise com IA
- **Insights inteligentes** sobre os dados
- **Otimizações de processo** sugeridas pela IA
- **Análise de padrões** e tendências
- **Recomendações** para melhorias

## 📋 Bases de Dados Integradas

| Base | Descrição | Função | Status |
|------|-----------|---------|---------|
| `ATIVOS.xlsx` | Funcionários ativos | Base principal de colaboradores | ✅ Funcionando |
| `FÉRIAS.xlsx` | Dados de férias | Exclusão de períodos de férias | ✅ Funcionando |
| `DESLIGADOS.xlsx` | Funcionários desligados | Cálculo proporcional | ✅ Funcionando |
| `ADMISSÃO ABRIL.xlsx` | Novas admissões | Cálculo proporcional | ✅ Funcionando |
| `Base sindicato x valor.xlsx` | Valores por sindicato | Cálculo de VR/VA | ✅ Funcionando |
| `Base dias uteis.xlsx` | Dias úteis por colaborador | Cálculo de dias | ✅ Funcionando |
| `AFASTAMENTOS.xlsx` | Funcionários afastados | Exclusão automática | ✅ Funcionando |
| `EXTERIOR.xlsx` | Funcionários no exterior | Exclusão automática | ✅ Funcionando |
| `ESTÁGIO.xlsx` | Estagiários | Exclusão automática | ✅ Funcionando |
| `APRENDIZ.xlsx` | Aprendizes | Exclusão automática | ✅ Funcionando |

## 🛠️ Instalação

### 1. Pré-requisitos

- Python 3.8 ou superior
- Ollama instalado e rodando
- Modelo Gemma3 baixado

### 2. Instalar Ollama

```bash
# Windows (usando winget)
winget install Ollama.Ollama

# Ou baixe de: https://ollama.ai/download
```

### 3. Baixar o modelo Gemma3

```bash
ollama pull gemma3
```

### 4. Instalar dependências Python

```bash
pip install -r requiremts.txt
```

## 🚀 Como Executar

### 1. Iniciar o Ollama

```bash
ollama serve
```

### 2. Executar a aplicação

```bash
streamlit run app.py
```

### 3. Acessar no navegador

A aplicação estará disponível em: `http://localhost:8501`

## 📖 Fluxo de Trabalho

### 1. 🏠 Visão Geral
- Visão geral da aplicação
- Status dos arquivos
- Estatísticas das bases
- Verificação de integridade dos dados

### 2. 📊 Processar Dados
- Carregamento automático de todas as bases
- Consolidação e validação
- Aplicação de regras de exclusão
- Detalhes das colunas por base

### 3. 🧮 Calcular VR/VA
- Cálculo automático de dias úteis
- Mapeamento inteligente de sindicatos
- Aplicação de regras sindicais
- Cálculo de valores e custos
- Debug detalhado do processo

### 4. 📋 Relatório Final
- Visualização dos resultados
- Gráficos e estatísticas
- Exportação para Excel/CSV
- Métricas de resumo

### 5. 🤖 Análise com IA
- Consultas inteligentes sobre os dados
- Insights e otimizações
- Perguntas sugeridas
- Análise de padrões

### 6. ⚙️ Configurações
- Status do Ollama
- Configurações de cálculo
- Instruções de uso
- Verificação de dependências

## 🔧 Regras de Negócio Implementadas

### 📅 Cálculo de Dias Úteis
- Exclusão automática de finais de semana
- Consideração de feriados estaduais e municipais
- Cálculo proporcional para datas quebradas
- Valor padrão de 22 dias quando base corrompida

### 💰 Cálculo de VR/VA
- **80%** custo da empresa
- **20%** desconto do funcionário
- Valores específicos por sindicato
- Ajuste proporcional por dias úteis

### 🚫 Regras de Exclusão
- **Diretores**: Exclusão automática
- **Estagiários**: Exclusão automática
- **Aprendizes**: Exclusão automática
- **Afastados**: Exclusão automática
- **Exterior**: Exclusão automática

### 📊 Regras de Desligamento
- **Antes do dia 15**: Não considerar para pagamento
- **Depois do dia 15**: Cálculo proporcional
- Validação de elegibilidade por matrícula

## 🔍 Mapeamento Inteligente de Sindicatos

### 🎯 Estratégias de Mapeamento
1. **Mapeamento Direto**: Busca exata no dicionário
2. **Mapeamento por Palavras-chave**: SINDPPD RS → R$ 35.00
3. **Mapeamento por Estado**: SP → R$ 37.50, RS → R$ 35.00

### 📊 Valores por Estado
- **São Paulo (SP)**: R$ 37.50
- **Rio Grande do Sul (RS)**: R$ 35.00
- **Rio de Janeiro (RJ)**: R$ 35.00
- **Paraná (PR)**: R$ 35.00

## 💡 Exemplos de Análise com IA

- "Quais são os principais insights sobre a distribuição de VR/VA?"
- "Existe algum padrão nos valores de VR/VA por colaborador?"
- "Como otimizar o processo de cálculo de VR/VA?"
- "Quais validações adicionais seriam úteis?"
- "Como melhorar a precisão dos cálculos?"
- "Quais são as possíveis inconsistências nos dados?"
- "Como aplicar melhor as regras sindicais?"
- "Quais otimizações de processo você recomendaria?"

## 🐛 Solução de Problemas

### Erro de Conexão com Ollama
```bash
# Verificar se o Ollama está rodando
ollama list

# Reiniciar o serviço
ollama serve
```

### Modelo não encontrado
```bash
# Baixar o modelo novamente
ollama pull gemma3

# Verificar modelos disponíveis
ollama list
```

### Dependências Python
```bash
# Atualizar pip
python -m pip install --upgrade pip

# Reinstalar dependências
pip install -r requiremts.txt --force-reinstall
```

### Problemas de Leitura de Excel
```bash
# Verificar se openpyxl está instalado
pip install openpyxl==3.1.2

# Verificar se pandas está atualizado
pip install pandas==2.1.4
```

## 🔧 Problemas Resolvidos

### ✅ **Detecção Automática de Colunas**
- Identifica automaticamente colunas de matrícula, valor VR e dias úteis
- Funciona independente dos nomes exatos das colunas
- Suporte a múltiplos formatos de dados

### ✅ **Conversão Automática de Tipos**
- Converte strings para números automaticamente
- Remove caracteres especiais (R$, espaços, vírgulas)
- Trata valores nulos e inválidos graciosamente

### ✅ **Mapeamento Inteligente de Sindicatos**
- Sistema de fallback para nomes diferentes
- Mapeamento por estado e palavras-chave
- Identifica automaticamente padrões nos nomes

### ✅ **Tratamento de Bases Corrompidas**
- Usa valores padrão quando bases estão corrompidas
- Detecta automaticamente problemas de dados
- Continua funcionando mesmo com dados inconsistentes

## 📊 Estrutura da Aplicação

```
app.py              # Aplicação principal de automação VR/VA
config.py           # Configurações personalizáveis
requiremts.txt      # Dependências Python
setup.bat           # Script de instalação Windows
setup.ps1           # Script PowerShell avançado
README.md           # Este arquivo
*.xlsx              # Bases de dados Excel
```

## 🔮 Funcionalidades Futuras

- [ ] Integração com sistemas de RH
- [ ] Validação automática de folha ponto
- [ ] Relatórios em PDF automáticos
- [ ] Dashboard executivo
- [ ] Alertas de inconsistências
- [ ] Integração com fornecedores
- [ ] Machine Learning para previsões
- [ ] API REST para integrações
- [ ] Validação de dados em tempo real
- [ ] Sistema de auditoria e logs

## 🤝 Contribuição

Para contribuir com o projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 📞 Suporte

Para suporte ou dúvidas:
- Abra uma issue no repositório
- Consulte a documentação do Ollama: https://ollama.ai/docs
- Consulte a documentação do Streamlit: https://docs.streamlit.io

## 🎊 Status do Projeto

### ✅ **Implementado e Funcionando:**
- Automação completa do processo VR/VA
- Processamento de todas as 10 bases de dados
- Cálculo automático com regras de negócio
- Mapeamento inteligente de sindicatos
- Sistema de exclusões automáticas
- Relatórios e exportação
- Análise com IA usando Gemma3
- Interface web responsiva
- Debug e validação de dados

### 🔄 **Em Desenvolvimento:**
- Melhorias de performance
- Validações adicionais
- Testes automatizados




