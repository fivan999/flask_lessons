import flask
from flask import jsonify, Response, request

from sqlalchemy import inspect
from . import db_session
from .jobs import Jobs
from .users import User


blueprint = flask.Blueprint(
    'mars_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs/')
def get_jobs() -> Response:
    """список всех работ"""
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    db_sess.close()
    return jsonify(
        {
            'jobs': [
                job.to_dict(
                    only=(
                        c_attr.key for c_attr in
                        inspect(job).mapper.column_attrs
                    )
                ) for job in jobs
            ]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>/')
def get_exact_job(job_id: int) -> Response:
    """одна работа"""
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == job_id)
    db_sess.close()
    if job.count():
        job = job.first()
        return jsonify(
            {
                'job': job.to_dict(
                    only=(
                        c_attr.key for c_attr in
                        inspect(job).mapper.column_attrs
                    )
                )
            }
        )
    else:
        return jsonify({'error': 'not found'})


@blueprint.route('/api/jobs/', methods=['POST'])
def create_job() -> Response:
    """добавление работы"""
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(
        key in request.json for key in [
            'id',
            'job',
            'work_size',
            'collaborators',
            'is_finished',
            'team_leader',
            'category_id'
        ]
    ):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == request.json['id'])
    if job.count():
        return jsonify({'error': 'id already exists'})
    new_job = Jobs(
        id=request.json['id'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished'],
        team_leader=request.json['team_leader'],
        category_id=request.json['category_id']
    )
    db_sess.add(new_job)
    db_sess.commit()
    db_sess.close()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>/', methods=['PUT'])
def edit_job(job_id: int) -> Response:
    """изменение работы"""
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(
        key in request.json for key in [
            'job',
            'work_size',
            'collaborators',
            'is_finished',
            'team_leader',
            'category_id'
        ]
    ):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == job_id)
    if not job.count():
        return jsonify({'error': 'no such job'})
    job = job.first()
    job.job = request.json['job']
    job.work_size = request.json['work_size']
    job.collaborators = request.json['collaborators']
    job.is_finished = request.json['is_finished']
    job.team_leader = request.json['team_leader']
    job.category_id = request.json['category_id']
    db_sess.commit()
    db_sess.close()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>/', methods=['DELETE'])
def delete_job(job_id: int) -> Response:
    """удаление работы"""
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == job_id)
    if not job.count():
        return jsonify({'error': 'not found'})
    job.delete()
    db_sess.commit()
    db_sess.close()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/')
def get_users() -> Response:
    """получение всех пользователей"""
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    db_sess.close()
    return jsonify(
        {
            'users': [
                user.to_dict(
                    only=(
                        c_attr.key for c_attr in
                        inspect(user).mapper.column_attrs
                    )
                ) for user in users
            ]
        }
    )


@blueprint.route('/api/users/<int:user_id>/')
def get_exact_user(user_id: int) -> Response:
    """один пользователь"""
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id)
    db_sess.close()
    if user.count():
        user = user.first()
        return jsonify(
            {
                'user': user.to_dict(
                    only=(
                        c_attr.key for c_attr in
                        inspect(user).mapper.column_attrs
                    )
                )
            }
        )
    else:
        return jsonify({'error': 'not found'})


@blueprint.route('/api/users/', methods=['POST'])
def create_user() -> Response:
    """добавление пользователя"""
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(
        key in request.json for key in [
            'surname',
            'name',
            'age',
            'position',
            'speciality',
            'address',
            'email',
            'password',
            'city_from'
        ]
    ):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == request.json['email'])
    if user.count():
        return jsonify({'error': 'user already exists'})
    new_user = User(
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email'],
        city_from=request.json['city_from']
    )
    new_user.set_password(request.json['password'])
    db_sess.add(new_user)
    db_sess.commit()
    db_sess.close()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/', methods=['PUT'])
def edit_user() -> Response:
    """изменение пользователя"""
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(
        key in request.json for key in [
            'surname',
            'name',
            'age',
            'position',
            'speciality',
            'address',
            'email',
            'password',
            'city_from'
        ]
    ):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == request.json['email'])
    if not user.count():
        return jsonify({'error': 'no such user'})
    user = user.first()
    user.surname = request.json['surname']
    user.name = request.json['name']
    user.age = request.json['age']
    user.position = request.json['position']
    user.speciality = request.json['speciality']
    user.address = request.json['address']
    user.city_from = request.json['city_from']
    user.set_password(request.json['password'])
    db_sess.commit()
    db_sess.close()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>/', methods=['DELETE'])
def delete_user(user_id: int) -> Response:
    """удаление юзера"""
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id)
    if not user.count():
        return jsonify({'error': 'not found'})
    user.delete()
    db_sess.commit()
    db_sess.close()
    return jsonify({'success': 'OK'})
