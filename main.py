# main.py
import matplotlib.pyplot as plt
import mplcyberpunk
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lag
from pyspark.sql.window import Window
import os

from sent_email import sendEmail


def analyze_market_data(email):
    # Definir o caminho para a pasta 'dataset' na raiz do projeto
    root_dir = os.path.dirname(os.path.abspath(__file__))  # Diretório atual do script
    project_root = os.path.abspath(os.path.join(root_dir))  # Raiz do projeto
    dataset_dir = os.path.join(project_root, 'dataset')  # Pasta 'dataset' na raiz do projeto

    # Se o diretório não existir, ele será criado
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)

    # Define o caminho completo do arquivo CSV
    file_path = os.path.join(dataset_dir, "market_data.csv")

    # Inicializa uma Spark Session para ler e manipular dados
    spark = SparkSession.builder \
        .master("local") \
        .appName("Market Data Analysis") \
        .getOrCreate()

    # Lê o arquivo CSV e cria um DataFrame do Spark
    try:
        stock_prices_df = spark.read \
            .format("csv") \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .option("sep", ",") \
            .load(file_path)
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
        spark.stop()
        return False

    # Remove quaisquer registros com valores ausentes (NaN) nas colunas do DataFrame
    dados_mercado = stock_prices_df.dropna()

    # Define uma especificação de janela ordenada pela coluna "Date"
    windowSpec = Window.orderBy("Date")

    # Calcula o retorno diário para as colunas
    retornos_diarios = dados_mercado.withColumn(
        "DOLAR", (col("DOLAR") / lag("DOLAR").over(windowSpec) - 1) * 100)
    retornos_diarios = retornos_diarios.withColumn(
        "IBOVESPA", (col("IBOVESPA") / lag("IBOVESPA").over(windowSpec) - 1) * 100)
    retornos_diarios = retornos_diarios.withColumn(
        "S&P500", (col("S&P500") / lag("S&P500").over(windowSpec) - 1) * 100)

    # Define o estilo gráfico 'cyberpunk' para os gráficos que serão gerados
    plt.style.use("cyberpunk")

    # Converte o DataFrame do Spark para um DataFrame do pandas para facilitar a plotagem de gráficos
    pdf = retornos_diarios.toPandas()

    # Plotagem dos gráficos
    try:

        # Ajuste o tamanho da figura para visualização de longo prazo
        plt.figure(figsize=(40, 20))  # Mais largo para melhor visualização em um longo período
        plt.plot(pdf["Date"], pdf["IBOVESPA"], label="IBOVESPA")
        plt.title("IBOVESPA")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("../dataset/ibovespa.png")  # Salva o gráfico

        plt.figure(figsize=(40, 20))  # Mais largo para melhor visualização em um longo períodovs
        plt.plot(pdf["Date"], pdf["DOLAR"], label="DOLAR")
        plt.title("DOLAR")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("../dataset/dollar.png")  # Salva o gráfico

        plt.figure(figsize=(40, 20))  # Mais largo para melhor visualização em um longo período
        plt.plot(pdf["Date"], pdf["S&P500"], label="S&P500")
        plt.title("S&P500")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("../dataset/sp500.png")  # Salva o gráfico

    except Exception as e:
        print(f"Erro ao gerar gráficos: {e}")

    # Cálculo dos últimos retornos diários
    try:
        df_dolar = retornos_diarios.select("DOLAR").toPandas()
        last_value_dolar = df_dolar["DOLAR"].iloc[-1]
        retorno_dolar = str(round(last_value_dolar, 2)) + "%"

        df_ibovespa = retornos_diarios.select("IBOVESPA").toPandas()
        last_value_ibovespa = df_ibovespa["IBOVESPA"].iloc[-1]
        retorno_ibovespa = str(round(last_value_ibovespa, 2)) + "%"

        df_ps = retornos_diarios.select("S&P500").toPandas()
        last_value_ps = df_ps["S&P500"].iloc[-1]
        retorno_sp500 = str(round(last_value_ps, 2)) + "%"

        total_items = stock_prices_df.count()

        # Envio do e-mail
        sendEmail(email, retorno_ibovespa, retorno_dolar, retorno_sp500, total_items)

    except Exception as e:
        print(f"Erro ao calcular retornos diários: {e}")

    # Finaliza a sessão do Spark
    spark.stop()

    return True
