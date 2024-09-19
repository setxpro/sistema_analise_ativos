from datetime import datetime


def format_date(date_str):
    # Converte a data de 'DD/MM/YYYY' para 'YYYY-MM-DD'
    formatted_date = datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
    return formatted_date
