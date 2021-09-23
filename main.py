from flask import Flask, render_template, url_for, request, flash, redirect
from forms import FormCriarConta, FormLogin

app = Flask(__name__)

lista_usuarios = ['Lira', 'João', 'Alon', 'Alessandra', 'Amanda']

app.config['SECRET_KEY'] = '5336b6b697f499f30638b9316c574e3d'

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/contato")
def contato():
    return render_template("contato.html")


@app.route('/usuarios')
def usuarios():
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criar_conta = FormCriarConta()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        flash(f'Login realizado com sucesso no e-mail {form_login.email.data}!', 'alert-success')
        return redirect(url_for('home'))

    if form_criar_conta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        flash(f'Conta criada com sucesso com o e-mail {form_criar_conta.email.data}!', 'alert-success')
        return redirect(url_for('home'))

    return render_template('login.html', form_login=form_login, form_criar_conta=form_criar_conta )

if __name__ == '__main__':
    app.run(debug=True)
