from flask_restful import reqparse, Api, Resource, abort
from flask import Response
import sqlalchemy
from .users import User






class UserResourse(Resource):
    """ресурсы юзера"""

    def get(self, user_id: int) -> Response:
        """получение одного пользователя"""

