from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_bcrypt import Bcrypt

load_dotenv()

metadata=MetaData()
db=SQLAlchemy(metadata=metadata)
migrate=Migrate()

bcrypt=Bcrypt()

def config_app(app):
    app.config.from_prefixed_env()
    db.init_app(app)
    migrate.init_app(app,db)
    bcrypt.init_app(app)