from main import retorno_ibovespa, retorno_dolar, retorno_sp500  # Importa os retornos calculados do arquivo 'main.py'

import smtplib  # Biblioteca para envio de e-mails usando o protocolo SMTP
from email.mime.base import MIMEBase  # Permite anexar arquivos no e-mail
from email.mime.text import MIMEText  # Permite adicionar texto simples ao e-mail
from email.mime.multipart import MIMEMultipart  # Cria um e-mail com múltiplas partes (texto, anexos, etc.)
from email import encoders  # Para codificar anexos em base64
import os  # Para interagir com variáveis de ambiente e sistema de arquivos
from dotenv import load_dotenv  # Para carregar variáveis de ambiente de um arquivo .env


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

# Informações do e-mail
from_email = email_user  # Define o remetente como o próprio usuário
to_email = 'patrickpqdt87289@gmail.com'  # Destinatário do e-mail
subject = 'Relatório de Mercado'  # Assunto do e-mail

# Corpo do e-mail com os retornos diários dos índices e moedas
body = f'''Prezado diretor, segue o relatório de mercado:

* O Ibovespa teve o retorno de {retorno_ibovespa}.
* O Dólar teve o retorno de {retorno_dolar}.
* O S&P500 teve o retorno de {retorno_sp500}.

Segue em anexo a peformance dos ativos nos últimos 6 meses.

Att,
Patrick Anjos
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
        part.add_header('Content-Disposition', f'attachment; filename={file_path.split("/")[-1]}')  # Define o cabeçalho do anexo com o nome do arquivo
        message.attach(part)  # Anexa o arquivo à mensagem

# Definição dos caminhos dos arquivos anexados (imagens geradas no 'main.py')
anexo_ibovespa = 'dataset/ibovespa.png'
anexo_dolar = 'dataset/dolar.png'
anexo_sp = 'dataset/sp500.png'

# Anexa os arquivos ao e-mail
anexar_arquivo(message, anexo_ibovespa)
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