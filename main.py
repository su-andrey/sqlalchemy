import requests
from flask import Flask, request
from flask import redirect, render_template
from flask_login import LoginManager
from flask_login import login_user, login_required, logout_user
from flask_restful import Api
from flask_wtf import FlaskForm
from requests import get
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField, DateField
from wtforms.validators import DataRequired

import jobs_resource
import users_resource
from data import db_session
from data.jobs import Jobs
from data.users import User

db_session.global_init("db/blogs.db")
app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("db/blogs.db")
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/blogs.db")
api.add_resource(users_resource.UsersListResource, '/api/v2/users')
api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:user_id>')
api.add_resource(jobs_resource.JobsListResource, '/api/v2/jobs')
api.add_resource(jobs_resource.JobResource, '/api/v2/jobs/<int:job_id>')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class AddForm(FlaskForm):
    job = StringField('Название работы', validators=[DataRequired()])
    team_leader = StringField('Id лидера', validators=[DataRequired()])
    work_size = StringField('Размер работы в часах', validators=[DataRequired()])
    start_date = DateField('Дата начала', validators=[DataRequired()])
    end_date = DateField('Дата окончания', validators=[DataRequired()])
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
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_repeat = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    age = StringField('Возраст', validators=[DataRequired()])
    position = StringField('Позиция', validators=[DataRequired()])
    speciality = StringField('Специальность', validators=[DataRequired()])
    address = StringField('Адресс', validators=[DataRequired()])
    submit = SubmitField('Войти')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        adress = db_sess.query(User).filter(User.email == form.email.data).first()
        if not adress and form.password.data == form.password_repeat.data:
            user = User()
            user.email = form.email.data
            user.age = form.age.data
            user.surname = form.surname.data
            user.name = form.name.data
            user.speciality = form.speciality.data
            user.position = form.position.data
            user.address = form.address.data
            user.check_password = generate_password_hash(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            return redirect('/login')
    return render_template('register.html', form=form)


@app.route('/addjob', methods=['GET', 'POST'])
@login_required
def addjob():
    form = AddForm()
    try:
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            job = Jobs()
            job.job = form.job.data
            job.team_leader = int(form.team_leader.data)
            job.work_size = int(form.work_size.data)
            job.start_date = form.start_date.data
            job.end_date = form.end_date.data
            job.collaborators = form.collaborations.data
            job.is_finished = form.is_finished.data
            db_sess.add(job)
            db_sess.commit()
            return redirect("/")
    except:
        return redirect('/addjob')
    return render_template('job.html', form=form)


@app.route('/editjob/<jobname>', methods=['GET', 'POST'])
@login_required
def editjob(jobname):
    form = AddForm()
    form.job.data = jobname
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        tex = db_sess.query(Jobs).filter(Jobs.job == jobname)
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


class DeleteJob(FlaskForm):
    name = StringField('Введите название работы для удаления', validators=[DataRequired()])
    delete = SubmitField('Удалить')


@app.route('/deletejob/<jobname>', methods=['GET', 'POST'])
@login_required
def delete_job(jobname):
    db_sess = db_session.create_session()
    i = db_sess.query(Jobs).filter(Jobs.job == jobname).one()
    db_sess.delete(i)
    db_sess.commit()
    return redirect("/")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/user_show/<id>', methods=['GET'])
def user_show(id):
    info = get(f'http://localhost:5000/api/user/{id}').json()["users"][0]
    city, name = info['city_from'], f'{info["name"]} {info["surname"]}'
    myau = 'https://geocode-maps.yandex.ru/1.x'
    mur = requests.get(myau, params={'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
                                     'geocode': city, 'format': 'json'})

    # Преобразуем ответ в json-объект
    json_response = mur.json()
    # Получаем первый топоним из ответа геокодера.
    # Согласно описанию ответа, он находится по следующему пути:
    toponym = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
    toponym = toponym.replace(' ', ',')
    map_request = "https://static-maps.yandex.ru/1.x"
    response = requests.get(map_request, params={'ll': toponym, 'z': 11, 'l': 'sat'})
    # Запишем полученное изображение в файл.
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    param = {}
    param['place'], param['name'], param['src'] = city, name, 'map.png'
    print('Success')
    return render_template('nostalgy.html', **param)


app.run()
