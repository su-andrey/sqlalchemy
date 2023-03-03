from flask import jsonify
from flask_restful import abort, Resource

from data import db_session
from data.db_session import create_session
from data.users import User
from parser_ import parser


class UsersResource(Resource):
    def get(self, user_id):
        user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('surname', 'name', 'age', 'position', 'speciality', 'address',
                  'email'))})

    def delete(self, user_id):
        user_not_found(user_id)
        session = db_session.create_session()
        news = session.query(User).get(user_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, user_id):
        args = parser.parse_args()
        user_not_found(user_id)
        session = db_session.create_session()
        user = {'surname': args['surname'], 'name': args['name'], 'age': args['age'], 'position': args['position'],
                'speciality': args['speciality'], 'address': args['address'], 'email': args['email'],
                'city_from': args['city_from']}
        session.query(User).filter(User.id == user_id).update(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def post(self, user_id):
        args = parser.parse_args()
        session = db_session.create_session()
        if not session.query(User).filter(User.id == user_id).all():
            user = User()
            user.surname = args['surname']
            user.name = args['name']
            user.age = args['age']
            user.position = args['position']
            user.speciality = args['speciality']
            user.address = args['address']
            user.email = args['email']
            user.city_from = args['city_from']
            session.add(user)
            session.commit()
            return jsonify({'success': 'OK'})
        return jsonify({'error': 'this user is already exists'})


class UsersListResource(Resource):
    def get(self):
        session = create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('surname', 'name', 'age', 'position', 'speciality', 'address',
                  'email')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User()
        user.surname = args['surname']
        user.age = args['age']
        user.name = args['name']
        user.email = args['email']
        user.position = args['position']
        user.address = args['address']
        user.city_from = args['city_from']
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def delete(self, user_id):
        user_not_found(user_id)
        session = db_session.create_session()
        news = session.query(User).get(user_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})


def user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")
