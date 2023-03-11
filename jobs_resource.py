from flask import jsonify
from flask_restful import abort, Resource

from data import db_session
from data.jobs import Jobs
from job_parser import parser


class JobResource(Resource):
    def get(self, job_id):
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        if job:
            return jsonify({'job': job.to_dict(
                only=('id', 'team_leader', 'work_size', 'collaborators', 'start_date', 'end_date',
                      'is_finished'))})
        else:
            return abort(404, message=f"User {job_id} not found")

    def delete(self, job_id):
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        if job:
            session.delete(job)
            session.commit()
            return jsonify({'success': f'{job_id} deleted'})
        else:
            return abort(404, message=f"Job {job_id} not found")

    def post(self, job_id):
        args = parser.parse_args()
        session = db_session.create_session()
        tex = session.query(Jobs).get(job_id)
        if not tex:
            return abort(404, message=f"Job {job_id} not found")
        job = {'team_leader': args['team_leader'], 'job': args['job'], 'work_size': args['work_size'],
               'collaborators': args['collaborators'],
               'start_date': args['start_date'], 'end_date': args['end_date'], 'is_finished': args['is_finished']}
        session.query(Jobs).filter(Jobs.id == job_id).update(job)
        session.commit()
        return jsonify({'success': f'{job_id} field updated'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict(
            only=('job', 'team_leader', 'collaborators', 'start_date', 'end_date', 'is_finished')) for item in jobs]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
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
        a = session.query(Jobs).order_by(Jobs.id.desc()).first().id
        return jsonify({'success': f'{Jobs.id} added'})
