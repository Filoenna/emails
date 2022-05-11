from re import template
from fastapi import APIRouter, Request, HTTPException, Depends, BackgroundTasks
from fastapi_mail import ConnectionConfig
import requests
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import EmailStr, BaseModel, BaseSettings
from typing import List, Dict, Any
from pathlib import Path
from fastapi.responses import JSONResponse
import os

from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

router = APIRouter(
    prefix="/email",
    tags=["emails"],
    responses={404: {"description": "Not found"}},
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def set_connection_config(provider: str):
    print(os.getenv(provider + "_MAIL_PORT"))
    conf = ConnectionConfig(
        MAIL_USERNAME=os.getenv(provider + "_MAIL_USERNAME"),
        MAIL_PASSWORD=os.getenv(provider + "_MAIL_PASSWORD"),
        MAIL_FROM=os.getenv(provider + "_MAIL_FROM"),
        MAIL_PORT=int(os.getenv(provider + "_MAIL_PORT")),
        MAIL_SERVER=os.getenv(provider + "_MAIL_SERVER"),
        MAIL_FROM_NAME=os.getenv(provider + "_MAIN_FROM_NAME"),
        MAIL_TLS=True,
        MAIL_SSL=False,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True,
        TEMPLATE_FOLDER=Path(__file__).parent / "templates",
    )
    return conf


class EmailSchema(BaseModel):
    email: List[EmailStr]
    body: str
    subject: str


class EmailSchemaForTemplates(BaseModel):
    email: List[EmailStr]
    body: Dict[str, Any]
    subject: str
    template: str


def sso(
    APIKey: str = Depends(oauth2_scheme),
):
    try:
        validation = requests.post(
            "http://127.0.0.1:5000/dj-rest-auth/token/verify/",
            data={"token": APIKey},
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)
    else:
        if validation.status_code != 200:
            raise HTTPException(status_code=401, detail=validation.text)
    return True


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data.username)
    print(form_data.password)
    data = {"email": form_data.username, "password": form_data.password}
    sso = requests.post(
        "http://127.0.0.1:5000/dj-rest-auth/login/",
        data,
    )
    content = sso.json()
    print(content["access_token"])
    if sso.status_code != 200:
        raise HTTPException(
            status_code=401,
        )
    return content["access_token"]


@router.post("/send")
async def email(
    request: Request, background_tasks: BackgroundTasks, email: EmailSchema
) -> JSONResponse:
    data = await request.json()
    token = data.get("token")
    provider = data.get("provider")
    sso(token)
    print(email.dict)
    message = MessageSchema(
        subject=email.dict().get("subject"),
        recipients=email.dict().get("email"),
        body=email.dict().get("body"),
    )
    conf = set_connection_config(provider)
    fm = FastMail(conf)

    background_tasks.add_task(fm.send_message, message)

    return JSONResponse(status_code=200, content={"message": "email has been sent"})


@router.post("/sendtemplate")
async def email_from_template(
    request: Request, email: EmailSchemaForTemplates
) -> JSONResponse:
    data = await request.json()
    token = data.get("token")
    provider = data.get("provider")
    sso(token)
    message = MessageSchema(
        subject=email.dict().get("subject"),
        recipients=email.dict().get("email"),
        template_body=email.dict().get("body"),
        subtype="html",
    )
    conf = set_connection_config(provider)
    fm = FastMail(conf)

    await fm.send_message(message, template_name=data.get("template") + ".html")

    return JSONResponse(status_code=200, content={"message": "email has been sent"})
