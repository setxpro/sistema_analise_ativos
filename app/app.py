from flask import Flask
from flask import render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=["GET"])
def home():
  return render_template('index.html', mensagem="")

@app.route('/', methods=["POST"])
def sendReport():
  if request.method == "POST":
    form = request.form
    dataInicial = form["dataInicial"]
    dataFinal = form["dataFinal"]
    email = form["email"]

    return render_template('index.html', mensagem="Relatório enviado com sucesso!")


if __name__ == '__main__':
    app.run(debug=True)
