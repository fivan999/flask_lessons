import os
from flask import Flask
from data import db_session, users_resourse, jobs_resourse
import shutil

import unittest

from typing import Union
from parameterized import parameterized
from flask_restful import Api
from data.users import User


class ApiJobTests(unittest.TestCase):
    """тесты на работу api jobs"""

    def setUp(self) -> None:
        """подготовка к тестированию, создание тестовой бд"""
        shutil.copyfile('db/mars_mission.sqlite3', 'db/test_db.sqlite3')
        self.app = Flask(__name__)
        db_session.global_init('db/test_db.sqlite3')
        self.api = Api(self.app)
        self.api.add_resource(
            jobs_resourse.JobListResourse, '/api/jobs/'
        )
        self.api.add_resource(
            jobs_resourse.JobResourse, '/api/jobs/<int:job_id>/'
        )
        self.client = self.app.test_client()
        super().setUp()

    def tearDown(self) -> None:
        """закрываем бд"""
        os.remove('db/test_db.sqlite3')
        super().tearDown()

    def test_api_get_jobs_correct_context(self) -> None:
        """тестируем корректный контекст get_jobs"""
        response = self.client.get('/api/jobs/').json
        self.assertIn('jobs', response)

    @parameterized.expand(
        [
            [1, 200],
            [2, 200],
            [3, 200],
            ['aboba', 404],
            [999, 404],
        ]
    )
    def test_api_get_exact_job_status_code(
        self, test_case: Union[int, str], expected: int
    ) -> None:
        """тестируем статус код у get_exact_job"""
        response = self.client.get(f'/api/jobs/{test_case}/')
        self.assertEqual(response.status_code, expected)

    @parameterized.expand(
        [
            [2, 'job'],
            [3, 'job'],
            [1, 'job'],
            [9999999, 'message'],
        ]
    )
    def test_api_get_exact_job_correct_context(
        self, test_case: int, expected: str
    ) -> None:
        """тестируем корректный контекст у get_exact_job"""
        response = self.client.get(f'/api/jobs/{test_case}/').json
        self.assertIn(expected, response)

    @parameterized.expand(
        [
            [
                {
                    'id': 2,  # существующий id
                    'job': 'a',
                    'work_size': 1,
                    'collaborators': '1, 2, 3',
                    'is_finished': False,
                    'team_leader': 1,
                    'category_id': 1
                },
                'message'
            ],
            [
                {
                    'id': 8,  # не хватает category_id
                    'job': 'a',
                    'work_size': 1,
                    'collaborators': '1, 2, 3',
                    'is_finished': False,
                    'team_leader': 1,
                },
                'message'
            ],
            [
                {}, 'message'  # пустой запрос
            ],
            [
                {
                    'id': 1097,  # всё нормик
                    'job': 'a',
                    'work_size': 1,
                    'collaborators': '1, 2, 3',
                    'is_finished': False,
                    'team_leader': 1,
                    'category_id': 1
                },
                'success'
            ],
        ]
    )
    def test_api_create_job(self, request_json: dict, expected: str) -> None:
        """тестируем post запросы на создание job"""
        response = self.client.post(
            '/api/jobs/', json=request_json
        ).json
        self.assertIn(expected, response)

    @parameterized.expand(
        [
            [
                99999999,  # несуществующий id
                {
                    'job': 'a',
                    'work_size': 1,
                    'collaborators': '1, 2, 3',
                    'is_finished': False,
                    'team_leader': 1,
                    'category_id': 1
                },
                'message'
            ],
            [
                2,  # не хватает category_id
                {
                    'job': 'a',
                    'work_size': 1,
                    'collaborators': '1, 2, 3',
                    'is_finished': False,
                    'team_leader': 1,
                },
                'message'
            ],
            [
                2, {}, 'message'  # пустой запрос
            ],
            [
                1,  # все ок
                {
                    'job': 'a',
                    'work_size': 1,
                    'collaborators': '1, 2',
                    'is_finished': False,
                    'team_leader': 1,
                    'category_id': 1
                },
                'success'
            ],
        ]
    )
    def test_api_edit_job(
        self, job_id: int, request_json: dict, expected: str
    ) -> None:
        """тестируем put запросы на изменение job"""
        response = self.client.put(
            f'/api/jobs/{job_id}/', json=request_json
        ).json
        self.assertIn(expected, response)

    @parameterized.expand(
        [
            (2,), (3,), (1,)
        ]
    )
    def test_api_delete_correct_job(self, job_id: int) -> None:
        """тестируем правильное удаление работы"""
        start_count = len(
            self.client.get('/api/jobs/').json['jobs']
        )
        self.client.delete(f'/api/jobs/{job_id}/')
        end_count = len(
            self.client.get('/api/jobs/').json['jobs']
        )
        self.assertEqual(start_count - 1, end_count)

    @parameterized.expand([(88,), (99999999,)])
    def test_api_delete_incorrect_job(self, job_id: Union[int, str]) -> None:
        """тестируем ошибку при удалении работы"""
        response = self.client.delete(f'/api/jobs/{job_id}/').json
        self.assertIn('message', response)


