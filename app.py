from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import database_access as db
from nanoid import generate

server = FastAPI()


class Link(BaseModel):
    longLink: str


@server.get("/", status_code=200)
def root():
    return {"Message": "Welcome to the root"}


@server.get("/{short_link}", status_code=200)
def redirect(short_link: str):
    element = db.find_by_short(short_link)
    if element is not None:
        return RedirectResponse(element["longLink"])
    
    return {"Error": "Please double check your shortlink"}

@server.post("/shorten/", status_code=201)
def shorten_link(link: Link):
    element = db.insert_new_link(link.longLink)
    return ({
        "longLink": element["longLink"],
        "shortLink": element["shortLink"]
            })


