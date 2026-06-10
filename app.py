from flask import Flask, render_template, redirect, url_for, flash
from sqlalchemy import or_
from werkzeug.security import generate_password_hash

from extensions import db
from forms import RegisterForm, TicketForm, LoginForm
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

# Create Flask app
app = Flask(__name__)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretkey123'

# Connect database to app
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'

# Import models AFTER db setup
from models import User, Ticket

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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

@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()

        if user and check_password_hash(
            user.password,
            form.password.data
        ):

            login_user(user)

            return redirect(url_for('dashboard'))

    return render_template(
        'login.html',
        form=form
    )

from flask import Flask, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from extensions import db
from forms import RegisterForm, LoginForm

# Create app
app = Flask(__name__)

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretkey123'

# Initialize database
db.init_app(app)

# Login manager
login_manager = LoginManager()
login_manager.init_app(app)

# Redirect if not logged in
login_manager.login_view = 'login'

# Import models
from models import User, Ticket

# User loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create tables
with app.app_context():
    db.create_all()

# Home route
@app.route('/')
def home():

    if current_user.is_authenticated:
        return f"Hello {current_user.username}"

    return "Flask is working!"

# Register route
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

        return redirect(url_for('login'))

    return render_template(
        'register.html',
        form=form
    )

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter(
            or_(
                User.email == form.identifier.data,
                User.username == form.identifier.data
            )
        ).first()

        if user and check_password_hash(
            user.password,
            form.password.data
        ):

            login_user(user)

            return redirect(url_for('dashboard'))
        
        flash("Invalid username/email or password")
        

    return render_template(
        'login.html',
        form=form
    )

# Dashboard route
@app.route('/dashboard')
@login_required
def dashboard():

    return render_template(
        'dashboard.html',
        user=current_user
    )

@app.route('/create-ticket', methods=['GET', 'POST'])
@login_required
def create_ticket():

    form = TicketForm()

    if form.validate_on_submit():

        ticket = Ticket(
            title=form.title.data,
            description=form.description.data,
            user_id=current_user.id
        )

        db.session.add(ticket)
        db.session.commit()

        return redirect(url_for('tickets'))

    return render_template(
        'create_ticket.html',
        form=form
    )

@app.route('/tickets')
@login_required
def tickets():

    tickets = Ticket.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        'tickets.html',
        tickets=tickets
    )

@app.route('/ticket/<int:ticket_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_ticket(ticket_id):

    ticket = Ticket.query.get_or_404(ticket_id)

    # Prevent users editing other users' tickets
    if ticket.user_id != current_user.id:
        return redirect(url_for('tickets'))

    form = TicketForm(obj=ticket)

    if form.validate_on_submit():

        ticket.title = form.title.data
        ticket.description = form.description.data

        db.session.commit()

        return redirect(url_for('tickets'))

    return render_template(
        'edit_ticket.html',
        form=form,
        ticket=ticket
    )

# Logout route
@app.route('/logout')
@login_required
def logout():

    logout_user()

    return redirect(url_for('login'))

# Run server
if __name__ == '__main__':
    app.run(debug=True)