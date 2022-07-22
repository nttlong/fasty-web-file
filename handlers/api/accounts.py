import uuid

from dependency_injector.wiring import inject, Provide
from fastapi_jwt_auth import AuthJWT
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status

import models.documents
from application_context import AppContext
from webapp.services.accounts import AccountsService
from webapp.containers import Container
from pydantic import BaseModel

from webapp.services.users import UserService


class User(BaseModel):
    username: str
    password: str


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
    # Configure application to store and get JWT from cookies
    authjwt_token_location: set = {"cookies"}
    # Disable CSRF Protection for this example. default is True
    authjwt_cookie_csrf_protect: bool = False


@AuthJWT.load_config
@inject
def get_config(config = Provide[Container.config]):
    fx = Settings()
    sc =config.provider.get('jwt').get('SECRET_KEY')
    fx.authjwt_secret_key=sc
    return fx


@inject
async def accounts_get_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        Authorize: AuthJWT = Depends(),
        account_service: AccountsService = Depends(Provide[Container.accounts_service]),
        user_service: UserService = Depends(Provide[Container.user_service])
):
    root_user =await user_service.get_user_by_name('admin','root')
    if root_user is None:
        root_user = models.documents.User({})
        root_user.Username='root'
        root_user.HashPassword,root_user.PasswordSalt= await account_service.hash_password(
            root_user.Username,
            'root'
        )
        await user_service.create_user('admin',root_user)

    if form_data.username.index('/')==-1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    app_name,uid = form_data.username.split('/')

    user = await user_service.get_user_by_name(app_name, uid)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if await account_service.validate(user, form_data.password):
        access_token: str = await account_service.get_access_token(form_data.username)
        Authorize.set_access_cookies(access_token)
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
