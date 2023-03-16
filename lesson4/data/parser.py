from flask_restful import reqparse


post_user_parser = reqparse.RequestParser()
post_user_parser.add_argument('surname', type=str)
post_user_parser.add_argument('name', type=str)
post_user_parser.add_argument('age', type=int)
post_user_parser.add_argument('position', type=str)
post_user_parser.add_argument('speciality', type=str)
post_user_parser.add_argument('address', type=str)
post_user_parser.add_argument('age', type=int)
post_user_parser.add_argument('email', type=str)
post_user_parser.add_argument('city_from', type=str)
post_user_parser.add_argument('password', type=str)
