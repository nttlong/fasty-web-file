from dependency_injector.wiring import inject, Provide
from webapp.containers import Container


@inject
def get_token_url(config_provider=Provide[Container.config]):
    config = config_provider.provider
    global SECRET_KEY
    global ALGORITHM
    # config: Configuration = config_provider.provider
    SECRET_KEY = config.get('jwt').get('SECRET_KEY')
    ALGORITHM = config.get('jwt').get('ALGORITHM')
    __api_host_dir__ = config.get('front-end').get('api-url')

    return f"{__api_host_dir__}/accounts/token"


"""
Quản lý JWT
"""
from fastapi import HTTPException
from typing import Dict, Optional

from starlette.requests import Request
from typing import Union
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from dependency_injector.wiring import inject, Provide
from dependency_injector.providers import Configuration
from fastapi.security.utils import get_authorization_scheme_param
from webapp.containers import Container
from jose import jwt
import jose
from starlette.status import HTTP_401_UNAUTHORIZED

from application_context import AppContext


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
    # Configure application to store and get JWT from cookies
    authjwt_token_location: set = {"cookies"}
    # Disable CSRF Protection for this example. default is True
    authjwt_cookie_csrf_protect: bool = False


SECRET_KEY = None
ALGORITHM = None
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class TokenData(BaseModel):
    username: Union[str, None] = None
    application: Union[str, None] = None


class OAuth2(OAuth2PasswordBearer):
    def __init__(
            self,
            scheme_name: Optional[str] = None,
            scopes: Optional[Dict[str, str]] = None,
            description: Optional[str] = None,
            auto_error: bool = True,
    ):
        tokenUrl = get_token_url()
        if not scopes:
            scopes = {}

        super().__init__(
            tokenUrl=tokenUrl,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
            scopes=scopes
        )

    async def get_token(self, request: Request):
        token = request.cookies.get('access_token_cookie')
        if token is None:
            authorization: str = request.headers.get("Authorization")
            if authorization is not None:
                try:
                    scheme, token = get_authorization_scheme_param(authorization)
                finally:
                    token = None
        return token

    @inject
    async def __call__(self, request: Request) -> Optional[str]:
        return await self.get_token(request)


@inject
def get_app_context(app_context: AppContext = Provide[Container.app_context]) -> AppContext:
    return app_context


@inject
class OAuth2Redirect(OAuth2):
    def __init__(
            self,
            scheme_name: Optional[str] = None,
            scopes: Optional[Dict[str, str]] = None,
            description: Optional[str] = None,
            auto_error: bool = True,
            app_context: AppContext = Provide[Container.app_context]
    ):
        OAuth2.__init__(self, scheme_name, scopes, description, auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        global SECRET_KEY
        global ALGORITHM

        token = await self.get_token(request)
        if token is None:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        try:
            ret_data = jwt.decode(token, SECRET_KEY,
                                  algorithms=[ALGORITHM],
                                  options={"verify_signature": False},
                                  )

            setattr(request, "username", ret_data.get("sup"))
            setattr(request, "application_name", ret_data.get("application"))


        except jose.exceptions.JWTError:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jose.exceptions.ExpiredSignatureError as e:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return token
