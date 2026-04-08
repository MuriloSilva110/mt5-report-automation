# 🤖 MT5 Report Automation: Inteligência de Dados para Trading

Este projeto automatiza a coleta, tratamento e geração de relatórios de performance de robôs de trading operando via **MetaTrader 5 (MT5)**. A solução utiliza Python para integração direta com o terminal e a biblioteca Pandas para transformar dados brutos em relatórios estruturados e prontos para análise.

### 🚀 Status do Projeto: Fase 2 (Extração e Processamento de Dados)
O projeto evoluiu da simples conexão para um fluxo funcional de dados. Atualmente, o sistema é capaz de calcular períodos dinâmicos, extrair o histórico de ordens, tratar inconsistências e exportar relatórios formatados automaticamente.

---

### 🧠 Diferencial Estratégico: Abordagem "Documentation-First"
Este projeto prioriza a consulta rigorosa à **documentação oficial do MetaTrader 5 para Python**, resultando em:
* **Lógica de Datas Dinâmica:** Cálculo automático do período semanal (domingo até a data atual) utilizando `datetime` e `timedelta`.
* **Tratamento de Exceções Avançado:** Diferenciação entre falhas de conexão (retorno `None`) e ausência de operações no período (lista vazia), evitando erros de execução.
* **Persistência Inteligente:** Uso da biblioteca `pathlib` para gestão de diretórios e exportação de CSV com encoding `utf-8-sig`, garantindo compatibilidade imediata com o Excel.

---

### 🛠️ Funcionalidades Atuais
- [x] Verificação de versão e integridade da biblioteca MT5.
- [x] Conexão resiliente com lógica de até 3 tentativas de reconexão.
- [x] **Extração Semanal Automática:** Captura de histórico de ordens sem necessidade de input manual de datas.
- [x] **Data Transformation:** Conversão de objetos complexos do MT5 em DataFrames do Pandas para análise.
- [x] **Sistema de Arquivos:** Criação automática de diretórios e geração de arquivos CSV nomeados por data.

### 💻 Stack Técnica
| Tecnologia | Aplicação |
| :--- | :--- |
| **Python 3.10+** | Núcleo do processamento e automação |
| **MetaTrader5 API** | Interface de comunicação e extração de dados |
| **Pandas** | Estruturação, limpeza e análise de dados financeiros |
| **Pathlib/Datetime** | Manipulação de arquivos e lógica temporal dinâmica |
| **Git/GitHub** | Controle de versão e documentação técnica |

---

### ⚙️ Como Executar o Projeto

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/MuriloSilva110/mt5-report-automation.git](https://github.com/MuriloSilva110/mt5-report-automation.git)

   Aqui estão os passos finais para completar a seção **"Como Executar o Projeto"** do seu README, já formatados em Markdown para você copiar e colar:

---

2. **Crie e ative seu ambiente virtual:**
   ```bash
   python -m venv .venv
   # No Windows:
   .venv\Scripts\activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a automação:**
   ```bash
   python main.py
   ```
   *O script verificará a conexão, extrairá os dados da semana e salvará o arquivo na pasta `/relatorios`.*
---

### 🛣️ Roadmap de Desenvolvimento

- [x] **Módulo de Extração:** Coleta automatizada do histórico de ordens por períodos específicos.
- [x] **Data Cleaning:** Tratamento de dados brutos com Pandas e conversão de timestamps (Unix para Datetime).
- [ ] **Análise de Performance:** Implementação de métricas avançadas como Drawdown, Fator de Lucro e Recovery Factor.
- [ ] **Refatoração para POO:** Encapsulamento da lógica em classes para aumentar a escalabilidade e permitir a gestão de múltiplas contas simultâneas.
- [ ] **Interface Visual:** Desenvolvimento de um Dashboard simples ou exportação para PDF formatado para melhor apresentação dos resultados.

---
