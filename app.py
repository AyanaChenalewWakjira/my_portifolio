from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my-portfolio-secret-key-12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Admin User Model (UserMixin fayyadama)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(250), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 1. LOGIN ROUTE
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Nagaan dhuftan, Admin!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Username ykn Password dogoggora!', 'danger')
            
    return render_template('login.html')

# 2. DASHBOARD ROUTE (PROTECTED)
@app.route('/dashboard')
@login_required
def dashboard():
    projects = Project.query.all()
    messages = Message.query.all()
    return render_template('dashboard.html', projects=projects, messages=messages)

# 3. ADD PROJECT ROUTE
@app.route('/add_project', methods=['POST'])
@login_required
def add_project():
    title = request.form.get('title')
    description = request.form.get('description')
    tech_stack = request.form.get('tech_stack')
    github_link = request.form.get('github_link')
    live_demo = request.form.get('live_demo')

    new_project = Project(
        title=title, 
        description=description, 
        tech_stack=tech_stack, 
        github_link=github_link, 
        live_demo=live_demo
    )
    db.session.add(new_project)
    db.session.commit()
    flash("Pirojeektiin haaraan milkaa'inaan dabalameera!", 'success')
    return redirect(url_for('dashboard'))

# 4. LOGOUT ROUTE
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Keessaa baataniirtu.', 'info')
    return redirect(url_for('login'))


# --- DATABASE MODELS ---
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    tech_stack = db.Column(db.String(150), nullable=False)
    github_link = db.Column(db.String(200))
    live_demo = db.Column(db.String(200))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

# Otomaatikiin database.db uumuu
with app.app_context():
    db.create_all()

# --- ROUTES ---
@app.route('/')
def home():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)

@app.route('/contact', methods=['POST'])
def contact():
    if request.method == 'POST':
        # Data form irraa dhufe fuudhuu
        user_name = request.form.get('name')
        user_email = request.form.get('email')
        user_msg = request.form.get('message')
        
        # Database model 'Message' keessatti ol-kaa'uu
        new_message = Message(name=user_name, email=user_email, message=user_msg)
        db.session.add(new_message)
        db.session.commit()
        
        # Flash message ergaa milkaa'inaa agarsiisu erguu
        flash('Ergaa keetiif galatoomi! Dafeen si quunnama.', 'success')
        return redirect(url_for('home'))
    
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
