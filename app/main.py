import requests

from fastapi import FastAPI, Request, HTTPException, Depends
from starlette.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
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
        "http://127.0.0.1:8000/dj-rest-auth/login/",
        data,
    )
    print(sso)
    if sso.status_code != 200:
        raise HTTPException(
            status_code=401,
        )
    return sso


@app.get("/")
async def home(current_user: str = Depends(get_current_user)):
    return current_user


@app.get("/login/")
def loginin():

    lg = requests.post(
        "http://127.0.0.1:8000/dj-rest-auth/login/",
        data={"email": "machefi1@gmail.com", "password": "fibbonacci"},
    )

    return lg


@app.post("/email")
# @login_required
async def email(request: Request):
    return "<h1>Home page</h1>"
