# 🤖 MT5 Report Automation: Inteligência de Dados para Trading

Este projeto automatiza a coleta, tratamento e geração de relatórios de performance de robôs de trading operando via **MetaTrader 5 (MT5)**. A solução utiliza Python para integração direta com o terminal e as bibliotecas Pandas e Matplotlib para transformar dados brutos em relatórios estatísticos estruturados (JSON) e análises visuais de performance (Curva de Capital).

---

### 🚀 Status do Projeto: Fase 4 (Integração de Pipeline ETL & Orquestração)

O motor estatístico e quantitativo (`analises.py`) está **100% refatorado sob os pilares da Programação Orientada a Objetos (POO)** e pronto para produção. O sistema possui tratamento defensivo de erros matemáticos, sanitização estrita de dados operacionais e serialização JSON customizada.

> 🎯 **Foco Atual:** Integração ponta a ponta do pipeline ETL em `main.py`, conectando a extração do MT5 diretamente ao motor sanitizador e gerador de métricas.

---

### 🧠 Diferencial Estratégico: Abordagem "Documentation-First" & Engenharia de Software

Este projeto prioriza a consulta rigorosa à **documentação oficial do MetaTrader 5 para Python** e a aplicação de padrões de projeto robustos:
- **Arquitetura Baseada em POO:** Separação estrita de responsabilidades (`ConectorMT5`, `ExtratorRelatorioSemanal`, `SanitizadorDados`, `AnalisesTecnicas`, `VisualizadorPerformance`).
- **Padrão Strategy & Abstração (SOLID):** Implementação de **Classes Abstratas (ABC)** para conversores de dados (`ConversorDataframe`), permitindo exportações extensíveis (CSV, JSON, Banco de Dados).
- **Tratamento Estatístico Defensivo:** Prevenção de divisões por zero (`ZeroDivisionError`), imunização contra valores `inf`/`nan` no Fator de Lucro e ancoragem em zero ($0.0$) para o cálculo real de *Max Drawdown*.
- **Gestão via Configurações:** Desacoplamento total de caminhos e dados operacionais via arquivos `JSON`.

---

### 🛠️ Funcionalidades Concluídas

- [x] **Suporte Multi-terminal:** Processamento em lote de diferentes contas e terminais através de loop dinâmico.
- [x] **Conexão Resiliente via Context Manager:** Classe `ConectorMT5` utilizando a sintaxe `with` (`__enter__` / `__exit__`) para abertura e fechamento seguro de conexões.
- [x] **Sanitização e Higienização de Dados:**
  - Filtro estrito de ordens executadas (`type < 2` e `entry == 1`).
  - Remoção de duplicados por `ticket` e eliminação de valores nulos.
  - Ordenação cronológica garantida (`.sort_values(by='time')`) e limpeza de espaços em branco nos ativos (`symbol.str.strip()`).
  - Cálculo de Resultado Líquido incorporando Custos Operacionais (`profit` + `commission` + `swap` + `fee`).
- [x] **Motor de Métricas Quantitativas (`analises.py`):**
  - Lucro Líquido Total, Taxa de Acerto (*Win Rate* %) e Fator de Lucro (*Profit Factor*).
  - Payoff Ratio com tratamento para históricos 100% vencedores ou 100% perdedores.
  - Maior Lucro Individual e Maior Prejuízo Individual.
  - *Max Drawdown* acumulado financeiro com vetor ancorado em zero.
  - Agrupamento de métricas por Ativo (`calcular_por_ativo()`).
  - Desempenho temporal agrupado por Dia da Semana (`desempenho_por_dia()`).
- [x] **Serialização Avançada:** Classe `EncoderTradingJSON` para conversão nativa de tipos do `numpy` (int64, float64) e `pandas.Timestamp` em JSON legível.
- [x] **Visualização Gráfica:** Classe `VisualizadorPerformance` para plotagem da Curva de Capital Acumulada via `Matplotlib`.

---

### 💻 Stack Técnica

| Tecnologia | Aplicação |
| :--- | :--- |
| **Python 3.10+** | Núcleo do processamento e arquitetura POO |
| **MetaTrader5 API** | Interface de comunicação e extração de dados financeiros |
| **Pandas** | Sanitização, agrupamento temporal e cálculo de métricas quantitativas |
| **NumPy** | Operações vetoriais e normalização de tipos numéricos |
| **Matplotlib** | Plotagem gráfica da Curva de Capital Acumulada (*Equity Curve*) |
| **JSON / ABC** | Serialização de relatórios, abstração de contratos e configurações |

---

### ⚙️ Como Executar o Projeto

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/MuriloSilva110/mt5-report-automation.git](https://github.com/MuriloSilva110/mt5-report-automation.git)
   cd mt5-report-automation

1 - Prepare o Ambiente Virtual:
  python -m venv .venv
  # No Windows (PowerShell):
  .\.venv\Scripts\Activate.ps1
  # Instale as dependências:
  pip install -r requirements.txt

2 - Configure os Terminais:
Crie o arquivo config/config.json a partir do modelo config/config_example.json:
  {
  "terminais": {
    "Conta_Pessoal": "C:/Caminho/Para/terminal64.exe",
    "Conta_Prop": "C:/Caminho/Para/Outro/terminal64.exe"
  }
}

3 -  Executar a Extração e Geração de Relatórios:
  python main.py

4 - Executar Testes de Análise Individual (Motor de Métricas):
  python analises.py


🛣️ Roadmap de Desenvolvimento
[x] Módulo de Extração: Coleta automatizada do histórico de ordens do MT5.

[x] Data Cleaning & Sanitização: Filtros de segurança, tratamento de datas e cálculo de resultado líquido com custos.

[x] Módulo de Análise em POO (analises.py): Motor completo de métricas estatísticas, agrupamentos e exportador JSON customizado.

[ ] ⏳ Fase 4: Orquestração do Pipeline ETL (main.py):

[ ] Ajuste no truncamento da janela de datas do ExtratorRelatorioSemanal (meia-noite exata).

[ ] Conexão direta entre main.py e o motor analises.py para gerar relatórios JSON automáticos ao final do loop.

[ ] ⏳ Módulo de Notificação: Envio automatizado de resumos de performance via Telegram Bot.

[ ] ⏳ Dashboard Integrado: Painel consolidado para acompanhamento de múltiplos robôs em tempo real.

👨‍💻 Sobre o Desenvolvedor
Projeto desenvolvido por Murilo Silva, aplicando os fundamentos de Análise e Desenvolvimento de Sistemas (ADS) da Unisa para criar arquiteturas de software robustas que unificam engenharia de dados e mercado financeiro.