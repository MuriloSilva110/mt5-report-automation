import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

from pathlib import Path
class LerRelatorioCsv():

    def __init__(self,nome_terminal):
        self.terminal = nome_terminal
        self.pasta_padrao = Path('relatorios/')

    def carregar_todos_arquivos_csv_do_terminal(self):
        arquivos_do_terminal = self.pasta_padrao.glob(f'relatorio_semanal_{self.terminal}_*.csv')
        lista_arquivos = sorted(list(arquivos_do_terminal))
        if not lista_arquivos:
            return []
        return lista_arquivos

    def transforma_lista_relatorios_em_dataframe(self,lista_relatorios):
        lista_de_relatorios_dataframe = []
        for arquivo in lista_relatorios:
            try:
                relatorio_semanal = pd.read_csv(arquivo,sep=';',encoding='utf-8-sig')
                lista_de_relatorios_dataframe.append(relatorio_semanal)
            
            except pd.errors.EmptyDataError:
                print(f"O arquivo {arquivo} está vazio")
                continue
            
            except Exception as e:
                print(f"Erro ao carregar o arquivo {arquivo}: {e}")
                continue

        return lista_de_relatorios_dataframe
    
    def carregar_dataframe_relatorio_completo(self):
        lista_de_relatorios_dataframe = self.transforma_lista_relatorios_em_dataframe(self.carregar_todos_arquivos_csv_do_terminal())
        if not lista_de_relatorios_dataframe:
            return pd.DataFrame()
        return pd.concat(lista_de_relatorios_dataframe, ignore_index=True)
      

class SanitizadorDados:
    def __init__(self,df_bruto):
        self.df_bruto = df_bruto

    def _filtrar_apenas_operacoes_realizadas(self,df):
        return df[(df['type'] < 2) & (df['entry'] == 1)].copy()

    def _remover_dados_nulos(self,df):
        return df.dropna(subset=[
            'ticket','order','type','time','profit','symbol','entry'
        ])

    def _remover_duplicados(self,df):
        return df.drop_duplicates(subset=['ticket'])

    def _normalizar_coluna_time(self,df):
        df['time'] = pd.to_datetime(df['time'],errors='coerce')
        df = df.dropna(subset=['time'])
        df = df.sort_values(by='time').reset_index(drop=True)
        return df

    def _calcular_resultado_liquido(self,df):
        commission = df['commission'].fillna(0) if 'commission' in df.columns else 0
        swap = df['swap'].fillna(0) if 'swap' in df.columns else 0
        fee = df['fee'].fillna(0) if 'fee' in df.columns else 0
        df['profit_liquido'] = (
            df['profit'].fillna(0) + commission + swap + fee
        )
        return df

    def _limpar_coluna_symbol(self, df):
        if 'symbol' in df.columns:
            df['symbol'] = df['symbol'].astype(str).str.strip()
        return df
        
    def sanitizar(self):
        if self.df_bruto.empty:
            return self.df_bruto.copy()

        colunas_obrigatorias = {'ticket', 'order', 'type', 'time', 'profit', 'symbol', 'entry'}
        if not colunas_obrigatorias.issubset(self.df_bruto.columns):
            print("Aviso: O arquivo CSV não possui todas as colunas obrigatórias.")
            return pd.DataFrame()
    
        df_sanitizado = self.df_bruto.copy()
        df_sanitizado = self._remover_dados_nulos(df_sanitizado)
        df_sanitizado = self._remover_duplicados(df_sanitizado)
        df_sanitizado = self._limpar_coluna_symbol(df_sanitizado)
        df_sanitizado = self._filtrar_apenas_operacoes_realizadas(df_sanitizado)
        df_sanitizado = self._normalizar_coluna_time(df_sanitizado)
        df_sanitizado = self._calcular_resultado_liquido(df_sanitizado)
    
        return df_sanitizado
        
