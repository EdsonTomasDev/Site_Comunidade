import flask_bcrypt
from flask import render_template, redirect, url_for, flash, request
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta, FormEditarPerfil
from comunidadeimpressionadora.models import Usuario
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image

lista_usuarios = ['Lira', 'João', 'Alon', 'Alessandra', 'Amanda']


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/contato")
def contato():
    return render_template("contato.html")


@app.route('/usuarios')
@login_required
def usuarios():
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criar_conta = FormCriarConta()


    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        #FILTRA O BANCO DE DADOS PELO EMAIL DIGITADO
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        #COMPARA USUARIO E SENHA
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login realizado com sucesso no e-mail {form_login.email.data}!', 'alert-success')
            #VERIFICAR SE EXISTE O PARÂMETRO NEXT PARA REDIRECIONAR A PÁGINA PARA ELE, EM CASO
            #DE O USUÁRIO TENHA SIDO REDIRECIONADO PARA A PÁGINA LOGIN POR ESTAR SEM LOGIN FEITO
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'falha do login, e-mail ou senha incorretos', 'alert-danger')

    if form_criar_conta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criar_conta.senha.data)
        usuario = Usuario(username=form_criar_conta.username.data, email=form_criar_conta.email.data, senha=senha_cript)
        database.session.add(usuario)
        database.session.commit()

        flash(f'Conta criada com sucesso com o e-mail {form_criar_conta.email.data}!', 'alert-success')
        return redirect(url_for('home'))

    return render_template('login.html', form_login=form_login, form_criar_conta=form_criar_conta)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash('Logout feito com sucesso', 'alert-success')
    return redirect(url_for('home'))


@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template("perfil.html", foto_perfil=foto_perfil)


@app.route('/post/criar')
@login_required
def criar_post():
    return render_template("criarpost.html")


#FUNÇÃO PARA PEGAR A IMAGEM, COMPACTAR E DAR UM NOME ALEATÓRIO PARA NÃO TER O MESMO NOME DE OUTRAS IMAGENS JÁ GRAVADAS
def salvar_imagem(imagem):
    #GERAR UM CÓDIGO ALEATÓRIO
    codigo = secrets.token_hex(8)
    #PEGAR O NOME E A EXTENSÃO DE ARQUIVO
    nome, extensao = os.path.splitext(imagem.filename)
    #ADICIONAR UM CÓDICO ALEATÓRIO NO NOME DA IMAGEM
    nome_arquivo = nome + codigo + extensao
    #DEFINE O CAMINHO PARA SALVAR A IMAGEM
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    # REDUZIR O TAMANHO DA IMAGEM
    tamanho_imagem = (200, 200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho_imagem)
    # SALVAR A IMAGEM NA PASTA FOTOS_PERFIL
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    #VALIDAR OS DADOS DO FORMULÁRIO AO CLICAR NO BOTÃO SUBMIT
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        #VERIFICA SE A FOTO FOI SELECIONADA
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        database.session.commit()
        flash('Perfil atualizado com sucesso!', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == "GET":
        form.email.data = current_user.email
        form.username.data = current_user.username
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template("editar_perfil.html", foto_perfil=foto_perfil, form=form)

