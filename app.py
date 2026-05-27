from flask import Flask, render_template, redirect, url_for
from werkzeug.security import generate_password_hash

from extensions import db
from forms import RegisterForm

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

@app.route('/')
def home():
    return "Flask is working!"

@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        hashed_password = generate_password_hash(
            form.password.data
        )

        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template(
        'register.html',
        form=form
    )

# Run server
if __name__ == '__main__':
    app.run(debug=True)