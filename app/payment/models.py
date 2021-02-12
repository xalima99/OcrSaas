from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class PaymentStatus(Enum):
    CREATED = "CREATED"
    COMPLETED = "COMPLETED"

class BaseOrder(BaseModel):
    currency: str = "USD"
    amount: int

class CreateOrder(BaseOrder):
    pass

class PaymentModel(BaseOrder):
    order_id: str
    order: dict
    user_id: str
    status: PaymentStatus = PaymentStatus.CREATED
    created_at: datetime
    updated_at: datetime

    @classmethod
    async def create(cls, order, user_id, currency, amount):
        payment = cls(order=order, user_id=user_id, currency=currency, amount=amount)
        payment.order_id = order["id"]
        payment.created_at = datetime.now()
        payment.save()
        
        return payment
    
    async def update_status(cls, order_id, user_id):
        pass
    
    def save(self):
        pass