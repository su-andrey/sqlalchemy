import flask

import sqlalchemy.exc
from data import db_session
from data.users import User
from flask import request

blueprint = flask.Blueprint(
    'user_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users', methods=['GET'])
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return flask.jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email'))
                 for item in users]
        }
    )


@blueprint.route('/api/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).one()
    if not user:
        return flask.jsonify({'error': 'Not found'})
    return flask.jsonify(
        {
            'users':
                [user.to_dict(only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email'))]
        }
    )


@blueprint.route('/api/user/<int:user_id>', methods=['GET'])
def add_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).one()
    if not user:
        return flask.jsonify({'error': 'Not found'})
    return flask.jsonify(
        {
            'users':
                [user.to_dict(only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email'))]
        }
    )


@blueprint.route('/api/adduser', methods=['POST'])
def create_user():
    if not request.json:
        return flask.jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['surname', 'name', 'age', 'position', 'speciality', 'email', 'id']):
        return flask.jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    try:
        if not db_sess.query(User).filter(User.id == request.json['id']).all():
            user = User()
            user.name = request.json['name']
            user.surname = request.json['surname']
            user.age = request.json['age']
            user.position = request.json['position']
            user.speciality = request.json['speciality']
            user.email = request.json['email']
            db_sess.add(user)
            db_sess.commit()
            return flask.jsonify({'success': 'OK'})
    except sqlalchemy.exc.IntegrityError:
        return flask.jsonify({'error': 'bad data', 'id': 'tis field was already used'})
    except Exception:
        return flask.jsonify({'error': 'bad data', 'id': 'already exists'})


@blueprint.route('/api/deleteuser/<int:user_id>', methods=['DELETE'])
def deleteuser(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return flask.jsonify({'error': 'Not found'})
    db_sess.delete(user)
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})




@blueprint.route('/api/edituser/<int:user_id>', methods=['POST'])
def edit_work(user_id):
    db_sess = db_session.create_session()
    try:
        user = db_sess.query(User).filter(User.id == user_id).one()
    except sqlalchemy.exc.NoResultFound:
        return flask.jsonify({'error': 'bad id or something else'})
    if not user:
        return flask.jsonify({'error': 'Not found'})
    try:
        user.name = request.json['name']
        user.surname = request.json['surname']
        user.age = int(request.json['age'])
        user.speciality = request.json['speciality']
        user.position = request.json['position']
        user.email = request.json['email']
        user.address = request.json['address']
        db_sess.add(user)
        db_sess.commit()
        return flask.jsonify({'success': 'OK'})
    except KeyError:
        return flask.jsonify({'Error': 'KeyError'})
    except ValueError:
        return flask.jsonify({'Error': 'ValueError'})