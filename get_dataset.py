import yfinance as yf  # Importa a biblioteca yfinance para obter dados de mercado financeiro

# Ativos - https://finance.yahoo.com
# Definição dos ativos de interesse:
# ^BVSP - Índice IBOVESPA (índice de ações da bolsa brasileira)
# ^GSPC - S&P 500 (índice de ações dos EUA)
# BRL=X - Taxa de câmbio USD/BRL (Dólar americano para Real brasileiro)
tickers = ["^BVSP", "^GSPC", "BRL=X"]

# Baixa os dados ajustados de fechamento ('Adj Close') dos últimos 6 meses para os ativos especificados
# A função yf.download retorna um DataFrame com os preços diários dos ativos
dados_mercado = yf.download(tickers, period="6mo")["Adj Close"]

# Remove quaisquer valores faltantes do DataFrame (linhas com NaN) para garantir que os dados estejam completos
dados_mercado = dados_mercado.dropna()

# Renomeia as colunas para facilitar a leitura e identificação
# 'BRL=X' é renomeado para 'DOLAR', '^BVSP' para 'IBOVESPA' e '^GSPC' para 'S&P500'
dados_mercado.columns = ["DOLAR", "IBOVESPA", "S&P500"]

# Salva os dados de mercado processados em um arquivo CSV para análise posterior
# O arquivo será salvo no diretório 'dataset' com o nome 'market_data.csv'
dados_mercado.to_csv("dataset/market_data.csv")