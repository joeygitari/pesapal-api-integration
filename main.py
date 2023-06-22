import os
import requests
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from typing import Dict, Union
from dotenv import load_dotenv, find_dotenv
from pydantic import BaseModel, BaseSettings

load_dotenv(find_dotenv())

app = FastAPI()

class User(BaseModel):
    username: str
    password: str

PESAPAL_URL: str = "https://cybqa.pesapal.com/pesapalv3/api/Auth/RequestToken"
PESAPAL_IPN_URL: str = "https://cybqa.pesapal.com/pesapalv3/api/URLSetup/RegisterIPN"
PESAPAL_SUBMIT_ORDER_URL: str = "https://cybqa.pesapal.com/pesapalv3/api/Transactions/SubmitOrderRequest"

consumer_key: str = os.getenv("CONSUMER_KEY")
consumer_secret: str = os.getenv("CONSUMER_SECRET")


class Settings(BaseSettings):
    authjwt_secret_key: str = "secret"


@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


@app.post('/login')
def login(user: User, Authorize: AuthJWT = Depends()):
    if user.username != "test" or user.password != "test":
        raise HTTPException(status_code=401, detail="Bad username or password")

    # subject identifier for who this token is for example id or username from database
    access_token = Authorize.create_access_token(subject=user.username)
    return {"access_token": access_token}


@app.get("/")
async def root():
    # Send a POST request to the Pesapal authentication URL
    response = requests.post(
        PESAPAL_URL,
        json={
            "consumer_key": consumer_key,
            "consumer_secret": consumer_secret,
        }
    )

    # Process the response
    if response.status_code == 200:
        # check if the response status code is 200
        if (response.json()["status"] == "200"):
            # return the access token
            return response.json()
        return {"error": f"Failed to retrieve access token {response.json()}"}
    else:
        # Handle error response
        return {"error": f"Failed to retrieve access token {response.json()}"}


@app.get("/ipnUrl")
async def ipn_url():
    authentication_response = await root()
    # send a POST request to the Pesapal IPN URL
    auth_token = authentication_response["token"]
    response = requests.post(
        PESAPAL_IPN_URL,
        json={
            "url": "http://localhost:3000/ipnUrl",
            "ipn_notification_type": "POST",
        },
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )

    # Process the response
    if response.status_code == 200:
        # check if the response status code is 200
        if (response.json()["status"] == "200"):
            # return the access token
            return_body = {
                "auth_token": auth_token,
                "notification_id": response.json()["ipn_id"],
                "ipnUrl": response.json()["url"]
            }
            return return_body
        return {"error": "Failed to retrieve ipnUrl response"}
    else:
        # Handle error response
        return {"error": "Failed to retrieve ipnUrl response"}


@app.get("/submitOrder")
async def submit_order(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    authentication_response = await ipn_url()
    # send a POST request to the Pesapal SubmitOrderRequest URL
    auth_token = authentication_response["auth_token"]
    notification_id = authentication_response["notification_id"]
    callback_url = authentication_response["ipnUrl"]

    request_body = {
        "id": "098226313f04b4982844bd681498c1a7",
        "currency": "KES",
        "amount": 1000.00,
        "description": "Payment for FENTY BEAUTY",
        "callback_url": f"{callback_url}",
        "notification_id": f"{notification_id}",
        "billing_address": {
            "email_address": "jgitaridev@gmail.com",
            "phone_number": "0706804187",
            "country_code": "KE",
            "first_name": "Joanne",
            "middle_name": "",
            "last_name": "Gitari",
            "line_1": "",
            "line_2": "",
            "city": "Nairobi",
            "state": "Nairobi",
            "postal_code": "00100",
            "zip_code": ""
        }
    }

    response = requests.post(
        PESAPAL_SUBMIT_ORDER_URL,
        json=request_body,
        headers={
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }
    )

    # Process the response
    if response.status_code == 200:
        # check if the response status code is 200
        if (response.json()["status"] == "200"):
            # return the access token
            print(response.json())
            return response.json()
        print(response.json())
        return {"error": f"Fail to retrieve submit order response {response.json()}"}
    else:
        # Handle error response
        return {"error": f"Fail to retrieve submit order response {response.json()}"}
