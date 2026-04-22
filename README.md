# 🤖 MT5 Report Automation: Inteligência de Dados para Trading

Este projeto automatiza a coleta, tratamento e geração de relatórios de performance de robôs de trading operando via **MetaTrader 5 (MT5)**. A solução utiliza Python para integração direta com o terminal e a biblioteca Pandas para transformar dados brutos em relatórios estruturados e prontos para análise.

### 🚀 Status do Projeto: Fase 3 (Arquitetura e Escalabilidade)
O projeto evoluiu de um script utilitário para um sistema modular baseado em **Programação Orientada a Objetos (POO)**. Atualmente, a arquitetura suporta a gestão de **múltiplos terminais simultâneos** através de configurações externas, utilizando princípios de SOLID para garantir a manutenibilidade e escalabilidade do código.

---

### 🧠 Diferencial Estratégico: Abordagem "Documentation-First" & Engenharia de Software
Este projeto prioriza a consulta rigorosa à **documentação oficial do MetaTrader 5 para Python** e a aplicação de padrões de projeto:
* **Arquitetura Baseada em POO:** Separação clara de responsabilidades entre classes de Conexão, Extração, Formatação e Conversão.
* **Abstração (SOLID):** Implementação de **Classes Abstratas (ABC)** para conversores de dados, permitindo a fácil expansão para novos formatos (CSV, Excel, JSON, etc.) sem alterar o núcleo do sistema.
* **Gestão via Configurações:** Desacoplamento total dos dados de acesso através de arquivos `JSON` e variáveis de ambiente (`.env`), garantindo segurança e portabilidade.

---

### 🛠️ Funcionalidades Atuais
- [x] **Suporte Multi-terminal:** Processamento em lote de diferentes contas e terminais através de um loop de execução.
- [x] **Conexão Resiliente:** Classe `ConectorMT5` com lógica de tentativas e encerramento seguro de sessão.
- [x] **Configuração Externa:** Carregamento dinâmico de diretórios de terminais via `config.json`.
- [x] **Data Transformation:** Conversão de objetos complexos do MT5 em DataFrames do Pandas com tratamento de timestamps.
- [x] **Persistência Estruturada:** Criação automática de diretórios e exportação de CSVs nomeados dinamicamente por terminal e data.

### 💻 Stack Técnica
| Tecnologia | Aplicação |
| :--- | :--- |
| **Python 3.10+** | Núcleo do processamento e arquitetura POO |
| **MetaTrader5 API** | Interface de comunicação e extração de dados financeiros |
| **Pandas** | Estruturação, limpeza e análise de dados |
| **python-dotenv / JSON** | Gestão de credenciais, segurança e configurações externas |
| **ABC (Abstract Base Classes)** | Implementação de contratos e padronização de métodos |

---

### ⚙️ Como Executar o Projeto

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/MuriloSilva110/mt5-report-automation.git
    ```

2.  **Prepare o Ambiente:**
    * Crie o ambiente virtual: `python -m venv .venv`
    * Ative o ambiente (Windows): `.venv\Scripts\activate`
    * Instale as dependências: `pip install -r requirements.txt`

3.  **Configure as Variáveis de Ambiente:**
    * Crie um arquivo `.env` baseado no `.env.example`.
    * Defina os caminhos dos terminais e chaves necessárias.

4.  **Configure os Terminais:**
    * Edite o arquivo `config/config.json` adicionando o nome e o caminho dos seus terminais MetaTrader 5:
    ```json
    {
      "terminais": {
        "Conta_Pessoal": "C:/Caminho/Para/terminal64.exe",
        "Conta_Prop": "C:/Caminho/Para/Outro/terminal64.exe"
      }
    }
    ```

5.  **Execute a automação:**
    ```bash
    python main.py
    ```

---

### 🛣️ Roadmap de Desenvolvimento

- [x] **Módulo de Extração:** Coleta automatizada do histórico de ordens por períodos específicos.
- [x] **Data Cleaning:** Tratamento de dados brutos com Pandas e conversão de timestamps.
- [x] **Refatoração para POO:** Encapsulamento em classes e suporte a múltiplos terminais.
- [ ] **Análise de Performance:** Implementação de métricas como Drawdown, Fator de Lucro e Recovery Factor.
- [ ] **Módulo de Notificação:** Integração com Telegram para envio de resumos diários/semanais.
- [ ] **Interface Visual:** Dashboard para visualização consolidada de múltiplos terminais.

---

### 👨‍💻 Sobre o Desenvolvedor
Projeto desenvolvido por **Murilo Silva**, aplicando os fundamentos de Análise e Desenvolvimento de Sistemas (ADS) da **Unisa** para criar arquiteturas de software robustas que unem tecnologia e mercado financeiro.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/murilo-silva-dev/)
---