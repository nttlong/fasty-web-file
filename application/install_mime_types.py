import mimetypes
import uvicorn
def install_mime_types():

    mimetypes.types_map['.js']='application/javascript'
    print(mimetypes.types_map['.js'])