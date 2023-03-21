from flask import jsonify
from flask_restful import abort, Resource
from data import db_session
from data.users import User
from parser_ import parser


class UsersResource(Resource):
    def get(self, user_id):
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        if user:
            return jsonify({'user': user.to_dict(
                only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address',
                      'email'))})
        else:
            return abort(404, message=f"User {user_id} not found")

    def delete(self, user_id):
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        if user:
            session.delete(user)
            session.commit()
            return jsonify({'success': 'OK'})
        else:
            return abort(404, message=f"User {user_id} not found")

    def post(self, user_id):
        args = parser.parse_args()
        session = db_session.create_session()
        tex = session.query(User).get(user_id)
        if not tex:
            return abort(404, message=f"User {user_id} not found")
        user = {'surname': args['surname'], 'name': args['name'], 'age': args['age'], 'position': args['position'],
                'speciality': args['speciality'], 'address': args['address'], 'email': args['email'],
                'city_from': args['city_from']}
        session.query(User).filter(User.id == user_id).update(user)
        session.commit()
        return jsonify({'success': f'{user_id} updated'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address',
                  'email')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
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
        #a = session.query(User).order_by(User.id.desc()).first().id
        return jsonify({'success': f'{user.id} added'})

