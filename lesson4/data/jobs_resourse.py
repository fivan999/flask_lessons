from flask_restful import Resource, abort
from flask import Response, jsonify
from . import db_session
import sqlalchemy
from .jobs import Jobs
from .categories import Category
from .parser import post_job_parser


def abort_if_job_not_found(job_id: int) -> None:
    """проверка работы на существование"""
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == job_id)
    db_sess.close()
    if jobs.count() == 0:
        abort(404, message=f'Job {job_id} not found')


def abort_if_category_not_found(category_id: int) -> None:
    """проверка работы на существование"""
    db_sess = db_session.create_session()
    category = db_sess.query(Category).filter(Category.id == category_id)
    db_sess.close()
    if category.count() == 0:
        abort(404, message=f'Category {category_id} not found')


def abort_if_job_already_exists(job_id: int) -> None:
    """проверка работы на существование"""
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == job_id)
    db_sess.close()
    if jobs.count():
        abort(404, message=f'Job {job_id} already exists')


def abort_if_post_args_not_enought(post_args: dict) -> None:
    """проверямяем наличие всех аргументов при создании работы"""
    if not all(
        post_args[key] is not None for key in [
            'job',
            'work_size',
            'collaborators',
            'is_finished',
            'team_leader',
            'category_id'
        ]
    ):
        abort(400, message='Bad request')


class JobListResourse(Resource):
    """работа со списком работ"""

    def get(self) -> Response:
        """получение всех работ"""
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).all()
        db_sess.close()
        return jsonify(
            {
                'jobs': [
                    job.to_dict(
                        only=(
                            c_attr.key for c_attr in
                            sqlalchemy.inspect(job).mapper.column_attrs
                        )
                    ) for job in jobs
                ]
            }
        )

    def post(self) -> Response:
        """добавляем работу"""
        args = post_job_parser.parse_args()
        abort_if_post_args_not_enought(args)
        abort_if_job_already_exists(args['id'])
        abort_if_category_not_found(args['category_id'])
        db_sess = db_session.create_session()
        new_job = Jobs(
            id=args['id'],
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            is_finished=args['is_finished'],
            team_leader=args['team_leader'],
            category_id=args['category_id']
        )
        db_sess.add(new_job)
        db_sess.commit()
        db_sess.close()
        return jsonify({'success': 'OK'})


class JobResourse(Resource):
    """одна работа"""

    def get(self, job_id: int) -> Response:
        """получение одной работы"""
        abort_if_job_not_found(job_id)
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
        db_sess.close()
        return jsonify(
            {
                'job': job.to_dict(
                    only=(
                        c_attr.key for c_attr in
                        sqlalchemy.inspect(job).mapper.column_attrs
                    )
                )
            }
        )

    def delete(self, job_id: int) -> Response:
        """удаляем одну работу"""
        abort_if_job_not_found(job_id)
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
        db_sess.delete(job)
        db_sess.commit()
        db_sess.close()
        return jsonify({'success': 'OK'})

    def put(self, job_id: int) -> Resource:
        """изменение работы"""
        abort_if_job_not_found(job_id)
        args = post_job_parser.parse_args()
        abort_if_post_args_not_enought(args)
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
        job.job = args['job']
        job.work_size = args['work_size']
        job.collaborators = args['collaborators']
        job.is_finished = args['is_finished']
        job.team_leader = args['team_leader']
        job.category_id = args['category_id']
        db_sess.commit()
        db_sess.close()
        return jsonify({'success': 'OK'})
