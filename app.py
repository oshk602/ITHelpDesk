from flask import Flask, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from extensions import db
from forms import RegisterForm, LoginForm, TicketForm
from sqlalchemy import or_

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

def seed_database():

    # Create users if none exist
    if User.query.count() == 0:

        users = [

            User(
                username='admin1',
                email='admin1@example.com',
                password=generate_password_hash('Password123'),
                role='admin'
            ),

            User(
                username='admin2',
                email='admin2@example.com',
                password=generate_password_hash('Password123'),
                role='admin'
            )

        ]

        for i in range(1, 9):

            users.append(
                User(
                    username=f'user{i}',
                    email=f'user{i}@example.com',
                    password=generate_password_hash('Password123'),
                    role='user'
                )
            )

        db.session.add_all(users)
        db.session.commit()

    # Create tickets if none exist
    if Ticket.query.count() == 0:

        users = User.query.all()

        sample_tickets = [

            Ticket(
                title='VPN Connection Issue',
                description='Unable to connect to company VPN.',
                status='Open',
                user_id=users[0].id
            ),

            Ticket(
                title='Printer Offline',
                description='Office printer not responding.',
                status='In Progress',
                user_id=users[1].id
            ),

            Ticket(
                title='Email Sync Problem',
                description='Emails not syncing on mobile device.',
                status='Resolved',
                user_id=users[2].id
            ),

            Ticket(
                title='Password Reset Request',
                description='Unable to access account.',
                status='Closed',
                user_id=users[3].id
            ),

            Ticket(
                title='Software Installation',
                description='Need Adobe Acrobat installed.',
                status='Open',
                user_id=users[4].id
            ),

            Ticket(
                title='Shared Drive Access',
                description='Cannot access network share.',
                status='In Progress',
                user_id=users[5].id
            ),

            Ticket(
                title='Laptop Running Slowly',
                description='Performance issues during startup.',
                status='Open',
                user_id=users[6].id
            ),

            Ticket(
                title='Monitor Not Detected',
                description='Second monitor not working.',
                status='Resolved',
                user_id=users[7].id
            ),

            Ticket(
                title='Account Locked',
                description='Too many login attempts.',
                status='Closed',
                user_id=users[8].id
            ),

            Ticket(
                title='Network Connectivity',
                description='Intermittent network connection.',
                status='Open',
                user_id=users[9].id
            )

        ]

        db.session.add_all(sample_tickets)
        db.session.commit()

# User loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():

    db.create_all()

    seed_database()


@app.route('/')
def home():

    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    return redirect(url_for('login'))

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

        flash(
            'Account created successfully. Please log in.',
            'success'
        )

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

            flash(
                'Login successful.',
                'success'
            )

            return redirect(url_for('dashboard'))
        
        flash("" \
        "Invalid username/email or password",
        'error'
        )
        

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
            status=form.status.data,
            user_id=current_user.id
        )

        db.session.add(ticket)
        db.session.commit()

        flash(
            'Ticket created successfully.',
            'success'
        )

        return redirect(url_for('tickets'))

    return render_template(
        'create_ticket.html',
        form=form
    )

@app.route('/tickets')
@login_required
def tickets():

    if current_user.role == 'admin':

        tickets = Ticket.query.all()

    else:

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
        ticket.status = form.status.data

        db.session.commit()

        flash(
            'Ticket updated successfully.',
            'success'
        )

        return redirect(url_for('tickets'))

    return render_template(
        'edit_ticket.html',
        form=form,
        ticket=ticket
    )

@app.route('/ticket/<int:ticket_id>/delete')
@login_required
def delete_ticket(ticket_id):

    ticket = Ticket.query.get_or_404(ticket_id)

    if current_user.role != 'admin':
        flash(
            'You do not have permission to delete tickets.',
            'error'
        )
        return redirect(url_for('tickets'))

    db.session.delete(ticket)
    db.session.commit()

    flash(
        'Ticket deleted successfully.',
        'success'
    )

    return redirect(url_for('tickets'))

@app.route('/admin/users')
@login_required
def manage_users():

    if current_user.role != 'admin':

        flash(
            'You do not have permission to access this page.',
            'error'
        )

        return redirect(url_for('dashboard'))

    users = User.query.all()

    return render_template(
        'manage_users.html',
        users=users
    )

@app.route('/admin/user/<int:user_id>/toggle-role')
@login_required
def toggle_role(user_id):

    if current_user.role != 'admin':

        flash(
            'You do not have permission.',
            'error'
        )

        return redirect(url_for('dashboard'))

    user = User.query.get_or_404(user_id)

    if user.role == 'admin':
        user.role = 'user'
    else:
        user.role = 'admin'

    db.session.commit()

    flash(
        'User role updated.',
        'success'
    )

    return redirect(url_for('manage_users'))

# Logout route
@app.route('/logout')
@login_required
def logout():

    logout_user()

    flash(
        'You have been logged out.',
        'info'
    )

    return redirect(url_for('login'))

# Run server
if __name__ == '__main__':
    app.run(debug=True)