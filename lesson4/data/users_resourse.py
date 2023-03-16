from flask_restful import Resource, abort
from flask import Response, jsonify
from . import db_session
import sqlalchemy
from .users import User
from .parser import post_user_parser


def abort_if_user_not_found(user_id: int) -> None:
    """проверка пользователя на существование"""
    db_sess = db_session.create_session()
    news = db_sess.query(User).get(user_id)
    db_sess.close()
    if not news:
        abort(404, message=f'User {user_id} not found')


def abort_if_post_args_not_enought(post_args: dict) -> None:
    """проверямяем наличие всех аргументов при создании юзера"""
    if not all(
        key in post_args for key in [
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
        abort(400, message='Bad request')


def abort_user_already_exists(email: str) -> None:
    """ппроверяем существует ли пользователь"""
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == email)
    db_sess.close()
    if user.count():
        abort(400, message='User already exists')


class UserListResourse(Resource):
    """работа со списком юзера"""

    def get(self) -> Response:
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
                            sqlalchemy.inspect(user).mapper.column_attrs
                        )
                    ) for user in users
                ]
            }
        )

    def post(self) -> Response:
        """добавляем пользователя"""
        args = post_user_parser.parse_args()
        abort_if_post_args_not_enought(args)
        db_sess = db_session.create_session()
        abort_user_already_exists(args['email'])
        new_user = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'],
            city_from=args['city_from']
        )
        new_user.set_password(args['password'])
        db_sess.add(new_user)
        db_sess.commit()
        db_sess.close()
        return jsonify({'success': 'OK'})


class UserResourse(Resource):
    """один юзер"""

    def get(self, user_id: int) -> Response:
        """получение одного пользователя"""
        abort_if_user_not_found(user_id)
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == user_id).first()
        db_sess.close()
        return jsonify(
            {
                'user': user.to_dict(
                    only=(
                        c_attr.key for c_attr in
                        sqlalchemy.inspect(user).mapper.column_attrs
                    )
                )
            }
        )

    def delete(self, user_id: int) -> Response:
        """удаляем одного пользователя"""
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


