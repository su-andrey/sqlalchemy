import flask_login
from flask import Flask, request
from flask import redirect, render_template
from flask_login import LoginManager
from flask_login import login_user, login_required, logout_user
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField
from wtforms.validators import DataRequired

from data import db_session
from data.jobs import Jobs
from data.users import User

db_session.global_init("db/blogs.db")
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("db/blogs.db")
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class AddForm(FlaskForm):
    job = StringField('Название работы', validators=[DataRequired()])
    team_leader = StringField('Id лидера', validators=[DataRequired()])
    work_size = StringField('Размер работы в часах', validators=[DataRequired()])
    start_date = StringField('Время начала', validators=[DataRequired()])
    end_date = StringField('Время окончания', validators=[DataRequired()])
    collaborations = StringField('Список работников через запятую', validators=[DataRequired()])
    is_finished = BooleanField('Работа окончена')
    submit = SubmitField('Готово')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and check_password_hash(user.check_password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/')
@login_required
def main():
    db_sess = db_session.create_session()
    profs = [job for job in db_sess.query(Jobs)]
    return render_template('jobs.html', profs=profs)


class Authorize(FlaskForm):
    enter = SubmitField('Войти')
    sign_up = SubmitField('Зарегестрироваться')


@app.route('/authorize', methods=['GET', 'POST'])
def authorize():
    form = Authorize()
    if request.method == 'POST':
        try:
            if request.form['enter']:
                return redirect('/login')
        except Exception:
            return redirect('/register')
    elif request.method == 'GET':
        return render_template('authorize.html', form=form)


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    age = StringField('Возраст', validators=[DataRequired()])
    position = StringField('Позиция', validators=[DataRequired()])
    speciality = StringField('Специальность', validators=[DataRequired()])
    address = StringField('Адресс', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        adress = db_sess.query(User).filter(User.email == form.email.data).first()
        if not adress:
            user = User()
            user.email = form.email.data
            user.age = form.age.data
            user.surname = form.surname.data
            user.name = form.name.data
            user.speciality = form.speciality.data
            user.position = form.position.data
            user.check_password = generate_password_hash(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            return redirect('/login')
    return render_template('register.html', form=form)


@app.route('/addjob', methods=['GET', 'POST'])
def addjob():
    form = AddForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        job.job = form.job.data
        job.team_leader = form.team_leader.data
        job.work_size = form.work_size.data
        job.start_date = form.start_date.data
        job.end_date = form.end_date.data
        job.collaborators = form.collaborations.data
        job.is_finished = form.is_finished.data
        db_sess.add(job)
        db_sess.commit()
        return redirect("/")
    return render_template('job.html', form=form)


@app.route('/editjob', methods=['GET', 'POST'])
def editjob():
    form = AddForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Jobs).filter(Jobs.job == form.job.data):
            if flask_login.current_user.id == '1' or form.team_leader.data == str(flask_login.current_user.id):
                tex = db_sess.query(Jobs).filter(Jobs.job == form.job.data)
                tex[0].team_leader = form.team_leader.data
                tex[0].job = form.job.data
                tex[0].work_size = form.work_size.data
                tex[0].end_date = form.end_date.data
                tex[0].start_date = form.start_date.data
                tex[0].is_finished = form.is_finished.data
                tex[0].collaborations = form.collaborations.data
                db_sess.commit()
        return redirect("/")
    return render_template('job.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
