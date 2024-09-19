from datetime import datetime
from dateutil.relativedelta import relativedelta


def format_date(date_str):
    # Converte a data de 'DD/MM/YYYY' para 'YYYY-MM-DD'
    formatted_date = datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
    return formatted_date


def calcular_intervalo(ini_date_str, end_date_str):
    # Converter as strings de data para objetos datetime
    ini_date = datetime.strptime(ini_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    # Usar relativedelta para calcular a diferença entre as datas
    intervalo = relativedelta(end_date, ini_date)

    return f"{intervalo.years} anos, {intervalo.months} meses, e {intervalo.days} dias"
