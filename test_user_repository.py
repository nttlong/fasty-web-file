from repositories import UserRepository
from unittest import mock
from models.Model_Users import User
repository_mock = mock.Mock(spec=UserRepository)
repository_mock.get_all.return_value = [
    User(id=1, email="test1@email.com", hashed_password="pwd", is_active=True),
    User(id=2, email="test2@email.com", hashed_password="pwd", is_active=False),
]
print('ok')