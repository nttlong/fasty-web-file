# """Endpoints module."""
#
# from fastapi import APIRouter, Depends, Response, status, Request, HTTPException
# from dependency_injector.wiring import inject, Provide
#
# from ...containers import Container
# from ...services.accounts import AccountsService
# from ..routers import router, router_api_post
#
# from fastapi.security import OAuth2PasswordRequestForm
#
# from fastapi_jwt_auth import AuthJWT
#
#
# @router_api_post("accounts/token")
# @inject
# async def get_token(
#         form_data: OAuth2PasswordRequestForm = Depends(),
#         Authorize: AuthJWT = Depends(),
#         account_service: AccountsService = Depends(Provide[Container.accounts_service]),
# ):
#     if await account_service.validate(form_data.username, form_data.password):
#         access_token: str = await account_service.get_access_token(form_data.username)
#         Authorize.set_access_cookies(access_token)
#         return {"access_token": access_token, "token_type": "bearer"}
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     # return await user_service.get_users()
