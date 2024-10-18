from fastapi import FastAPI

gapp = FastAPI()


@gapp.get("/wel")
def root():
    return {"message": "My first project ykkk"}
