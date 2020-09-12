import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

#Configuration setup
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:EmmanueL1@localhost/sccl_master"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# UPLOAD_FOLDER = os.path.join(os.getcwd(), "text_files")
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0



#Linking and registering the database
db = SQLAlchemy(app)
Migrate(app,db)

#Blueprint registration
from project.rules_engine.views import rules_blueprint
app.register_blueprint(rules_blueprint,url_prefix='/rules')
