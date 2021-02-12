from fastapi import APIRouter, Query
from .exceptions import raise_http_exception
from .paypal import Payment
from .models import CreateOrder, PaymentModel
from uuid import uuid4

payment_router = APIRouter()
payment_router.prefix = "/payments"

payment = Payment()


@payment_router.post("/order")
async def create_order(order: CreateOrder):
    try:
        amount, currency = order.amount, order.currency

        order = payment.create_order(
            amount=amount, currency=currency)
            
        PaymentModel.create(amount=amount, currency=currency,
                            order=order, user_id=uuid4().hex)
        return order
    except Exception as e:
        print(e.args)
        raise_http_exception(e)


@payment_router.get("/capture")
async def capture_order(id: str = Query(..., convert_underscore=True)):
    try:
        response = payment.capture_order(id)

        if response.status_code in [200, 202]:
            PaymentModel.update_status(order_id=id, user_id=uuid4().hex)

        return response
    except Exception as e:
        print(e.args)
        raise_http_exception(e)
