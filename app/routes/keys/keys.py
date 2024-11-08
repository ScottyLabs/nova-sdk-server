import configparser
from fastapi import APIRouter, HTTPException
from pathlib import Path
from typing import Dict, Optional

router = APIRouter()

configparser = configparser.ConfigParser()
KEYS_DIR = str(Path(__file__).parent) + "/"


def read_keys_for_team(*, team_id: str) -> Optional[Dict[str, str]]:
    """ Reads the keys for a given team ID from the keys.ini file in this folder.
    
    ### Parameters:
    1. team_id : str
        - The team ID to read the keys for.
    
    ### Returns:
    - dict[str, str]:
        - The keys for the given team ID.
        - You can expect there to be the following keys: "OPENAI_API_KEY"
    - None
        - if there is no section for the given team ID.
    """
    configparser.read(KEYS_DIR + "keys.ini")

    if team_id in configparser.sections():
        return configparser[team_id] 


@router.get("/keys/")
def read_keys(team_id: str):
    keys = read_keys_for_team(team_id=team_id)

    if keys is not None:
        return keys
    else:
        raise HTTPException(status_code=404, detail="Team ID not found")