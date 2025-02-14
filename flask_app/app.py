import os, json
from flask import Flask, render_template
# from blueprint.catpics.catpics import catpics
# from blueprint.quotes.quotes import quote_app
# from blueprint.goldprice.goldprice import goldprice_app
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
envs = dict()
CWD = app.root_path
with open(f'{CWD}/env.json') as file:
    envs = json.load(file)

db_password = envs.get('MYSQL_DB_PASSWORD')
# db_uri = f'mysql+mysqldb://dshaw0004:{db_password}@dshaw0004.mysql.pythonanywhere-services.com/dshaw0004$default'
db_uri = 'sqlite:///test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config["SQLALCHEMY_POOL_RECYCLE"] = 7069
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.secret_key = envs.get('FLASK_APPLICATION_SECRET_KEY')
# app.secret_key = 'FLASK_APPLICATION_SECRET_KEY'
#
# app.register_blueprint(catpics, url_prefix='/catpics')
# app.register_blueprint(quote_app, url_prefix='/quote')
# app.register_blueprint(goldprice_app, url_prefix='/goldprice')
