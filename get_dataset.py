import yfinance as yf  # Importa a biblioteca yfinance para obter dados de mercado financeiro
import os


def createDataset(start, end):
    # Ativos - https://finance.yahoo.com
    # Definição dos ativos de interesse:
    # ^BVSP - Índice IBOVESPA (índice de ações da bolsa brasileira)
    # ^GSPC - S&P 500 (índice de ações dos EUA)
    # BRL=X - Taxa de câmbio USD/BRL (Dólar americano para Real brasileiro)
    tickers = ["^GSPC", "BRL=X"]

    # Baixa os dados ajustados de fechamento ('Adj Close') dos últimos 6 meses para os ativos especificados
    # A função yf.download retorna um DataFrame com os preços diários dos ativos
    print(start)
    print(end)

    dados_mercado = yf.download(tickers, start=start, end=end)["Adj Close"]
    # Remove quaisquer valores faltantes do DataFrame (linhas com NaN) para garantir que os dados estejam completos
    dados_mercado = dados_mercado.dropna()

    # Renomeia as colunas para facilitar a leitura e identificação
    # 'BRL=X' é renomeado para 'DOLAR', '^BVSP' para 'IBOVESPA' e '^GSPC' para 'S&P500'
    dados_mercado.columns = ["DOLAR", "S&P500"]

    # Definir o caminho para a pasta 'dataset' na raiz do projeto
    root_dir = os.path.dirname(os.path.abspath(__file__))  # Diretório atual do script
    project_root = os.path.abspath(os.path.join(root_dir))  # Raiz do projeto
    dataset_dir = os.path.join(project_root, 'dataset')  # Pasta 'dataset' na raiz do projeto

    # Se o diretório não existir, ele será criado
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)

    # Define o caminho completo do arquivo CSV
    file_path = os.path.join(dataset_dir, "market_data.csv")

    # Exibe o caminho onde o arquivo será salvo
    print(f"Saving dataset to: {os.path.abspath(file_path)}")
    dados_mercado.to_csv(file_path)

    return True
