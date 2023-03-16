import os
from flask import Flask
from data import db_session, api
import shutil

import unittest

from typing import Union
from parameterized import parameterized


class ApiJobTests(unittest.TestCase):
    """тесты на работу api"""

    def setUp(self) -> None:
        """подготовка к тестированию, создание тестовой бд"""
        shutil.copyfile('db/mars_mission.sqlite3', 'db/test_db.sqlite3')
        self.app = Flask(__name__)
        db_session.global_init('db/test_db.sqlite3')
        self.app.register_blueprint(api.blueprint)
        self.client = self.app.test_client()
        super().setUp()

    def tearDown(self):
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
            [999, 200],
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
            [9999999, 'error'],
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
                'error'
            ],
            [
                {
                    'id': 2,  # не хватает category_id
                    'job': 'a',
                    'work_size': 1,
                    'collaborators': '1, 2, 3',
                    'is_finished': False,
                    'team_leader': 1,
                },
                'error'
            ],
            [
                {}, 'error'  # пустой запрос
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
        if expected == 'success':
            job = self.client.get(f'/api/jobs/{request_json["id"]}/').json
            self.assertIn('job', job)
        else:
            self.assertIn(expected, response)

    @parameterized.expand(
        [
            (2,), (3,), (4,)
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
        self.assertIn('error', response)

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
                'error'
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
                'error'
            ],
            [
                2, {}, 'error'  # пустой запрос
            ],
            [
                1,
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
        if expected == 'success':
            job = self.client.get(f'/api/jobs/{job_id}/').json
            self.assertIn('job', job)
        else:
            self.assertIn(expected, response)


# class ApiUserTest(unittest.TestCase):
#     """тестируем апи юзера"""
#
#     def setUp(self) -> None:
#         """подготовка к тестированию, создание тестовой бд"""
#         shutil.copyfile('db/mars_mission.sqlite3', 'db/test_db.sqlite3')
#         self.app = Flask(__name__)
#         db_session.global_init('db/test_db.sqlite3')
#         self.app.register_blueprint(api.blueprint)
#         self.client = self.app.test_client()
#         super().setUp()




if __name__ == '__main__':
    unittest.main()
