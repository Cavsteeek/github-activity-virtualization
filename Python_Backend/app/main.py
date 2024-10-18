from fastapi import FastAPI, HTTPException


gapp = FastAPI()


@gapp.get("/wel")
def root():
    return {"message": "My first project ykkk"}
