from fastapi.exceptions import HTTPException

def raise_http_exception(e):
    raise HTTPException(detail=", ".join([str(arg) for arg in e.args]), status_code=422)