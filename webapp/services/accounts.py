import uuid

from .base import BaseService
from repositories.accounts import AccountsRepository
from jose import jwt
from models.Model_Users import User
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    global pwd_context
    return pwd_context.verify(plain_password, hashed_password)
def generate_salt_and_has_password(username:str,password):
    salt = str(uuid.uuid4())
    hash_text = f"{salt}/{username.lower()}/{password}"
    has_pass =pwd_context.hash(hash_text)
    return has_pass, salt


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
    async def hash_password(self, username, password):
        return generate_salt_and_has_password(username,password)
    async def get_access_token(self, username: str):
        app_name, uid = username.split('/')

        data = dict(
            sub=uid,
            app_name=app_name
        )
        to_encode = data.copy()
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    async def get_sso_id(self, app_name, username, token, return_url_atfer_signIn):

        sso_token = await self.repository.get_sso_id(app_name,username,token,return_url_atfer_signIn)
        return sso_token

    async def get_access_token_from_sso_id(self, SSOID):

        access_token = await self.repository.get_access_token_from_sso_id(SSOID)
        return access_token



