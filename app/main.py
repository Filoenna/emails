from fastapi import FastAPI
from . import send_email

app = FastAPI()
app.include_router(send_email.router)


@app.get("/")
async def home():
    return "Home page"
