from fastapi import FastAPI
from pydantic import BaseModel
from scr.dbconnector import DBConnector
from scr.manager import Manager


app = FastAPI()
manager = Manager()
db = DBConnector(dbname="d2d1ljqhqhl34q",
                 user="udmehkiskcczbm",
                 password="d4f6d3d3a48a96f498f7829d75ef285bd9777989c15a135aa5a72903fc86127e",
                 address=("ec2-54-161-164-220.compute-1.amazonaws.com", "5432"))


class SignUp(BaseModel):
    name: str
    surname: str
    email: str
    phone_number: str


@app.route("/api/signup/")
async def signup(user: SignUp):

    if not manager.check_spelling(user.name):
        return {"message": "check your spelling at name field"}
    if not manager.check_spelling(user.surname):
        return {"message": "check your spelling at surname field"}
    if not manager.check_spelling(user.email, email=True):
        return {"message": "check your spelling at email field"}
    if not manager.check_spelling(user.phone_number, phone_number=True):
        return {"message": "check your spelling at phone_number field"}

    if db.check_if_value_exists("email", user.email):
        return {"message": "this email already exists"}
    if db.check_if_value_exists("phone_number", user.phone_number):
        return {"message": "this phone number already exists"}

    db.signup_user(user)

    return {"message": "user signed up successfully"}
