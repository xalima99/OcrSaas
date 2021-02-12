import os
from pprint import pprint
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment, LiveEnvironment

from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest

from paypalhttp import HttpError

class Payment:
    
    def __init__(self, environment="sandbox"):
        environments = {"sandbox": SandboxEnvironment,
                        "live": LiveEnvironment
                        }
        # Creating Access Token for Sandbox
        client_id = os.environ["PAYPAL_CLIENT_ID"]
        client_secret = os.environ["PAYPAL_CLIENT_SECRET"]
        # Creating an environment
        self.environment = environments[environment](client_id=client_id, client_secret=client_secret)
        self.client = PayPalHttpClient(self.environment)
    
    def create_order(self, amount, currency="USD"):
        # Construct a request object and set desired parameters
        # Here, OrdersCreateRequest() creates a POST request to /v2/checkout/orders
        request = OrdersCreateRequest()

        request.prefer('return=representation')

        request.request_body (
            {
                "intent": "CAPTURE",
                "purchase_units": [
                    {
                        "amount": {
                            "currency_code": currency,
                            "value": str(amount)
                        }
                    }
                ]
            }
        )

        try:
            # Call API with your client and get a response for your call
            response = self.client.execute(request)
            order_result = response.result
            order = {
                "id": order_result.id,
                "status_code": response.status_code,
                "status": order_result.status,
                "intent": order_result.intent,
                "links": {}
            }
            for link in order_result.links:
                order["links"][link.rel] = {"href": link.href, "method": link.method,
                                            "currency": order_result.purchase_units[0].amount.currency_code,
                                            "amount": order_result.purchase_units[0].amount.value}
            pprint(order)
            return order
        except IOError as ioe:
            print(ioe)
            if isinstance(ioe, HttpError):
                # Something went wrong server-side
                print(ioe.status_code)
            raise IOError(ioe.args)

    def capture_request(self, order_id):
        request = OrdersCaptureRequest(order_id)

        try:
            # Call API with your client and get a response for your call
            response = self.client.execute(request)

            # If call returns body in response, you can get the deserialized version from the result attribute of the response
            order = response.result.id
            pprint(response.result)
            return order
        except IOError as ioe:
            if isinstance(ioe, HttpError):
                # Something went wrong server-side
                print(ioe.status_code)
                print(ioe.headers)
                print(ioe)
            else:
                # Something went wrong client side
                print(ioe)
            raise ioe