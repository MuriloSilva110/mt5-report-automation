'''
projeto de automação de relatórios de performance de robôs de trading, utilizando a biblioteca MT5 para coletar 
os dados e a biblioteca pandas para organizar e gerar os relatórios.
'''
# Importando as bibliotecas necessárias
import MetaTrader5 as mt5
from time import sleep

# exibimos dads sobre o pacote MetaTrader5
print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)

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
        

#chama a funçao para se conectar ao terminal especificado
if conectar_terminal(caminho_terminal="C:\\Program Files\\MetaTrader-pessoal\\terminal64.exe"):
    print("Conexão ao terminal MetaTrader 5 estabelecida com sucesso.")
    # Imprimimos informaçoes  sobre o estado da conexao, o nome do servidor e a conta de negociaçao (# Futura def)
    print(mt5.terminal_info())

    # imprimimos informaçoes sobre a versao do mt5 (# Futura def)
    print(mt5.version())
else:
    print(f"Falha ao conectar ao terminal MetaTrader 5 após várias tentativas. verifique o caminho do terminal e tente novamente.\nErro: {mt5.last_error()}")


# concluimos a conexao ao terminal mt5 (# Futura def)
mt5.shutdown()