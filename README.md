# 🤖 MT5 Report Automation: Inteligência de Dados para Trading

Este projeto automatiza a coleta, tratamento e geração de relatórios de performance de robôs de trading operando via **MetaTrader 5 (MT5)**. A solução utiliza Python para integração direta com o terminal e as bibliotecas Pandas e Matplotlib para transformar dados brutos em relatórios estruturados e análises visuais de performance.

### 🚀 Status do Projeto: Fase 3 (Arquitetura, Escalabilidade e Análise de Performance)
O projeto conta com um sistema modular baseado em **Programação Orientada a Objetos (POO)** para extração automatizada, suportando a gestão de **múltiplos terminais simultâneos** através de configurações externas e princípios de SOLID.

Atualmente, foi iniciada a etapa de **Análise Quantitativa e Métricas de Performance** (`analises.py`). 

> ⚠️ **Aviso de Desenvolvimento:** A etapa de análise de performance **ainda não está concluída**. Os cálculos atuais (lucro/prejuízo bruto, resultado líquido, taxa de acerto, fator de lucro e saldo acumulado) estão em fase exploratória. As próximas metas prioritárias são a **refatoração desse módulo para Programação Orientada a Objetos (POO)** e a **criação e enriquecimento de dados visuais com Matplotlib**.

---

### 🧠 Diferencial Estratégico: Abordagem "Documentation-First" & Engenharia de Software
Este projeto prioriza a consulta rigorosa à **documentação oficial do MetaTrader 5 para Python** e a aplicação de padrões de projeto:
* **Arquitetura Baseada em POO:** Separação clara de responsabilidades entre classes de Conexão, Extração, Formatação e Conversão.
* **Abstração (SOLID):** Implementação de **Classes Abstratas (ABC)** para conversores de dados, permitindo a fácil expansão para novos formatos (CSV, Excel, JSON, etc.) sem alterar o núcleo do sistema.
* **Gestão via Configurações:** Desacoplamento total dos dados de acesso através de arquivos `JSON` e variáveis de ambiente, garantindo segurança e portabilidade.

---

### 🛠️ Funcionalidades Atuais
- [x] **Suporte Multi-terminal:** Processamento em lote de diferentes contas e terminais através de um loop de execução.
- [x] **Conexão Resiliente:** Classe `ConectorMT5` com lógica de tentativas e encerramento seguro de sessão.
- [x] **Configuração Externa:** Carregamento dinâmico de diretórios de terminais via `config.json` (com modelo em `config_example.json`).
- [x] **Data Transformation:** Conversão de objetos complexos do MT5 em DataFrames do Pandas com tratamento de timestamps.
- [x] **Persistência Estruturada:** Criação automática de diretórios e exportação de CSVs nomeados dinamicamente por terminal e data.
- [ ] ⏳ **Módulo de Análise e Métricas (Em Andamento):** Cálculos preliminares de Lucro Bruto, Prejuízo Bruto, Resultado Líquido, Taxa de Acerto (Win Rate), Fator de Lucro (*Profit Factor*) e Lucro Acumulado com `.cumsum()`.

### 💻 Stack Técnica
| Tecnologia | Aplicação |
| :--- | :--- |
| **Python 3.10+** | Núcleo do processamento e arquitetura POO |
| **MetaTrader5 API** | Interface de comunicação e extração de dados financeiros |
| **Pandas** | Estruturação, limpeza, tratamento e cálculo de métricas quantitativas |
| **Matplotlib** | Visualização de dados e plotagem gráfica da Curva de Capital (*Equity Curve*) |
| **python-dotenv / JSON** | Gestão de credenciais, segurança e configurações externas |
| **ABC (Abstract Base Classes)** | Implementação de contratos e padronização de métodos |

---

### ⚙️ Como Executar o Projeto

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/MuriloSilva110/mt5-report-automation.git
    cd mt5-report-automation
    ```

2.  **Prepare o Ambiente:**
    * Crie o ambiente virtual: `python -m venv .venv`
    * Ative o ambiente (Windows): `.venv\Scripts\activate`
    * Instale as dependências: `pip install -r requirements.txt`

3.  **Configure os Terminais:**
    * Crie o arquivo `config/config.json` a partir do `config/config_example.json`:
    ```json
    {
      "terminais": {
        "Conta_Pessoal": "C:/Caminho/Para/terminal64.exe",
        "Conta_Prop": "C:/Caminho/Para/Outro/terminal64.exe"
      }
    }
    ```

4.  **Execute a extração dos relatórios:**
    ```bash
    python main.py
    ```

5.  **Executar análises (Protótipo em desenvolvimento):**
    ```bash
    python analises.py
    ```

---

### 🛣️ Roadmap de Desenvolvimento

- [x] **Módulo de Extração:** Coleta automatizada do histórico de ordens por períodos específicos.
- [x] **Data Cleaning:** Tratamento de dados brutos com Pandas e conversão de timestamps.
- [x] **Refatoração para POO (Extração e Conexão):** Encapsulamento em classes e suporte a múltiplos terminais.
- [ ] ⏳ **Módulo de Análise de Performance (Não Concluído - Em Andamento):**
  - [x] Cálculos preliminares de Lucro/Prejuízo Bruto, Taxa de Acerto, Fator de Lucro e Saldo Acumulado (`analises.py`).
  - [ ] 🎯 **Próxima Meta (POO):** Migrar a estrutura procedural do script `analises.py` para **Programação Orientada a Objetos**, criando classes especializadas para cálculo de métricas e relatórios estatísticos.
  - [ ] 🎯 **Próxima Meta (Visualização de Dados):** Criação e aprimoramento de dados visuais com **Matplotlib** (Curva de Capital / *Equity Curve*, Drawdown subaquático e distribuição de retornos).
- [ ] **Módulo de Notificação:** Integração com Telegram para envio automatizado de resumos diários/semanais.
- [ ] **Interface Visual / Dashboard:** Dashboard para visualização consolidada de múltiplos robôs e contas.

---

### 👨‍💻 Sobre o Desenvolvedor
Projeto desenvolvido por **Murilo Silva**, aplicando os fundamentos de Análise e Desenvolvimento de Sistemas (ADS) da **Unisa** para criar arquiteturas de software robustas que unem tecnologia e mercado financeiro.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/murilo-silva-dev/)
---