import flask
from data import db_session
from data.jobs import Jobs
from flask import request
blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/news', methods=['POST'])
def create_news():
    if not request.json:
        return flask.jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['job', 'team_leader', 'work_size', 'is_finished', 'collaborators', 'start_date', 'end_date']):
        return flask.jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    news = Jobs(
        job=request.json['job'],
        team_leader=request.json['team_leader'],
        start_date=request.json['start_date'],
        end_date=request.json['end_date'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished'],
        work_size=request.json['work_size']
    )
    db_sess.add(news)
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})

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


