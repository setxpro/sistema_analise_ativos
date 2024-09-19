from flask import Flask
from flask import render_template, request, redirect, url_for

from utils.format_date import format_date
from get_dataset import createDataset
from main import analyze_market_data
import time

app = Flask(__name__)


@app.route('/', methods=["GET"])
def home():
    return render_template('index.html', mensagem="")


@app.route('/', methods=["POST"])
def sendReport():
    if request.method == "POST":
        form = request.form
        dataInicial = format_date(form["dataInicial"])
        dataFinal = format_date(form["dataFinal"])
        email = form["email"]

        print(dataInicial)
        print(dataFinal)

        # Create DATASET
        createDataset(dataInicial, dataFinal)

        # Adiciona um atraso de 5 segundos
        time.sleep(5)
        print(email)

        analyze_market_data(email)

        return render_template('index.html', mensagem="Relatório enviado com sucesso!")


if __name__ == '__main__':
    app.run(debug=True)
