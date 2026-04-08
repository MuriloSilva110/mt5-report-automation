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


# exibimos dads sobre o pacote MetaTrader5
print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)

# tRANSFORMAR O RELATORIO EM UM DATAFRAME DO PANDAS PARA MELHOR ANALISE E VISUALIZAÇAO (Futura def)
def transformar_relatorio_em_dataframe(relatorio):
    df = pd.DataFrame(list(relatorio), columns=relatorio[0]._asdict().keys())
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df

# Tranformar o DataFrame em um arquivo CSV para facilitar a análise e compartilhamento (Futura def)
def salvar_relatorio_como_csv(df):
    # verificar se o diretório "relatorios" existe, se não, criar-lo
    diretorio_relatorios = Path("relatorios")
    if not diretorio_relatorios.exists():
        diretorio_relatorios.mkdir()
    # Gerar um nome de arquivo com base na data atual
    nome_arquivo = diretorio_relatorios / f"relatorio_semanal_{datetime.now().strftime('%Y%m%d')}.csv"
    # Salvar o DataFrame em um arquivo CSV
    df.to_csv(nome_arquivo, index=False, sep=';', encoding='utf-8-sig')



# funçao para se conectar ao terminal (# Futura class)
def conectar_terminal(caminho_terminal="", max_tentativas_conexao=3):
    while max_tentativas_conexao > 0:
        # estabelecemos a conexão com o terminal MetaTrader 5 para a conta especificada
        if not mt5.initialize(path=caminho_terminal, timeout=5000):
            sleep(1)  # Aguarda 1 segundo antes de tentar se conectar novamente
            max_tentativas_conexao -= 1
        else:
            return True
    return False
        

# Funçao que extrai o relatorio de operaçoes semanal
def extrair_relatorio_semanal():
    # Calvula a data de início e fim da semana atual com base no dia atual
        #otem o dia atual
    data_fim = datetime.today()
    dias_voltar = data_fim.weekday() + 1 # Obtém o número do dia da semana (0=segunda-feira, 6=domingo)
    inicio_semana = data_fim - timedelta(days=dias_voltar)  # Calcula o início da semana (domingo)
    historico_odens_semanal = mt5.history_deals_get(inicio_semana, data_fim)
   

    if historico_odens_semanal is not None and len(historico_odens_semanal) > 0:
        return historico_odens_semanal
    
    else:
        return f"Falha ao extrair o relatório semanal. Verifique a conexão com o terminal e tente novamente.\nErro: {mt5.last_error()}"
    


#chama a funçao para se conectar ao terminal especificado
if conectar_terminal(caminho_terminal="C:\\Program Files\\MetaTrader-pessoal\\terminal64.exe"):
    print("Conexão ao terminal MetaTrader 5 estabelecida com sucesso.")
    # Imprimimos informaçoes  sobre o estado da conexao, o nome do servidor e a conta de negociaçao (# Futura def)
    print(mt5.terminal_info())

    # imprimimos informaçoes sobre a versao do mt5 (# Futura def)
    print(mt5.version())


    relatorio = extrair_relatorio_semanal()
    if isinstance(relatorio, str):
        print(relatorio)  # Imprime a mensagem de erro se a extração falhou
    else:
        df_relatorio = transformar_relatorio_em_dataframe(relatorio)
        salvar_relatorio_como_csv(df_relatorio)
        print("Relatório semanal extraído e salvo com sucesso.")
        print('=+='*20)
        print(df_relatorio)  # Imprime o DataFrame do relatório semanal
        print('=+='*20)

else:
    print(f"Falha ao conectar ao terminal MetaTrader 5 após várias tentativas. verifique o caminho do terminal e tente novamente.\nErro: {mt5.last_error()}")


# concluimos a conexao ao terminal mt5 (# Futura def)
mt5.shutdown()


'''
df.to_csv('dados_formatados.csv', index=False, sep=';', encoding='utf-8-sig')
'''