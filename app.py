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

# ---------------------------------------------------------------------------
# 1. DATABASE MODELS (Duraan durse define ta'uu qabu)
# ---------------------------------------------------------------------------

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(250), nullable=False)

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


# ---------------------------------------------------------------------------
# 2. FLASK-LOGIN CONFIGURATION
# ---------------------------------------------------------------------------

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
   #login_manager.login_message = 'Gara Dashboard seenuuf mee jalqaba login godhaa.'
    #login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    # SQLAlchemy 2.0 Modern & Safe loader
    return db.session.get(User, int(user_id))


# ---------------------------------------------------------------------------
# 3. INITIALIZE DATABASE & CREATE DEFAULT ADMIN USER
# ---------------------------------------------------------------------------

with app.app_context():
    db.create_all()
    # Default Admin User 'ayana' uumuu (yoo database keessa hin jire ta'e)
    if not User.query.filter_by(username='ayana').first():
        hashed_password = generate_password_hash('password123', method='scrypt')
        admin_user = User(username='ayana', password_hash=hashed_password)
        db.session.add(admin_user)
        db.session.commit()


# ---------------------------------------------------------------------------
# 4. APPLICATION ROUTES
# ---------------------------------------------------------------------------

@app.route('/')
def home():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)



@app.route('/login', methods=['GET', 'POST'])
def login():
    # 1. Yoo duraan login ta'aniiru ta'e qofa gara dashboard geessi
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    # 2. Form Submission (Yeroo Sign In dhiiban)
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Username ykn Password dogoggora!', 'danger')
            return redirect(url_for('login'))
            
    # 3. Form GET Request (Fuula login.html kallattiin banuu)
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    # Yoo user-n login hin taane, message ergiiti KALLATTIN gara /login geessi
    if not current_user.is_authenticated:
        flash('Gara Dashboard seenuuf dura maaloo login godhaa.', 'info')
        return redirect(url_for('login'))
        
    projects = Project.query.all()
    messages = Message.query.all()
    return render_template('dashboard.html', projects=projects, messages=messages)


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

@app.route('/contact', methods=['POST'])
def contact():
    if request.method == 'POST':
        user_name = request.form.get('name')
        user_email = request.form.get('email')
        user_msg = request.form.get('message')
        
        new_message = Message(name=user_name, email=user_email, message=user_msg)
        db.session.add(new_message)
        db.session.commit()
        
        flash('Ergaa keetiif galatoomi! Dafeen si quunnama.', 'success')
        return redirect(url_for('home'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Keessaa baataniirtu.', 'info')
    return redirect(url_for('login'))


# 1. PROJECT UPDATE ROUTE
@app.route('/edit_project/<int:id>', methods=['POST'])
@login_required
def edit_project(id):
    project = db.session.get(Project, id)
    if project:
        project.title = request.form.get('title')
        project.description = request.form.get('description')
        project.tech_stack = request.form.get('tech_stack')
        project.github_link = request.form.get('github_link')
        project.live_demo = request.form.get('live_demo')
        
        db.session.commit()
        flash("Pirojeektiin milkaa'inaan fooyya'eera!", 'success')
    else:
        flash('Pirojeektiin hin argamne!', 'danger')
        
    return redirect(url_for('dashboard'))


# 2. PROJECT DELETE ROUTE
@app.route('/delete_project/<int:id>', methods=['POST', 'GET'])
@login_required
def delete_project(id):
    project = db.session.get(Project, id)
    if project:
        db.session.delete(project)
        db.session.commit()
        flash("Pirojeektiin milkaa'inaan haqameera!", 'success')
    else:
        flash('Pirojeektiin hin argamne!', 'danger')
        
    return redirect(url_for('dashboard'))
# ---------------------------------------------------------------------------
# 5. SERVER ENTRYPOINT
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)