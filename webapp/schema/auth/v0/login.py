from fastapi import Body
from pydantic import BaseModel


class LoginQuery(BaseModel):
    email: str
    password: str
