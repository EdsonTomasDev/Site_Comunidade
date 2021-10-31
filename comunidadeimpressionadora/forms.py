#Biblioteca que formata formulários
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from comunidadeimpressionadora.models import Usuario
from flask_login import current_user


class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()], render_kw={"placeholder": "Digite seu E-mail"})
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao = PasswordField('Confirmação da senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

#Esta função verifica se já existe usuário com este e-mail cadastrado no banco de dados
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login para continuar ')



class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar dados de acesso')
    botao_submit_login = SubmitField('Fazer Login')


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()], render_kw={"placeholder": "Digite seu E-mail"})
    botao_submit_editarperfil = SubmitField('Editar Perfil')
    #VARIÁVEL QUE IRÁ RECEBER A IMAGEM PARA GRAVAR COMO FOTO DE PERFIL DO USUÁRIO
    foto_perfil = FileField('Atualizar Foto de Perfil', validators=[FileAllowed(['jpg', 'png'], 'Somente é permitido arquivos com extensão jpg e png')])

    curso_excel = BooleanField('Excel impressionador')
    curso_vba = BooleanField('VBA impressionador')
    curso_powerbi = BooleanField('Power BI impressionador')
    curso_python = BooleanField('Python impressionador')
    curso_ppt = BooleanField('Apresentações impressionadoras')
    curso_sql = BooleanField('SQL impressionador')

    # Esta função verifica se já existe usuário com este e-mail cadastrado no banco de dados
    def validate_email(self, email):
        #VERIFICAR SE O CARA MUDOU DE E-MAIL
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail!')


class FormCriarPost(FlaskForm):
    titulo = StringField('Título do Post', validators=[DataRequired(),Length(2, 140)])
    corpo = TextAreaField('Escreva seu Post aqui', validators=[DataRequired()])
    botao_submit = SubmitField('Criar Post')

