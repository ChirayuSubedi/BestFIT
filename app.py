from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bestfit.db'
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure secret key
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

from routes import *
from models import User, Workout, MealPlan, FoodSuggestion

if __name__ == "__main__":
    app.run(debug=True)
