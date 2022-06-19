from fastapi_mail import MessageSchema
from typing import List, Dict, Any
from pydantic import EmailStr, BaseModel, BaseSettings


class Mail:
    TO: list[str] = []
    FROM: str
    SUBJECT: str
    BODY: str
    TEMPLATE: str


class EmailSchema(BaseModel):
    email: List[EmailStr]
    body: str
    subject: str


class EmailSchemaForTemplates(BaseModel):
    email: List[EmailStr]
    body: Dict[str, Any]
    subject: str
    template: str
