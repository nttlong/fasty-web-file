import mimetypes

from fastapi import Request
import time
async def add_process_javascript_module(request: Request, call_next):
    mimetypes.types_map['.js'] = 'application/javascript'
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response