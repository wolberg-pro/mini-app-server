# -*- coding: utf-8 -*-
from starlette import status

from core.test.transaction_test_case import TransactionTestCase


class PingTestCase(TransactionTestCase):

    def test_ping(self):
        response = self.client.get('/api/v1/devops/ping')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
