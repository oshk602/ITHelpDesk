from flask import Flask
from extensions import db

# Create Flask app
app = Flask(__name__)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretkey123'

# Connect database to app
db.init_app(app)

# Import models AFTER db setup
from models import User, Ticket

# Create tables
with app.app_context():
    db.create_all()

# Test route
@app.route('/')
def home():
    return "Flask is working!"

# Run server
if __name__ == '__main__':
    app.run(debug=True)