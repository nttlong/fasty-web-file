import handlers
from handlers.client_model.files_register import RegisterUploadInfoResult
from .routers import router, router_api_post, router_api_get
from handlers.api.accounts import accounts_get_token
from handlers.client_model.app import EditAppResutl
from handlers.spa.home_page import page_index
from handlers.spa.one_page import page_only_one
from handlers.api.apps import app_get_list,app_get,app_update
from handlers.api.files import get_list as file_api_get_list_of_files
from handlers.api.file_content import get_content  as file_api_get_content
from handlers.api.files_resgister import register_new_upload
router_api_post("accounts/token")(accounts_get_token)
router_api_post("{app_name}/apps")(app_get_list)
router_api_post("{app_name}/apps/get/{app_name_get}")(app_get)
router_api_post("{app_name}/apps/update/{app_edit}",response_model=EditAppResutl)(app_update)
router_api_post("{app_name}/files")(file_api_get_list_of_files)
router_api_get("{app_name}/file/{directory:path}")(file_api_get_content)
router_api_post("{app_name}/files/register", response_model=RegisterUploadInfoResult)(register_new_upload)
router.get('/')(page_index)
router.get("/{directory:path}")(page_only_one)

