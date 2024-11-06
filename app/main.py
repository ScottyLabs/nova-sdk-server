from fastapi import FastAPI

from . import keys, messages

app = FastAPI()

app.include_router(keys.router)
app.include_router(messages.router)

def read_root():
    return {"status": "OK"}