class AnalisesTecnicas:
    def __init__(self,df_sanitizado):
        self.df_sanitizado = df_sanitizado

    def _eh_invalido(self):
        if self.df_sanitizado is None or self.df_sanitizado.empty or 'profit_liquido' not in self.df_sanitizado.columns:
            return True
        return False

    def lucro_liquido(self):
        if self._eh_invalido():
            return 0.00
        lucro_liquido = self.df_sanitizado['profit_liquido'].sum()
        return round(float(lucro_liquido),2)
    
    def taxa_acerto(self):
        if self._eh_invalido():
            return 0.00
        total_operacoes = len(self.df_sanitizado.index)
        if total_operacoes == 0:
            return 0.00
        operacoes_ganhadoras = len(self.df_sanitizado[self.df_sanitizado['profit_liquido'] > 0].index)
        return round(float(operacoes_ganhadoras / total_operacoes) * 100,2)
    
    def fator_lucro(self):
        if self._eh_invalido():
            return 0.00
        lucro_bruto = self.df_sanitizado[self.df_sanitizado['profit_liquido'] > 0]['profit_liquido'].sum()
        prejuizo_bruto = self.df_sanitizado[self.df_sanitizado['profit_liquido'] < 0]['profit_liquido'].sum()
        if prejuizo_bruto == 0:
            return 0.00    

        try:
            resultado_fator_lucro = round(float(lucro_bruto / abs(prejuizo_bruto)), 2)
            if pd.isna(resultado_fator_lucro):
                return 0.00
            return resultado_fator_lucro
        except ZeroDivisionError:
            return 0.00

    def maior_lucro_individual(self):
        if self._eh_invalido():
            return 0.00
        resultado_maior_lucro_individual = round(float(self.df_sanitizado['profit_liquido'].max()),2)
        
        if resultado_maior_lucro_individual < 0:
            return 0.00
        return resultado_maior_lucro_individual
        

    def maior_prejuizo_individual(self):
        if self._eh_invalido():
            return 0.00
        resultado_maior_prejuizo_individual = round(float(self.df_sanitizado['profit_liquido'].min()),2)
        if resultado_maior_prejuizo_individual > 0:
            return 0.00
        return resultado_maior_prejuizo_individual

    def payoff_ratio(self):
        if self._eh_invalido():
            return 0.00
            
        operacoes_vencedoras = self.df_sanitizado[self.df_sanitizado['profit_liquido'] > 0]['profit_liquido']
        operacoes_perdedoras = self.df_sanitizado[self.df_sanitizado['profit_liquido'] < 0]['profit_liquido']

        # Caso: 0% de vitórias ou nenhuma operação com lucro positivo
        if operacoes_vencedoras.empty:
            return 0.00

        media_lucro = operacoes_vencedoras.mean()

        # Caso: 100% de vitórias (nenhuma operação perdedora)
        if operacoes_perdedoras.empty:
            return round(float(media_lucro), 2)

        media_prejuizo = abs(operacoes_perdedoras.mean())
        if media_prejuizo == 0 or pd.isna(media_prejuizo):
            return round(float(media_lucro), 2)

        try:
            return round(float(media_lucro / media_prejuizo), 2)
        except ZeroDivisionError:
            return 0.00

    def max_drawdown(self):
        if self._eh_invalido():
            return 0.00

        # Cria a série de lucros ancorada no ponto zero (0.0)
        serie_profits = pd.concat([pd.Series([0.0]), self.df_sanitizado['profit_liquido']], ignore_index=True)
    
        profit_acumulado = serie_profits.cumsum()
        max_acumulado = profit_acumulado.cummax()
        drawdown = profit_acumulado - max_acumulado
    
        return round(float(drawdown.min()), 2)

    def calcular_por_ativo(self):
        if self._eh_invalido():
            return {}
        
        resultado_por_ativo = {}
        simbolos_unicos = self.df_sanitizado['symbol'].unique()

        for simbolo in simbolos_unicos:
            df_ativo = self.df_sanitizado[self.df_sanitizado['symbol'] == simbolo].copy()

            analise_ativo = AnalisesTecnicas(df_ativo)
            resultado_por_ativo[simbolo] = analise_ativo.calcular_tudo()
        return resultado_por_ativo

    def desempenho_por_dia(self):
        if self._eh_invalido():
            return {}

        df_temp = self.df_sanitizado.copy()
        df_temp['num_dia'] = df_temp['time'].dt.dayofweek
        df_temp['dia_semana'] = df_temp['time'].dt.day_name()

        # Agrupa mantendo a ordem dos dias da semana
        agrupado = df_temp.groupby(['num_dia', 'dia_semana'])['profit_liquido'].agg(
            lucro_liquido='sum',
            total_operacoes='count'
        ).reset_index()

        # Formata o retorno em um dicionário limpo
        resultado = {}
        for _, row in agrupado.iterrows():
            dia = row['dia_semana']
            resultado[dia] = {
                'lucro_liquido': round(float(row['lucro_liquido']), 2),
                'total_operacoes': int(row['total_operacoes'])
            }

        return resultado

    def calcular_tudo(self):
        return {
            'lucro_liquido': self.lucro_liquido(),
            'taxa_acerto': self.taxa_acerto(),
            'fator_lucro': self.fator_lucro(),
            'total_operacoes': 0 if self._eh_invalido() else len(self.df_sanitizado.index),
            'maior_lucro_individual': self.maior_lucro_individual(),
            'maior_prejuizo_individual': self.maior_prejuizo_individual(),
            'payoff_ratio': self.payoff_ratio(),
            'max_drawdown': self.max_drawdown(),
        }

        

class VisualizadorPerformance:
    def __init__(self,df_sanitizado,nome_terminal):
        self.df_sanitizado = df_sanitizado
        self.nome_terminal = nome_terminal

    def curva_capital(self):
        df = self.df_sanitizado.copy()
        if df.empty or 'profit_liquido' not in df.columns:
            return
        df['profit_acumulado'] = df['profit_liquido'].cumsum()
        plt.plot(df['time'],df['profit_acumulado'],label='Curva de Capital')
        plt.title(f'Curva de Capital Acumulada {self.nome_terminal}')
        plt.xlabel('Data / Hora')
        plt.ylabel('Lucro Acumulado (R$)')
        plt.axhline(0, color='red', linestyle='--')
        plt.grid(True, linestyle=':', alpha=0.6)
        plt.legend()
        plt.tight_layout()
        plt.show()


class EncoderTradingJSON(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (pd.Timestamp, datetime)):
            return obj.isoformat()
        return super().default(obj)

if __name__ == "__main__":

    nome_terminal = "Terminal1"

    ler_relatorio_csv = LerRelatorioCsv(nome_terminal)

    dataframe_relatorio = ler_relatorio_csv.carregar_dataframe_relatorio_completo()
    
    if len(dataframe_relatorio) == 0:

        print(f"Nenhum arquivo .csv encontrado para o terminal {nome_terminal}")
    else:

        sanitizador = SanitizadorDados(dataframe_relatorio)

        dataframe_sanitizado = sanitizador.sanitizar()
        
        analises = AnalisesTecnicas(dataframe_sanitizado)
        
        relatorio_completo = analises.calcular_tudo()
        
        print("--- RELATÓRIO COMPLETO EM JSON ---")
        json_resultado = json.dumps(relatorio_completo, indent=4, cls=EncoderTradingJSON)
        print(json_resultado)

        visualizador = VisualizadorPerformance(dataframe_sanitizado, nome_terminal)
        visualizador.curva_capital()