from typing import Optional, Dict
from datetime import datetime, timedelta

import requests
import json
from jose import jwt

from app.core import settings

def send_email(subject: str, text: str, recipient: str):
    pass

def send_template_email(subject: str, template_name: str, variables: Dict, recipient: str):
    pass

def send_confirmation_email(username: str, verification_token: str, email: str):
    pass

def send_reset_password_email(token: str, email: str):
    pass

def generate_verification_token(email: str) -> str:
    delta = timedelta(hours=72)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email}, settings.SECRET_KEY, algorithm="HS256",
    )
    return encoded_jwt


def check_verification_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token["sub"]
    except jwt.JWTError:
        return None