import configparser
from fastapi import APIRouter, HTTPException

router = APIRouter()
configparser = configparser.ConfigParser()

@router.get("/keys/")
def read_keys(team_id: str):
    configparser.read("keys.ini")

    if team_id in configparser.sections():
        return configparser[team_id]
    else:
        raise HTTPException(status_code=404, detail="Team ID not found")