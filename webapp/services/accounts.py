from .base import BaseService
from repositories.accounts import AccountsRepository
from jose import jwt
from models.Model_Users import User
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    global pwd_context
    return pwd_context.verify(plain_password, hashed_password)

class AccountsService(BaseService):
    def __init__(self,
                 account_repository: AccountsRepository,
                 config: dict):
        BaseService.__init__(self)
        self.repository: AccountsRepository = account_repository
        self.config = config
        self.SECRET_KEY = config.get('jwt').get('SECRET_KEY')
        self.ALGORITHM = config.get('jwt').get('ALGORITHM')

    async def validate(self, user: User, password) -> bool:
        pass_hash = user.PasswordSalt+'/'+ user.Username.lower() + "/" + password
        ret = verify_password(pass_hash,user.HashPassword)
        return ret

    async def get_access_token(self, username: str):
        app_name, uid = username.split('/')

        data = dict(
            sub=uid,
            app_name=app_name
        )
        to_encode = data.copy()
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt
