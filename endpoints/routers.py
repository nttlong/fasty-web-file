from fastapi import APIRouter, Depends, Response, status
router = APIRouter()
def router_api_get(path):
    return router.get('/api/'+path)
def router_api_post(path,response_model=None):
    if response_model is not  None:
        return router.post('/api/' + path,response_model=response_model)

    return router.post('/api/'+path)