import configparser
from fastapi import APIRouter, HTTPException
from pathlib import Path

router = APIRouter()
configparser = configparser.ConfigParser()

keys_dir = str(Path(__file__).parent) + "/"

@router.get("/keys/")
def read_keys(team_id: str):
    configparser.read(
        keys_dir + "keys.ini"
    )

    if team_id in configparser.sections():
        return configparser[team_id]
    else:
        raise HTTPException(status_code=404, detail="Team ID not found")