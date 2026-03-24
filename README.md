# 🤖 MT5 Report Automation: Inteligência de Dados para Trading

Este projeto automatiza a coleta, tratamento e geração de relatórios de performance de robôs de trading operando via **MetaTrader 5 (MT5)**. A solução utiliza Python para integração direta com o terminal e a biblioteca Pandas para transformar dados brutos em relatórios estruturados para análise.

### 🚀 Status do Projeto: Fase 1 (Conexão e Resiliência)
Atualmente, o projeto foca na fundação crítica da automação: a **comunicação resiliente** com o terminal de negociação, garantindo que a extração de dados ocorra sem falhas silenciosas.

---

### 🧠 Diferencial Estratégico: Abordagem "Documentation-First"
Este projeto não foi construído com base em códigos prontos de IA. Priorizei a consulta rigorosa à **documentação oficial do MetaTrader 5 para Python**, garantindo:
* **Tratamento de Exceções:** Implementação de lógica de *retry* (tentativas) para contornar latências de inicialização.
* **Clean Code:** Código modularizado com foco em manutenibilidade e futura transição para Programação Orientada a Objetos (POO).
* **Segurança de Dados:** Configuração de `.gitignore` para proteção de credenciais e dados financeiros sensíveis.

---

### 🛠️ Funcionalidades Atuais
- [x] Verificação de versão e integridade da biblioteca MT5.
- [x] Função de conexão automatizada com suporte a caminhos customizados de executáveis (`.exe`).
- [x] Lógica de até 3 tentativas de reconexão automática em caso de falha.
- [x] Extração e log de metadados do terminal (servidor, conta e estado da conexão).

### 💻 Stack Técnica
| Tecnologia | Aplicação |
| :--- | :--- |
| **Python 3.10+** | Núcleo do processamento e lógica de automação |
| **MetaTrader5 API** | Interface de comunicação e extração de dados |
| **Pandas** | (Em implementação) Estruturação e análise de dados |
| **Git/GitHub** | Controle de versão e documentação técnica |

---

### ⚙️ Como Executar o Projeto

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/seu-usuario/nome-do-repositorio.git](https://github.com/seu-usuario/nome-do-repositorio.git)