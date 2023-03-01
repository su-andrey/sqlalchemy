import flask
import datetime
from data import db_session
from data.jobs import Jobs
from flask import request
blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/addjobs', methods=['POST'])
def create_job():
    if not request.json:
        return flask.jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['job', 'team_leader', 'work_size', 'is_finished', 'collaborators', 'start_date', 'end_date']):
        return flask.jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    try:
        if not db_sess.query(Jobs).filter(Jobs.id == request.json['id']).all():
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
    except Exception:
        return Exception
    return flask.jsonify({'error': 'bad data', 'id': 'already exists'})

@blueprint.route('/api/jobs')
def get_news():
    db_sess = db_session.create_session()
    news = db_sess.query(Jobs).all()
    return flask.jsonify(
        {
            'news':
                [item.to_dict(only=('job', 'start_date', 'end_date'))
                 for item in news]
        }
    )

@blueprint.route('/api/jobs/<int:news_id>', methods=['GET'])
def get_one_news(news_id):
    db_sess = db_session.create_session()
    news = db_sess.query(Jobs).get(news_id)
    if not news:
        return flask.jsonify({'error': 'Not found'})
    return flask.jsonify(
        {
            'news': news.to_dict(only=(
                'job', 'team_leader', 'start_date', 'end_date'))
        }
    )


@blueprint.route('/api/deletework/<int:work_id>', methods=['DELETE'])
def delete_news(work_id):
    db_sess = db_session.create_session()
    work = db_sess.query(Jobs).get(work_id)
    if not work:
        return flask.jsonify({'error': 'Not found'})
    db_sess.delete(work)
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})


@blueprint.route('/api/editwork/<int:work_id>', methods=['POST'])
def edit_work(work_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == work_id).one()
    if not job:
        return flask.jsonify({'error': 'Not found'})
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




