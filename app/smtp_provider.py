import os
import requests

from fastapi import Depends, HTTPException, APIRouter, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from . import provider
from . import mail
from pathlib import Path
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema

load_dotenv()


router = APIRouter()

router = APIRouter(
    prefix="/email",
    tags=["emails"],
    responses={404: {"description": "Not found"}},
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class SMTPProvider(provider.Provider):
    def __init__(self, name):
        self.username = os.getenv(name + "_MAIL_PASSWORD")
        self.password = os.getenv("GOOGLE_MAIL_PASSWORD")
        self.mail_from = os.getenv(name + "_MAIL_FROM")
        self.port = int(os.getenv(name + "_MAIL_PORT"))
        self.server = os.getenv(name + "_MAIL_SERVER")
        self.tls = os.getenv(name + "_MAIL_TLS")
        self.ssl = os.getenv(name + "_MAIL_SSL")
        self.credentials = os.getenv(name + "_USE_CREDENTIALS")
        self.validate_certs = os.getenv(name + "_VALIDATE_CERTS")

    def set_connection_config(self):
        conf = ConnectionConfig(
            MAIL_USERNAME=self.username,
            MAIL_PASSWORD=self.password,
            MAIL_FROM=self.mail_from,
            MAIL_PORT=self.port,
            MAIL_SERVER=self.server,
            MAIL_TLS=self.tls,
            MAIL_SSL=self.ssl,
            USE_CREDENTIALS=self.credentials,
            VALIDATE_CERTS=self.validate_certs,
            TEMPLATE_FOLDER=Path(__file__).parent / "templates",
        )

        return conf

    def prepare_message(self, email: mail.EmailSchema):
        message = MessageSchema(
            subject=email.dict().get("subject"),
            recipients=email.dict().get("email"),
            template_body=email.dict().get("body"),
            subtype="html",
        )
        return message

    async def send_mail(self, request: Request, message: MessageSchema) -> JSONResponse:
        data = await request.json()
        token = data.get("token")
        sso(token)
        conf = self.set_connection_config()
        fm = FastMail(conf)

        await fm.send_message(message, template_name=data.get("template") + ".html")

        return JSONResponse(status_code=200, content={"message": "email has been sent"})


def sso(
    api_key: str = Depends(oauth2_scheme),
):
    try:
        validation = requests.post(
            "http://127.0.0.1:5000/dj-rest-auth/token/verify/",
            data={"token": api_key},
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
