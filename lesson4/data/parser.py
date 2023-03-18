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

post_job_parser = reqparse.RequestParser()
post_job_parser.add_argument('id', type=int)
post_job_parser.add_argument('job', type=str)
post_job_parser.add_argument('work_size', type=str)
post_job_parser.add_argument('collaborators', type=str)
post_job_parser.add_argument('is_finished', type=bool)
post_job_parser.add_argument('team_leader', type=int)
post_job_parser.add_argument('category_id', type=int)
