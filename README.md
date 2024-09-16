# Sistema de Análise de Ativos Financeiros e Envio de Relatórios

- [Installation](#installation)
- [Usage](#usage)
- [Dataset](#dataset)
- [Config](#config)
- [Contributing](#contributing)

<h2 id="installation">⚡ Installation</h2>

1. Clone the repository:

```bash
git remote add origin https://github.com/setxpro/sistema_analise_ativos.git
```
2. Install dependencies with Maven

```bash 
    pip install -r requirements.txt
```

---

<h2 id="usage">🚀 Usage</h2>



## Scripts Python

1. get_dataset.py:
- Importação do yfinance: Coleta dados financeiros do Yahoo Finance.
- Definição dos Ativos: Índice IBOVESPA (^BVSP), S&P 500 (^GSPC) e taxa USD/BRL (BRL=X).
- Coleta e Tratamento dos Dados: Baixa os dados dos últimos 6 meses, remove valores faltantes e salva em CSV.

2. main.py:
- Inicialização do Spark: Leitura e manipulação de grandes conjuntos de dados.
- Cálculo dos Retornos Diários: Calcula o retorno diário dos ativos.
- Plotagem de Gráficos: Gera gráficos dos retornos dos ativos.
- Cálculo dos Últimos Retornos: Calcula o último retorno diário de cada ativo.

4. sent_email.py:
- Configuração do Servidor SMTP: Define o servidor SMTP do Gmail para o envio de e-mails.
- Corpo do E-mail: Inclui um relatório com os retornos diários e anexos dos gráficos.
- Anexar Arquivos e Enviar E-mail: Anexa os gráficos e envia o e-mail com os dados.


<h2 id="dataset">🗄️ Dataset</h2>
O dataset utilizado no projeto contém dados de mercado para os seguintes ativos:

IBOVESPA
S&P 500
USD/BRL
Os dados são coletados diretamente do Yahoo Finance e armazenados em um arquivo CSV (dataset/market_data.csv).

<h2 id="config">🛠️ Config</h2>
## Configuração do Ambiente
1. Arquivo .env:
- USER_EMAIL: E-mail do remetente.
- PASSWORD_EMAIL: Senha do e-mail do remetente.

## Explicação Detalhada
- main.py:
  - Spark Session: Inicializa uma sessão do Spark para manipular grandes conjuntos de dados.
  - Leitura e Limpeza de Dados: Lê o CSV, remove valores nulos e calcula retornos diários.
  - Conversão e Plotagem: Converte para pandas e gera gráficos com estilo cyberpunk.
- get_dataset.py:
  - Importação e Definição: Usa yfinance para obter dados financeiros.
  - Tratamento e Armazenamento: Processa e salva os dados em um CSV.
- sent_email.py:
  - Configuração e Envio: Define o servidor SMTP e configura o e-mail para envio com anexos.


## Estrutura do docker-compose.yml

- <h4>Spark Master</h4>```spark-master```
  - Imagem: Utiliza a imagem ````bitnami/spark:latest```` para o Spark master.
  - Variáveis de ambiente: Define o modo do Spark como master.
  - Portas: Expõe as portas 8080 e 7077.
  - Redes: Conecta-se à rede ```spark-network```.
- <h4>Spark Worker</h4> ```spark-worker```
  - Imagem: Também utiliza a imagem bitnami/spark:latest para o Spark worker.
  - Variáveis de ambiente: Define o modo do Spark como worker e especifica a URL do Spark master.
  - Dependências: Garante que o spark-master esteja ativo antes de iniciar.
  - Redes: Conecta-se à rede spark-network.
- <h4>Jupyter Notebook</h4> ```jupyter``` 
  - Imagem: jupyter/pyspark-notebook
  - Função: Fornece um ambiente Jupyter para análises e processamento com PySpark.
  - Portas: Expõe 8888 (interface do Jupyter Notebook).
  - Volumes: Mapeia o diretório local ./notebooks para o diretório de trabalho do Jupyter.
  - Dependências: Garante que spark-master e spark-worker estejam ativos.
  - Rede: Conecta-se à spark-network.
  - Comando: Inicia o Jupyter sem um token de autenticação.
- <h4>Elasticsearch</h4> ```elasticsearch```
  - Imagem: docker.elastic.co/elasticsearch/elasticsearch:8.10.2
  - Função: Armazenamento e pesquisa de dados.
  - Portas: Expõe 9200 (interface REST).
  - Volumes: Utiliza o volume elasticsearch_data para persistência.
  - Rede: Conecta-se à spark-network.
- <h4>Kibana</h4> ```kibana```
  - Imagem: docker.elastic.co/kibana/kibana:8.10.2
  - Função: Interface de visualização para dados no Elasticsearch.
  - Portas: Expõe 5601 (interface do Kibana).
  - Dependências: Garante que o elasticsearch esteja ativo.
  - Rede: Conecta-se à spark-network.
- <h4>Hadoop NameNode</h4> ```namenode```
  - Imagem: bde2020/hadoop-namenode:2.0.0-hadoop3.2.1-java8
  - Função: Gerencia o sistema de arquivos distribuído Hadoop (HDFS).
  - Portas: Expõe 50070 (interface web) e 8020 (RPC do Namenode).
  - Volumes: Utiliza o volume namenode-data para persistência.
  - Rede: Conecta-se à spark-network.
  - Comando: Formata o HDFS e inicia o Namenode.

- <h4>Hadoop DataNode</h4> ```datanode```
  - Imagem: bde2020/hadoop-datanode:2.0.0-hadoop3.2.1-java8
  - Função: Armazena blocos de dados no HDFS.
  - Variáveis: Configura a conexão com o Namenode.
  - Dependências: Garante que o namenode esteja ativo.
  - Portas: Expõe 50075

- Volumes: Utiliza o volume datanode-data para persistência.
- Rede: Conecta-se à spark-network.
- Comando: Inicia o DataNode.


## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request to the repository.

When contributing to this project, please follow the existing code style, [commit conventions](https://github.com/iuricode/padroes-de-commits), and submit your changes in a separate branch.