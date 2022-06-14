from fastapi import FastAPI
from . import send_email
from . import google
from . import api_provider

app = FastAPI()
app.include_router(send_email.router)


@app.get("/")
async def home():
    return "Home page"


@app.get("/google/")
def gogle():
    google.main()


@app.get("/send_google_mail/")
def google_api():
    provider = api_provider.GoogleApiProvider()
    provider.send_mail()
