'''
projeto de automação de relatórios de performance de robôs de trading, utilizando a biblioteca MT5 para coletar 
os dados e a biblioteca pandas para organizar e gerar os relatórios.
'''
# Importando as bibliotecas necessárias
import MetaTrader5 as mt5
from time import sleep
from datetime import datetime, timedelta
import pandas as pd
from pathlib import Path
from abc import ABC, abstractmethod
import json
# Importação dos módulos de sanitização, análise e serialização do analises.py
from analises import LerRelatorioCsv, SanitizadorDados, AnalisesTecnicas, EncoderTradingJSON

# exibimos dads sobre o pacote MetaTrader5
print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)



class ConectorMT5: 
    def __init__(self, caminho_terminal="", max_tentativas_conexao=3):
        self.caminho_terminal = caminho_terminal
        self.max_tentativas_conexao = max_tentativas_conexao


    def conectar(self):
        tentativas = self.max_tentativas_conexao
        while tentativas > 0:
            if not mt5.initialize(path=self.caminho_terminal, timeout=5000):
                sleep(1)  
                tentativas -= 1
            else:
                return True
        return False
    
    def desconectar(self):  
        mt5.shutdown()

    def __enter__(self):
        if self.conectar():
            return self
        raise Exception("Falha ao conectar com MT5")
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.desconectar()

class ExtratorRelatorioSemanal:
    def extrair_relatorio(self):
        try:
            data_fim = datetime.today()
            dias_voltar = data_fim.weekday() + 1
            inicio_semana = data_fim - timedelta(days=dias_voltar)
            historico_ordens_semanal = mt5.history_deals_get(inicio_semana, data_fim)
            
            if historico_ordens_semanal is not None and len(historico_ordens_semanal) > 0:
                return historico_ordens_semanal
            else:
                return list()

        except Exception as e:
            print(f"Erro ao extrair relatório semanal: {e}")
            return list()

class FormatarRelatorioSemanal:
    def create_dataframe(self, relatorio):
        if len(relatorio) >=1:
            df = pd.DataFrame(list(relatorio), columns=relatorio[0]._asdict().keys())
            df['time'] = pd.to_datetime(df['time'], unit='s')
            return df
        else:
            df = pd.DataFrame()
            return df

#Classe abstrata para organizar as funçoes de conversao do dataframe, como salvar em csv, gerar gráficos, etc
class ConversorDataframe(ABC):
    @abstractmethod
    def salvar(self, df, path):
        pass



class ConversorCSV(ConversorDataframe):
    def salvar(self, df, caminho_completo):
        caminho_completo.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(caminho_completo, index=False, sep=';', encoding='utf-8-sig')
        return caminho_completo
       
class ConversorJSON(ConversorDataframe):
    def salvar(self, dados, caminho_completo):
        caminho_completo.parent.mkdir(parents=True, exist_ok=True)
        with open(caminho_completo, 'w', encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, indent=4, cls=EncoderTradingJSON)
        return caminho_completo


def carregar_configuracao(caminho_config="config/config.json"):
    try:
        with open(caminho_config, 'r') as arquivo:
            config = json.load(arquivo)
            return config.get("terminais", {})
    except FileNotFoundError:
        print(f"Arquivo de configuração não encontrado: {caminho_config}")
        return {}
    except json.JSONDecodeError:
        print(f"Erro ao decodificar o arquivo de configuração: {caminho_config}")
        return {}
# Criar Loop principal para executar o processo de automação em varios terminais.

if __name__ == "__main__":
    terminais = carregar_configuracao()
    print("Iniciando o processo de automação de relatórios de performance de robôs de trading...")
    
    extrator = ExtratorRelatorioSemanal()
    formatador = FormatarRelatorioSemanal()
    conversor_csv = ConversorCSV()
    conversor_json = ConversorJSON()
    
    for nome_terminal, caminho_terminal in terminais.items():
        try:
            print(f"\n--- Processando Terminal: {nome_terminal} ---")
            relatorio_semanal = []
            
            with ConectorMT5(caminho_terminal=caminho_terminal) as conector:
                print(f"Conexão com MT5 estabelecida para {nome_terminal}!")
                relatorio_semanal = extrator.extrair_relatorio()
                
            if len(relatorio_semanal) > 0:
                print(f"Relatório semanal extraído com sucesso! Ordens no período: {len(relatorio_semanal)}")
                
                # 1. Converte e salva o relatório bruto da última semana
                df_semana = formatador.create_dataframe(relatorio_semanal)
                caminho_csv = Path("relatorios/") / f"relatorio_semanal_{nome_terminal}_{datetime.today().strftime('%Y-%m-%d')}.csv"
                conversor_csv.salvar(df_semana, caminho_csv)
                print(f"Relatório semanal salvo em: {caminho_csv}")
            else:
                print("Nenhuma ordem nova encontrada no período semanal.")
                
            # 2. Carrega o histórico acumulado exclusivo deste terminal
            leitor_historico = LerRelatorioCsv(nome_terminal)
            df_historico_completo = leitor_historico.carregar_dataframe_relatorio_completo()
            
            if not df_historico_completo.empty:
                # 3. Sanitiza o histórico completo
                sanitizador = SanitizadorDados(df_historico_completo)
                df_sanitizado = sanitizador.sanitizar()
                
                if not df_sanitizado.empty:
                    # 4. Calcula métricas quantitativas acumuladas
                    analises = AnalisesTecnicas(df_sanitizado)
                    metricas_acumuladas = analises.calcular_tudo()
                    
                    # Adiciona quebras por ativo e por dia da semana
                    metricas_acumuladas['desempenho_por_ativo'] = analises.calcular_por_ativo()
                    metricas_acumuladas['desempenho_por_dia'] = analises.desempenho_por_dia()
                    
                    # 5. Salva o JSON consolidado do terminal
                    caminho_json = Path("relatorios/") / f"metricas_consolidadas_{nome_terminal}.json"
                    conversor_json.salvar(metricas_acumuladas, caminho_json)
                    print(f"Métricas históricas consolidadas salvas em: {caminho_json}")
                else:
                    print(f"Aviso: Nenhuma operação válida restou após a sanitização do histórico de {nome_terminal}.")
            else:
                print(f"Nenhum histórico acumulado encontrado para o terminal {nome_terminal}.")

        except Exception as e:
            print(f"Erro ao processar o terminal {nome_terminal}: {e}")