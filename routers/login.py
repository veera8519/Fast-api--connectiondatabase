from fastapi import APIRouter
from product import schema

router=APIRouter()

@router.post('/login',tags=['LOGIN'])
def login(request:schema.login):
    return request