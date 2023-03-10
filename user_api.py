import datetime

import flask
import sqlalchemy.exc
from flask import request

from data import db_session
from data.users import User

blueprint = flask.Blueprint(
    'user_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users', methods=['GET'])
def get_user():
    db_sess = db_session.create_session()
    news = db_sess.query(User).all()
    return flask.jsonify(
        {
            'users':
                [item.to_dict(only=('surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'city_from')
                              ) for item in news]
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def add_user():
    if not request.json:
        return flask.jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['name', 'surname', 'age', 'position', 'speciality', 'address', 'email', 'city_from']):
        return flask.jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    user = User()
    user.name = request.json['name']
    user.surname = request.json['surname']
    user.age = request.json['age']
    user.modified_date = datetime.datetime.now()
    user.speciality = request.json['speciality']
    user.address = request.json['address']
    user.email = request.json['email']
    user.city_from = request.json['city_from']
    db_sess.add(user)
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return flask.jsonify({'error': 'Not found'})
    return flask.jsonify(
        {
            'user': user.to_dict(
                only=('surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'city_from'))
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['POST'])
def edituser(user_id):
    db_sess = db_session.create_session()
    try:
        user = db_sess.query(User).get(user_id)
    except sqlalchemy.exc.NoResultFound:
        return flask.jsonify({'error': 'bad id or something else'})
    if not user:
        return flask.jsonify({'error': 'Not found'})
    try:
        user.name = request.json['name']
        user.surname = request.json['surname']
        user.age = request.json['age']
        user.modified_date = datetime.datetime.now()
        user.speciality = request.json['speciality']
        user.address = request.json['address']
        user.email = request.json['email']
        user.city_from = request.json['city_from']
        db_sess.add(user)
        db_sess.commit()
        return flask.jsonify({'success': 'OK'})
    except KeyError:
        return flask.jsonify({'Error': 'KeyError'})
    except ValueError:
        return flask.jsonify({'Error': 'ValueError'})


@blueprint.route('/api/users/<int:users_id>', methods=['DELETE'])
def delete_user(users_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(users_id)
    if not user:
        return flask.jsonify({'error': 'Not found'})
    db_sess.delete(user)
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})
