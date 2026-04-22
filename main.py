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
import os
from dotenv import load_dotenv
from abc import ABC, abstractmethod
import json
# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Busca o caminho de forma segura
CAMINHO_MT5 = os.getenv("MT5_TERMINAL_PATH")

# exibimos dads sobre o pacote MetaTrader5
print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)



class ConectorMT5: 
    def __init__(self, caminho_terminal="", max_tentativas_conexao=3):
        self.caminho_terminal = caminho_terminal
        self.max_tentativas_conexao = max_tentativas_conexao


    def conectar(self):
        while self.max_tentativas_conexao > 0:
            if not mt5.initialize(path=self.caminho_terminal, timeout=5000):
                sleep(1)  
                self.max_tentativas_conexao -= 1
            else:
                return True
        return False
    
    def desconectar(self):  
        mt5.shutdown()

class ExtratorRelatorioSemanal:
    def extrair_relatorio(self):
        data_fim = datetime.today()
        dias_voltar = data_fim.weekday() + 1
        inicio_semana = data_fim - timedelta(days=dias_voltar)
        historico_odens_semanal = mt5.history_deals_get(inicio_semana, data_fim)
        if historico_odens_semanal is not None and len(historico_odens_semanal) > 0:
            return historico_odens_semanal
        else:
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
    def salvar(self, df, path, nome_terminal):
        diretorio_relatorios = Path(path)
        if not diretorio_relatorios.exists():
            diretorio_relatorios.mkdir()
        nome_arquivo = diretorio_relatorios / f"relatorio_semanal_{nome_terminal}_{datetime.now().strftime('%Y%m%d')}.csv"
        df.to_csv(nome_arquivo, index=False, sep=';', encoding='utf-8-sig')
    
        return nome_arquivo



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
    for nome_terminal, caminho_terminal in terminais.items():
        conector = ConectorMT5(caminho_terminal=caminho_terminal)
        if conector.conectar():
            print(f"Conexão com MT5 estabelecida com sucesso para o terminal {nome_terminal}!")
            extrator = ExtratorRelatorioSemanal()
            relatorio_semanal = extrator.extrair_relatorio()
            if len(relatorio_semanal) > 0:
                print(f"Relatório semanal extraído com sucesso! Total de ordens: {len(relatorio_semanal)}")
                formatador = FormatarRelatorioSemanal()
                df_relatorio = formatador.create_dataframe(relatorio_semanal)
                conversor_csv = ConversorCSV()
                caminho_relatorio = conversor_csv.salvar(df_relatorio, path="relatorios", nome_terminal=nome_terminal)
                print(f"Relatório semanal salvo em: {caminho_relatorio}")
                conector.desconectar()
            else:
                print("Nenhuma ordem encontrada no período semanal. Verifique se há dados disponíveis.")
                conector.desconectar()
        else:
            print(f"Falha ao conectar com MT5. Verifique o caminho do terminal {nome_terminal} e tente novamente.")

