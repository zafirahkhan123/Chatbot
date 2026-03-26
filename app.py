from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------------- DATABASE MODEL ---------------- #

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

with app.app_context():
    db.create_all()

# ---------------- INDEX PAGE ---------------- #

@app.route('/')
def index():
    return render_template('index.html')

# ---------------- ABOUT PAGE ---------------- #

@app.route('/about')
def about():
    return render_template('about.html')

# ---------------- REGISTER ---------------- #

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # validations
        if not name or len(name.strip()) < 2:
            flash('Name must be at least 2 characters long.', 'error')
            return redirect(url_for('register'))

        if not email or '@' not in email:
            flash('Please enter a valid email address.', 'error')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('register'))

        # check existing user
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash('Email already registered.', 'error')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

        new_user = User(
            name=name.strip(),
            email=email.strip(),
            password=hashed_password
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))

        except Exception as e:
            db.session.rollback()
            flash('Registration error. Try again.', 'error')
            return redirect(url_for('register'))

    return render_template('register.html')


# ---------------- LOGIN ---------------- #

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            session['user_id'] = user.id
            session['user_name'] = user.name

            flash('Login successful!', 'success')

            return redirect(url_for('index'))

        else:
            flash('Invalid email or password.', 'error')

    return render_template('login.html')


# ---------------- RUN APP ---------------- #

if __name__ == '__main__':
    app.run(debug=True)