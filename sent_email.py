import smtplib  # Biblioteca para envio de e-mails usando o protocolo SMTP
from email.mime.base import MIMEBase  # Permite anexar arquivos no e-mail
from email.mime.text import MIMEText  # Permite adicionar texto simples ao e-mail
from email.mime.multipart import MIMEMultipart  # Cria um e-mail com múltiplas partes (texto, anexos, etc.)
from email import encoders  # Para codificar anexos em base64
import os  # Para interagir com variáveis de ambiente e sistema de arquivos
from dotenv import load_dotenv  # Para carregar variáveis de ambiente de um arquivo .env
import time

# Carregar as variáveis do arquivo .env
load_dotenv()

# Obtém as credenciais de e-mail do arquivo .env
user_email = os.getenv('USER_EMAIL')  # E-mail do remetente
pass_email = os.getenv('PASSWORD_EMAIL')  # Senha do remetente

# Configurações do servidor de e-mail (exemplo com Gmail)
smtp_server = 'smtp.gmail.com'  # Servidor SMTP do Gmail
smtp_port = 587  # Porta usada para envio de e-mails com TLS (Gmail usa 587)
email_user = user_email  # E-mail do remetente
email_password = pass_email  # Senha do remetente


def sendEmail(
        to,
        total_time,
        retorno_dolar,
        retorno_sp500,
        total_items
):

    print("SEND EMAIL.")
    # Informações do e-mail
    from_email = email_user  # Define o remetente como o próprio usuário
    to_email = to  # Destinatário do e-mail
    subject = 'Relatório de Mercado'  # Assunto do e-mail

    # Corpo do e-mail com os retornos diários dos índices e moedas
    body = f'''Prezados, segue o relatório de mercado:
    
    * USD/BRL (BRL=X) teve o retorno de {retorno_dolar}.
    
    * S&P 500 (^GSPC) teve o retorno de {retorno_sp500}.
    
    * {total_items} registros encontrados.
    
    Segue em anexo a peformance dos ativos nos últimos {total_time}.

    Att,
    Yahoo Finance
    '''

    # Montando o e-mail
    message = MIMEMultipart()  # Cria uma mensagem com múltiplas partes (corpo e anexos)
    message['From'] = from_email  # Define o campo "De"
    message['To'] = to_email  # Define o destinatário
    message['Subject'] = subject  # Define o assunto

    # Corpo do e-mail
    message.attach(MIMEText(body, 'plain'))  # Adiciona o texto ao corpo do e-mail

    # Função para anexar arquivos ao e-mail
    def anexar_arquivo(message, file_path):
        if not os.path.isfile(file_path):
            print(f'Arquivo não encontrado: {file_path}')
            return

        with open(file_path, 'rb') as attachment:  # Abre o arquivo no modo binário de leitura
            part = MIMEBase('application', 'octet-stream')  # Define o tipo de conteúdo do anexo
            part.set_payload(attachment.read())  # Lê o arquivo e o coloca no payload do e-mail
            encoders.encode_base64(part)  # Codifica o conteúdo em base64 para envio seguro
            part.add_header('Content-Disposition',
                            f'attachment; filename={file_path.split("/")[-1]}')  # Define o cabeçalho do anexo com o nome do arquivo
            message.attach(part)  # Anexa o arquivo à mensagem

        # Definir o caminho para a pasta 'dataset' na raiz do projeto

    # Tempo para as images serem salvas
    time.sleep(5)

    # Define o caminho completo do arquivo CSVx
    anexo_dolar = "../dataset/dollar.html"
    anexo_sp = "../dataset/sp500.html"

    # Anexa os arquivos ao e-mail
    anexar_arquivo(message, anexo_dolar)
    anexar_arquivo(message, anexo_sp)

    # Envia o e-mail
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)  # Conecta ao servidor SMTP do Gmail
        server.starttls()  # Ativa a segurança TLS
        server.login(email_user, email_password)  # Realiza o login no servidor SMTP com as credenciais

        # Converte o e-mail para string e o envia
        text = message.as_string()
        server.sendmail(from_email, to_email, text)

        print('E-mail enviado com sucesso!')

        server.quit()  # Fecha a conexão com o servidor SMTP
    except Exception as e:  # Captura qualquer erro durante o processo de envio
        print(f'Erro ao enviar o e-mail: {e}')
