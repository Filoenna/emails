import dotenv
from fastapi_mail import ConnectionConfig
import requests

from fastapi import FastAPI, Request, HTTPException, Depends, BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import EmailStr, BaseModel
from typing import List

from fastapi.responses import JSONResponse
import os

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_FROM_NAME=os.getenv("MAIN_FROM_NAME"),
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


class EmailSchema(BaseModel):
    email: List[EmailStr]


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


def get_current_user(token: str = Depends(oauth2_scheme)):
    token2 = "EUREKA " + token
    if token2 == "EUREKA ":
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token2


@app.post("/token")
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


@app.get("/")
async def home(current_user: str = Depends(get_current_user)):
    return current_user


@app.get("/login/")
def loginin():

    lg = requests.post(
        "http://localhost:5000/dj-rest-auth/login/",
        data={"email": "machefi1@gmail.com", "password": "fibbonacci"},
    )
    tokens = lg.content

    return tokens


@app.post("/email")
async def email(
    request: Request, background_tasks: BackgroundTasks, email: EmailSchema
) -> JSONResponse:
    data = await request.json()
    token = data.get("token")
    sso(token)
    message = MessageSchema(
        subject="Fastapi mail module",
        recipients=email.dict().get("email"),
        body="I did it! Simple email, no template so far, but I did it!",
    )

    fm = FastMail(conf)

    background_tasks.add_task(fm.send_message, message)

    return JSONResponse(status_code=200, content={"message": "email has been sent"})
