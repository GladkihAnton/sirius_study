from fastapi import Body, Query
from pydantic import BaseModel


class LoginQuery(BaseModel):
    email: str = Query()
    password: str = Query()
