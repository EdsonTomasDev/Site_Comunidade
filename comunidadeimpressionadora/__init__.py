from flask import Flask
#Banco de dados: pip install flask-sqlalchemy
from flask_sqlalchemy import SQLAlchemy
#pip install flask-bcrypt
from flask_bcrypt import Bcrypt
#pip install flask-login
from flask_login import LoginManager




app = Flask(__name__)



app.config['SECRET_KEY'] = '5336b6b697f499f30638b9316c574e3d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


from comunidadeimpressionadora import routes

