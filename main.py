from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<p>Olá tá tudo funcionando bem! Tô sabendo muito!</p>"

@app.route("/contato")
def contato():
    return "okQualquer dúvida entre em contato conosco pelo e-mail contato@contato.com"

if __name__ == '__main__':
    app.run(debug=True)
