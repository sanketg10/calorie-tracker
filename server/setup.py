from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/sanket'
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})
