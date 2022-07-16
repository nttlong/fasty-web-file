from fastapi import APIRouter, Depends, Response, status
router = APIRouter()
def router_api_get(path):
    return router.get('/api/'+path)