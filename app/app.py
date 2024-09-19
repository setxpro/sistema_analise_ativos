from flask import Flask
from flask import render_template, request

from utils.format_date import format_date, calcular_intervalo
from get_dataset import createDataset
from spark import analyze_market_data

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

        # Create DATASET
        createDataset(dataInicial, dataFinal)

        total_time = calcular_intervalo(dataInicial, dataFinal)

        analyze_market_data(email, total_time)

        return render_template('index.html', mensagem="Relatório enviado com sucesso!")


if __name__ == '__main__':
    app.run(debug=True)
