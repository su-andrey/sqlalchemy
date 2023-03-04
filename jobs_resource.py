from flask import jsonify
from flask_restful import abort, Resource

from data import db_session
from data.jobs import Jobs
from job_parser import parser


class JobResource(Resource):
    def get(self, job_id):
        user_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        return jsonify({'user': job.to_dict(
            only=('id', 'team_leader', 'work_size', 'collaborators', 'start_date', 'end_date',
                  'is_finished'))})

    def delete(self, job_id):
        user_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, job_id):
        args = parser.parse_args()
        user_not_found(job_id)
        session = db_session.create_session()
        job = {'team_leader': args['team_leader'], 'job': args['job'], 'work_size': args['work_size'],
               'collaborators': args['collaborators'],
               'start_date': args['start_date'], 'end_date': args['end_date'], 'is_finished': args['is_finished']}
        session.query(Jobs).filter(Jobs.id == job_id).update(job)
        session.commit()
        return jsonify({'success': 'OK'})

    def post(self, job_id):
        args = parser.parse_args()
        session = db_session.create_session()
        if not session.query(Jobs).filter(Jobs.id == job_id).all():
            job = Jobs()
            job.job = args['job']
            job.team_leader = args['team_leader']
            job.work_size = args['work_size']
            job.collaborators = args['collaborators']
            job.start_date = args['start_date']
            job.end_date = args['end_date']
            job.is_finished = args['is_finished']
            session.add(job)
            session.commit()
            return jsonify({'success': 'OK'})
        return jsonify({'error': 'this job is already exists'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'users': [item.to_dict(
            only=('job', 'team_leader', 'collaborators', 'start_date', 'end_date', 'is_finished')) for item in jobs]})

    def post(self, job_id):
        args = parser.parse_args()
        session = db_session.create_session()
        if not session.query(Jobs).filter(Jobs.id == job_id).all():
            job = Jobs()
            job.job = args['job']
            job.team_leader = args['team_leader']
            job.work_size = args['work_size']
            job.collaborators = args['collaborators']
            job.start_date = args['start_date']
            job.end_date = args['end_date']
            job.is_finished = args['is_finished']
            session.add(job)
            session.commit()
            return jsonify({'success': 'OK'})
        return jsonify({'error': 'this job is already exists'})

    def delete(self, job_id):
        user_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})


def user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(Jobs).get(user_id)
    if not user:
        abort(404, message=f"Job {user_id} not found")
