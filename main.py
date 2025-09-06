from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Banco de dados em memória
transacoes = []
contador_id = 1


@app.route("/")
def home():
    receitas = sum(t["valor"] for t in transacoes if t["tipo"] == "receita")
    despesas = sum(t["valor"] for t in transacoes if t["tipo"] == "despesa")
    saldo = receitas - despesas
    return render_template(
        "index.html",
        transacoes=transacoes,
        receitas=receitas,
        despesas=despesas,
        saldo=saldo
    )


@app.route("/adicionar", methods=["POST"])
def adicionar():
    global contador_id
    tipo = request.form["tipo"]
    descricao = request.form["descricao"]
    valor = float(request.form["valor"])
    categoria = request.form["categoria"]

    nova_transacao = {
        "id": contador_id,
        "tipo": tipo,
        "descricao": descricao,
        "valor": valor,
        "categoria": categoria,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }

    transacoes.append(nova_transacao)
    contador_id += 1

    return redirect(url_for("home"))


@app.route("/deletar/<int:id>")
def deletar(id):
    global transacoes
    transacoes = [t for t in transacoes if t["id"] != id]
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)


