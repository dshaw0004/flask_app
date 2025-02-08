import os
from flask import Flask, render_template
# from blueprint.catpics.catpics import catpics
# from blueprint.quotes.quotes import quote_app
# from blueprint.goldprice.goldprice import goldprice_app
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://dshaw0004:planksconstant@dshaw0004.mysql.pythonanywhere-services.com/dshaw0004$default'
db_password = os.environ.get('MYSQL_DB_PASSWORD')
db_uri = f'mysql+mysqldb://dshaw0004:{db_password}@dshaw0004.mysql.pythonanywhere-services.com/dshaw0004$default'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.secret_key = os.environ['FLASK_APPLICATION_SECRET_KEY']
# app.secret_key = 'FLASK_APPLICATION_SECRET_KEY'
#
# app.register_blueprint(catpics, url_prefix='/catpics')
# app.register_blueprint(quote_app, url_prefix='/quote')
# app.register_blueprint(goldprice_app, url_prefix='/goldprice')
