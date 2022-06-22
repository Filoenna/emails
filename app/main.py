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

providers = providers.Providers(
    {
        "google_api": api_provider.GoogleApiProvider(),
        "google": smtp_provider.SMTPProvider("GMAIL"),
    }
)


@app.get("/")
async def home():
    return "Home page"


@app.post("/send_mail/")
async def send_mail(request: Request, email: mail.EmailSchema):
    data = await request.json()
    provider_name = data.get("provider")
    provider = providers[provider_name]
    prepared_message = provider.prepare_message(email)
    provider.send_mail(prepared_message)