class ApiUserTest(unittest.TestCase):
    """тестируем апи юзера"""

    def setUp(self) -> None:
        """подготовка к тестированию, создание тестовой бд"""
        shutil.copyfile('db/mars_mission.sqlite3', 'db/test_db.sqlite3')
        self.app = Flask(__name__)
        db_session.global_init('db/test_db.sqlite3')
        self.api = Api(self.app)
        self.api.add_resource(
            users_resourse.UserListResourse, '/api/users/'
        )
        self.api.add_resource(
            users_resourse.UserResourse, '/api/users/<int:user_id>/'
        )
        self.client = self.app.test_client()
        super().setUp()

    def tearDown(self) -> None:
        """закрываем бд"""
        os.remove('db/test_db.sqlite3')
        super().tearDown()

    def test_api_get_users_correct_context(self) -> None:
        """тестируем корректный контекст получения пользователей"""
        response = self.client.get('/api/users/').json
        self.assertIn('users', response)

    @parameterized.expand(
        [
            [1, 200],
            [2, 200],
            [3, 200],
            ['aboba', 404],
            [999, 404],
        ]
    )
    def test_api_get_exact_user_status_code(
        self, test_case: Union[int, str], expected: int
    ) -> None:
        """тестируем статус код получения пользователя"""
        response = self.client.get(f'/api/users/{test_case}/')
        self.assertEqual(response.status_code, expected)

    @parameterized.expand(
        [
            (2,), (3,), (1,)
        ]
    )
    def test_api_delete_correct_user(self, user_id: int) -> None:
        """тестируем правильное удаление пользователя"""
        start_count = len(
            self.client.get('/api/users/').json['users']
        )
        self.client.delete(f'/api/users/{user_id}/')
        end_count = len(
            self.client.get('/api/users/').json['users']
        )
        self.assertEqual(start_count - 1, end_count)

    @parameterized.expand(
        [
            [
                {
                    'surname': 'ivan',  # не хватает city_from
                    'name': 'ivan',
                    'age': 1,
                    'position': 'genius',
                    'speciality': 'verb',
                    'address': '1',
                    'email': 'aboba2@ya.ru',
                    'password': 'aboba'
                },
                'message'
            ],
            [
                {
                    'surname': 'ivan',  # неправильный формат address
                    'name': 'ivan',
                    'age': 1,
                    'position': 'genius',
                    'speciality': 'verb',
                    'address': 1,
                    'email': 'aboba@ya.ru',
                    'password': 'aboba',
                    'city_from': 'moscow'
                },
                'message'
            ],
            [
                {
                    'surname': 'ivan',  # существующая почта
                    'name': 'ivan',
                    'age': 1,
                    'position': 'genius',
                    'speciality': 'verb',
                    'address': 'a',
                    'email': 'aboba@ya.ru',
                    'password': 'aboba',
                    'city_from': 'moscow'
                },
                'message'
            ],
            [
                {
                    'surname': 'ivan',  # все нормик
                    'name': 'ivan',
                    'age': 1,
                    'position': 'genius',
                    'speciality': 'verb',
                    'address': 'module 1',
                    'email': 'aboba4@ya.ru',
                    'password': 'aboba',
                    'city_from': 'moscow'
                },
                'success'
            ],
        ]
    )
    def test_api_create_user(self, request_json: dict, expected: str) -> None:
        """тестируем post запросы на создание user"""
        response = self.client.post(
            '/api/users/', json=request_json
        ).json
        self.assertIn(expected, response)

    @parameterized.expand(
        [
            [
                1,
                {
                    'surname': 'ivan',  # все нормик
                    'name': 'ivan',
                    'age': 1,
                    'position': 'genius',
                    'speciality': 'verb',
                    'address': 'module 1',
                    'email': 'aboba4@ya.ru',
                    'password': 'aboba',
                    'city_from': 'moscow'
                },
                'success'
            ],
            [
                1,
                {
                    'surname': 'ivan',  # существующая почта
                    'name': 'ivan',
                    'age': 1,
                    'position': 'genius',
                    'speciality': 'verb',
                    'address': 'a',
                    'email': 'aboba@ya.ru',
                    'password': 'aboba',
                    'city_from': 'moscow'
                },
                'message'
            ],
            [
                9999,  # несуществующий id
                {
                    'surname': 'ivan',
                    'name': 'ivan',
                    'age': 1,
                    'position': 'genius',
                    'speciality': 'verb',
                    'address': '1',
                    'email': 'aboba@ya.ru',
                    'password': 'aboba',
                    'city_from': 'moscow'
                },
                'message'
            ],
            [
                1,
                {
                    'surname': 'ivan',  # не хватает city_from
                    'name': 'ivan',
                    'age': 1,
                    'position': 'genius',
                    'speciality': 'verb',
                    'address': '1',
                    'email': 'aboba@ya.ru',
                    'password': 'aboba',
                },
                'message'
            ],
        ]
    )
    def test_api_edit_user(
        self, user_id: int, request_json: dict, expected: str
    ) -> None:
        """тестируем put запросы на изменение user"""
        response = self.client.put(
            f'/api/users/{user_id}/', json=request_json
        ).json
        self.assertIn(expected, response)


if __name__ == '__main__':
    unittest.main()
