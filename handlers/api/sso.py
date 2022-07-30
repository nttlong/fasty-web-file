from dependency_injector.wiring import inject, Provide
from webapp.containers import Container
from fastapi import Depends, status
from fastapi.responses import RedirectResponse

import utils
from  fastapi import Request
# @fasty.api_post("/get_sso_token")
from services.accounts import AccountsService
from services.apps import AppService


@inject
async def get_sso_token(
        request:Request,
        token: str = Depends(utils.OAuth2AndGetUserInfo()),
        account_service:AccountsService=Depends(Provide[Container.accounts_service]),
        apps_services: AppService= Depends(Provide[Container.apps_services])
        ):
    app = await apps_services.get_app_by_name('admin', request.app_name)
    if app is None:
        return  None
    sso_id = await account_service.get_sso_id(
        request.app_name,request.username, token,app.ReturnUrlAfterSignIn)
    """
    <h2>Lấy SSO Token</h2>.<br>
    Bên cạnh việc cung cấp các Restfull API, hệ thống này cũng cung cấp các dịch vụ như xem file,
    media streaming,..., kể cả các web app.<br/>
    <p>
        Với các dịch vụ Restfull API thì việc truyền Access token vào header trước khi request về hệ thống này là rất dễ dàng.
        Nhưng với các dịch vụ khác là điều không thể.
        Ví dụ một request để xem video của một trang như sau: https://my-server/video/my-video.pm4
        đòi hỏi phải vượt qua được chứng thực tại server my-server
        (người dùng chỉ copy link này và paste vào thanh address của trình duyệt,
         nên việc gắn Access token vào request là điều không thể) Có các cách sau để vượt qua được chứng thực này:
        <ol>
            <li>Login (chỉ thực hiện được khi my-server cung cấp một trang để Login)</li>
            <li>
                Gắn query string vào link này ví dụ: https://my-server/video/my-video.pm4?access-token=... Điều này là không nên bởi 2 lý do sau
                <ol>
                    <li>Bảo mật: Access token là thành phần nên được che đậy cẩn thận </li>
                    <li>Url truy cập phải giống nhau với mọi user ở bất kỳ thời điểm nào </li>
                </ol>
            </li>
        </ol>
    </p>
    <p>
        Vì lý dó trên mà dịch vụ này sẽ cung cấp một API để lấy SSO Token. Sau đó sử dụng SSO Token này để Sigin vào dịch vụ
        (Dịch vụ không có quyền bắt người dùng cuối phải login)
    </p>
    <p>
        API này sẽ trả về SSO token key. SSO token sẽ mất hiệu lực ngay khi được sử dụng kể cả trường hợp không thành công.<br/>
        Để gọi API này gắn Access token vào header như sau:
        header[Authorization]='Bearer [Access token key]'<br/>
        Ví dụ:
        <textarea>

            fetch('api/get_sso_token', {
            method: 'POST',
            mode: 'no-cors', // this is to prevent browser from sending 'OPTIONS' method request first
            redirect: 'follow',
            headers: new Headers({
                    'Content-Type': 'text/plain',
                    'X-My-Custom-Header': 'value-v',
                    'Authorization': 'Bearer ' + token,
            }),
            body: companyName

        })
        </textarea>
    </p>

    :param app_name:
    :param token:
    :return:
    """

    return {"token": sso_id}

@inject
async def sso_sigin(SSOID: str,request: Request,account_service:AccountsService= Depends(Provide[Container.accounts_service])):
    """
    Đăng nhập vào dịch vụ bằng SSOID.
    Khi 1 web site remote muốn truy cập vào dịch vụ bằng trình duyệt,
    nhưng lại không thể gởi access token qua header hoặc request params.
    (Ví dụ như xem nôi dung file bằng url của dịch vụ ngay tại site remote)
    Thì web site remote phải redirect sang url của dịch vụ để có thể truy cập được
    :param SSOID:
    :param account_service:
    :return:
    """
    access_token = await account_service.get_access_token_from_sso_id(SSOID)
    # ret_url = ret_item.get(fasty.JWT_Docs.SSOs.ReturnUrlAfterSignIn.__name__, fasty.config.app.root_url)
    # Authorize.set_access_cookies(ret_item[fasty.JWT_Docs.SSOs.Token.__name__])
    ret_url = request.query_params.get('ret','/')

    res = RedirectResponse(url=ret_url, status_code=status.HTTP_303_SEE_OTHER)
    res.set_cookie("access_token_cookie", access_token)
    return res

# @fasty.api_get("sso/signin/{SSOID}")(sso_sigin)
# async def do_sign_in(app_name:str,SSOID: str):
#     """
#     Đăng nhập vào dịch vụ bằng SSOID.
#     Khi 1 web site remote muốn truy cập vào dịch vụ bằng trình duyệt,
#     nhưng lại không thể gởi access token qua header hoặc request params.
#     (Ví dụ như xem nôi dung file bằng url của dịch vụ ngay tại site remote)
#     Thì web site remote phải redirect sang url của dịch vụ để có thể truy cập được
#
#     :param app_name:
#     :param SSOID:
#     :param request:
#     :param Authorize:
#     :return:
#     """
#     access_token =
#     db_name = default_db_name
#     if db_name is None:
#         return Response(status_code=403)
#     db_context = get_db_context(db_name)
#     ret_item = await db_context.find_one_async(
#         fasty.JWT_Docs.SSOs,
#         fasty.JWT_Docs.SSOs.SSOID == SSOID
#     )
#     ret_url = ret_item.get(fasty.JWT_Docs.SSOs.ReturnUrlAfterSignIn.__name__, fasty.config.app.root_url)
#     Authorize.set_access_cookies(ret_item[fasty.JWT_Docs.SSOs.Token.__name__])
#     ret_url = request.query_params.get('ret', ret_url)
#
#     res = RedirectResponse(url=ret_url, status_code=status.HTTP_303_SEE_OTHER)
#     res.set_cookie("access_token_cookie", ret_item[fasty.JWT_Docs.SSOs.Token.__name__])
#     return res