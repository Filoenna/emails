from fastapi import FastAPI
import datetime
from . import send_email
from . import api_provider
from . import template
from . import provider

app = FastAPI()
app.include_router(send_email.router)


templates = template.Template(
    {
        "basic": {"title": str, "name": str},
        "store": {"username": str, "item": list},
        "vacation": {"username": str, "date": datetime.date, "email": str},
    }
)


@app.get("/")
async def home():
    return "Home page"


@app.get("/send_mail/")
def send_mail(provider: provider.Provider):
    provider.send_mail()
