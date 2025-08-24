
import hmac, hashlib
from fastapi import APIRouter, Header, HTTPException, Request, status
from ..config import settings

router = APIRouter(prefix="/billing", tags=["billing"])

@router.post("/stripe/webhook")
async def stripe_webhook(request: Request, stripe_signature: str | None = Header(default=None)):
    # 占位：示例性验证（实际 Stripe 使用专有签名头 'Stripe-Signature'，此处为演示）
    if settings.stripe_webhook_secret:
        body = await request.body()
        mac = hmac.new(settings.stripe_webhook_secret.encode(), msg=body, digestmod=hashlib.sha256).hexdigest()
        provided = (stripe_signature or "").split(",")[-1] if stripe_signature else ""
        if provided != mac:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid webhook signature")

    event = await request.json()
    # TODO: 根据 `event['type']` 处理订阅、发票等事件
    return {"received": True}
