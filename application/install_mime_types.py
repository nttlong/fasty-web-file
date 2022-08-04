import mimetypes
import uvicorn
def install_mime_types():

    mimetypes.types_map['.js']='application/javascript'
    mimetypes.types_map['.webp']='image/webp'
    print(mimetypes.types_map['.js'])