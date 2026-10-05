import pandas as pd
import matplotlib.pyplot as plt
# Ler e transformar relatorio em um dataframe
relatorio_semanal = pd.read_csv('relatorios/relatorio_semanal_Terminal0_20261001.csv', sep=';')
relatorio_semanal = relatorio_semanal[relatorio_semanal['type'] < 2]

# exibir data frame
print(relatorio_semanal.head())

# Gurdar em uma variavel as linhas onde o profit e maior que 0
relatorio_lucros = relatorio_semanal[(relatorio_semanal['profit'] > 0) & (relatorio_semanal['type'] < 2)]

# Gurdar em uma variavel as linhas onde o profit e menor que 0
relatorio_prejuizos = relatorio_semanal[(relatorio_semanal['profit'] < 0) & (relatorio_semanal['type'] < 2)]


# Exibir relatorio de lucros
print('relatorio de lucros:\n', relatorio_lucros.head())

# Exibir total de lucro bruto 
lucro_bruto = relatorio_lucros['profit'].sum()
print(f'lucro bruto: R${lucro_bruto:.2f}')

# Exibir relatorio de prejuizos
print(relatorio_prejuizos)

#Exibir total de prejuizo bruto 
prejuizo_bruto = relatorio_prejuizos['profit'].sum()
print(f'prejuizo bruto: R${prejuizo_bruto:.2f}')

# Exibir resultado liquido semanal
resultado_liquido = lucro_bruto - abs(prejuizo_bruto)
print(f'resultado liquido: R${resultado_liquido:.2f}')

#calcular taxa de acerto 
taxa_acerto = len(relatorio_lucros) / len(relatorio_semanal) * 100
print(f'taxa de acerto: {taxa_acerto:.2f}%')

#Calcular fator de lucro
## tratar divisao po zero 
try:
    fator_lucro = lucro_bruto / abs(prejuizo_bruto)
    print(f'fator de lucro: {fator_lucro:.2f}')
except ZeroDivisionError:
    print('Sem operaçoes perdedoras',prejuizo_bruto)


# Exibir grafico para visualizar o lucro ao longo do tempo
relatorio_semanal['lucro_acumulado'] = relatorio_semanal['profit'].cumsum()
print(relatorio_semanal.head())



plt.plot(relatorio_semanal['time'], relatorio_semanal['lucro_acumulado'])
plt.xlabel('Tempo')
plt.ylabel('Lucro')
plt.title('Lucro ao longo do tempo')
plt.show()