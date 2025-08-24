
from fastapi import APIRouter, Depends
from ..schemas import EchoRequest, EchoResponse
from ..security import get_current_user_token
from ..rate_limit import rate_limit_dependency

router = APIRouter(prefix="/api/v1", tags=["protected"])

@router.post("/echo", response_model=EchoResponse, dependencies=[Depends(rate_limit_dependency)])
def echo(payload: EchoRequest, user_id: str = Depends(get_current_user_token)):
    # 在这里实现你的业务逻辑（示例：回显）
    return EchoResponse(message=f"user:{user_id} said: {payload.message}")
