from flask import Flask, render_template, Response, url_for, redirect
from camera import Video
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    print(user_id)
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    number = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def get_id(self):
           return (self.number)

class Performance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, db.ForeignKey('user.number'), nullable=False)
    micorsleep = db.Column(db.Integer, nullable=False)
    yawning = db.Column(db.Integer, nullable=False)
    neutral = db.Column(db.Integer, nullable=False)

class RegisterForm(FlaskForm):
    number = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Student Number"})
    name = StringField(validators=[InputRequired(), Length(min=1, max=50)], render_kw={"placeholder": "Name"})
    surname = StringField(validators=[InputRequired(), Length(min=1, max=50)], render_kw={"placeholder": "Surname"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Register')

    def validate_username(self, number):
        existing_user = User.query.filter_by(number=number.data).first()
        if existing_user:
            raise ValidationError('That username already exists. Please choose a different one.')
        
class LoginForm(FlaskForm):
    number = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Student Number"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(number=form.number.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))

    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('index.html', user=current_user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(number=form.number.data, name=form.name.data, surname=form.surname.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
       b'Content-Type:  image/jpeg\r\n\r\n' + frame +
         b'\r\n\r\n')

@app.route('/video')
def video():
    return Response(gen(Video()), mimetype='multipart/x-mixed-replace; boundary=frame')

app.run(debug=True)