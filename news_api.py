import datetime
import flask
import sqlalchemy.exc
from flask import request

from data import db_session
from data.jobs import Jobs

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)
#Все по адресу /api/jobs (get - просмотр, delete -удаление, post - Добавление, put - изменение)

@blueprint.route('/api/jobs', methods=['GET'])
def get_news():
    db_sess = db_session.create_session()
    news = db_sess.query(Jobs).all()
    return flask.jsonify(
        {
            'jobs':
                [item.to_dict(only=('job', 'start_date', 'end_date'))
                 for item in news]
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def add_news():
    if not request.json:
        return flask.jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['job', 'team_leader', 'work_size', 'is_finished', 'collaborators']):
        return flask.jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    job = Jobs()
    job.job = request.json['job']
    job.team_leader = request.json['team_leader']
    job.work_size = request.json['work_size']
    job.start_date = datetime.datetime.now()
    job.end_date = datetime.datetime.now()
    job.collaborators = request.json['collaborators']
    job.is_finished = request.json['is_finished']
    db_sess.add(job)
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_news(job_id):
    db_sess = db_session.create_session()
    news = db_sess.query(Jobs).get(job_id)
    if not news:
        return flask.jsonify({'error': 'Not found'})
    return flask.jsonify(
        {
            'jobs': news.to_dict(only=(
                'job', 'team_leader', 'start_date', 'end_date'))
        }
    )


@blueprint.route('/api/jobs/<int:job_id>', methods=['POST'])
def editwork(job_id):
    db_sess = db_session.create_session()
    try:
        job = db_sess.query(Jobs).get(job_id)
    except sqlalchemy.exc.NoResultFound:
        return flask.jsonify({'error': 'bad id or something else'})
    if not job:
        return flask.jsonify({'error': 'Not found'})
    try:
        job.job = request.json['job']
        job.team_leader = int(request.json['team_leader'])
        job.work_size = int(request.json['work_size'])
        job.start_date = datetime.datetime.now()
        job.end_date = datetime.datetime.now()
        job.collaborators = request.json['collaborators']
        job.is_finished = request.json['is_finished']
        db_sess.add(job)
        db_sess.commit()
        return flask.jsonify({'success': 'OK'})
    except KeyError:
        return flask.jsonify({'Error': 'KeyError'})
    except ValueError:
        return flask.jsonify({'Error': 'ValueError'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_news(jobs_id):
    db_sess = db_session.create_session()
    work = db_sess.query(Jobs).get(jobs_id)
    if not work:
        return flask.jsonify({'error': 'Not found'})
    db_sess.delete(work)
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})
