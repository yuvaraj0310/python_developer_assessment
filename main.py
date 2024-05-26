from fastapi import FastAPI, Depends
from pydantic import BaseModel
from database import (account, destinations)



class IncomingData(BaseModel):
    username : str
    email: str
    contact : str
    password : str
    


app = FastAPI()



@app.post("/server/incoming_data")
def incoming_data(request : IncomingData):
    try:

        # if type(request.model_dump()) == "dict":
        #     return {
        #         "message" : "Invalid Data",
        #         "status" : "failure"
        #     }

        if (accunt_data := account.find_one({"email" : request.email}, {"_id" : 0})) is not None:
            return {
                "message" : "user already exist",
                "status" : "failure"
            }
        else:
            id_ = account.insert_one(request.model_dump()).inserted_id
            destinations.insert_one({"account_id" : str(id_), "message" : "account created"})

            return {
                "message" : "user created",
                "status" : "success",
                "user_id" : str(id_)
            } 

    except Exception as e:
        return str(e)


class Destination(BaseModel):
    message : str



@app.post("/server/destinations/{user_id}")
def destination(request: Destination, user_id : str):

    try:

        print(user_id)
        print(request.message)

        
        data = destinations.update_one({"account_id" : user_id},{"$set" : {"message" : request.message}}).modified_count

        print(data)
        return {
            "message" : "destination completed",
            "modified_count" : str(data)
        }
    except  Exception as e:
        return str(e)
