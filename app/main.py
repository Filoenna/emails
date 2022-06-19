from fastapi import FastAPI, Request
import datetime
from . import send_email
from . import api_provider
from . import smtp_provider
from . import template
from . import providers
from . import mail

app = FastAPI()
app.include_router(send_email.router)


templates = template.Template(
    {
        "basic": {"title": str, "name": str},
        "store": {"username": str, "item": list},
        "vacation": {"username": str, "date": datetime.date, "email": str},
    }
)

providers = providers.Provider(
    {
        "google_api": api_provider.GoogleApiProvider(),
        "google": smtp_provider.SMTPProvider("GOOGLE"),
    }
)


@app.get("/")
async def home():
    return "Home page"


@app.get("/send_mail/")
def send_mail(
    request: Request, provider_name: str, email: mail.EmailSchemaForTemplates
):
    provider = providers[provider_name]
    provider.send_email()
