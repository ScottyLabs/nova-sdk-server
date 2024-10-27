import configparser
from fastapi import FastAPI, HTTPException

app = FastAPI()
configparser = configparser.ConfigParser()

@app.get("/")
def read_root():
    return {"status": "OK"}

@app.get("/keys/")
def read_keys(team_id: str):
    configparser.read("keys.ini")

    if team_id in configparser.sections():
        return configparser[team_id]
    else:
        raise HTTPException(status_code=404, detail="Team ID not found")



