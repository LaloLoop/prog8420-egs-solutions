from unittest import TestCase

from repository import DBRepository


class TestDBRepository(TestCase):
    def test_create_user(self):
        repo = DBRepository()

        email = 'some@conestoga.ca'
        password = 'MYP4S5'

        created = repo.create_user(email, password)

        self.assertTrue(created)
