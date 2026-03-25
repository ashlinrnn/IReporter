from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

load_dotenv()

metadata=MetaData()
db=SQLAlchemy(metadata=metadata)
migrate=Migrate()

def config_app(app):
    app.config.from_prefixed_env()
    db.init_app(app)
    migrate.init_app(app,db)