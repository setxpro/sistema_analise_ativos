# Importações de bibliotecas necessárias
import matplotlib.pyplot as plt  # Para visualização de gráficos
import mplcyberpunk  # Estilo gráfico 'cyberpunk' para o matplotlib
from pyspark.sql import SparkSession  # Para trabalhar com Spark DataFrames
from pyspark.sql.functions import col, lag  # Funções para manipulação de colunas no Spark
from pyspark.sql.window import Window  # Para definição de janelas em cálculos de séries temporais

# Inicializa uma Spark Session para ler e manipular dados
# (master) Define o modo de execução local
# (appName) Nomeia a aplicação
# (getOrCreate) Cria a sessão
spark = SparkSession.builder \
    .master("local") \
    .appName("Market Data Analysis") \
    .getOrCreate()

# Define o caminho para o arquivo CSV contendo os dados do mercado
file_path = "dataset/market_data.csv"

# Lê o arquivo CSV e cria um DataFrame do Spark
# O cabeçalho é inferido e o esquema de tipos é automaticamente detectado
stock_prices_df = spark.read \
    .format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .option("sep", ",") \
    .load(file_path)

# (opcional) Mostra o DataFrame carregado para inspeção
# stock_prices_df.show()

# Remove quaisquer registros com valores ausentes (NaN) nas colunas do DataFrame
dados_mercado = stock_prices_df.dropna()

# (opcional) Mostra o DataFrame após remover os valores ausentes
# dados_mercado.show()

###########################################################
# Cálculo dos retornos diários
###########################################################

# Define uma especificação de janela ordenada pela coluna "Date"
# Isso é necessário para calcular os retornos baseados no valor anterior da mesma coluna
windowSpec = Window.orderBy("Date")

# Calcula o retorno diário para a coluna "DOLAR" (diferença percentual entre o valor atual e o valor anterior)
retornos_diarios = dados_mercado.withColumn(
    "DOLAR", (col("DOLAR") / lag("DOLAR").over(windowSpec) - 1) * 100)

# Calcula o retorno diário para a coluna "IBOVESPA"
retornos_diarios = dados_mercado.withColumn(
    "IBOVESPA", (col("IBOVESPA") / lag("IBOVESPA").over(windowSpec) - 1) * 100)

# Calcula o retorno diário para a coluna "S&P500"
retornos_diarios = dados_mercado.withColumn(
    "S&P500", (col("S&P500") / lag("S&P500").over(windowSpec) - 1) * 100)

# (opcional) Mostra o DataFrame com os retornos diários calculados
# retornos_diarios.show()

# Salva o DataFrame resultante com os retornos diários em um arquivo CSV
# retornos_diarios.write.csv("dataset/market_data_with_returns", header=True)

# Define o estilo gráfico 'cyberpunk' para os gráficos que serão gerados
plt.style.use("cyberpunk")

# Converte o DataFrame do Spark para um DataFrame do pandas para facilitar a plotagem de gráficos
pdf = retornos_diarios.toPandas()


###########################################################
# Plotagem dos gráficos
###########################################################

# Gráfico do IBOVESPA
plt.figure(figsize=(10, 5))  # Define o tamanho da figura
plt.plot(pdf["Date"], pdf["IBOVESPA"], label="IBOVESPA")  # Plota os dados do IBOVESPA
plt.title("IBOVESPA")  # Adiciona título ao gráfico
plt.xlabel("Date")  # Adiciona o rótulo do eixo X
plt.ylabel("Price")  # Adiciona o rótulo do eixo Y
plt.legend()  # Exibe a legenda
plt.xticks(rotation=45)  # Rotaciona os rótulos do eixo X
plt.tight_layout()  # Ajusta o layout para evitar sobreposição
# plt.savefig("dataset/ibovespa.png")  # (opcional) Salva o gráfico como imagem


# Gráfico do DOLAR
plt.figure(figsize=(10, 5))
plt.plot(pdf["Date"], pdf["DOLAR"], label="DOLAR")
plt.title("DOLAR")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
# plt.savefig("dataset/dolar.png")

# Gráfico do S&P500
plt.figure(figsize=(10, 5))
plt.plot(pdf["Date"], pdf["S&P500"], label="S&P500")
plt.title("S&P500")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
# plt.savefig("dataset/sp500.png")

###########################################################
# Cálculo dos últimos retornos diários
###########################################################

# DOLAR
# Converte o DataFrame do Spark para pandas para manipulação de dados
df_dolar = retornos_diarios.select("DOLAR").toPandas()
# Pega o último valor de retorno diário para o DOLAR
last_value_dolar = df_dolar["DOLAR"].iloc[-1]
# Formata o valor como porcentagem
retorno_dolar = str(round(last_value_dolar * 100, 2)) + "%"
print("ÚLTIMO VALOR DIÁRIO DO DOLAR")
print(retorno_dolar)

# IBOVESPA
# Mesmo procedimento para o IBOVESPA
df_ibovespa = retornos_diarios.select("IBOVESPA").toPandas()
last_value_ibovespa = df_ibovespa["IBOVESPA"].iloc[-1]
retorno_ibovespa = str(round(last_value_ibovespa * 100, 2)) + "%"
print("ÚLTIMO VALOR DIÁRIO DO IBOVESPA")
print(retorno_ibovespa)


# S&P500
# Mesmo procedimento para o S&P500
df_ps = retornos_diarios.select("S&P500").toPandas()
last_value_ps = df_ps["S&P500"].iloc[-1]
retorno_sp500 = str(round(last_value_ps * 100, 2)) + "%"
print("ÚLTIMO VALOR DIÁRIO DO S&P500")
print(retorno_sp500)