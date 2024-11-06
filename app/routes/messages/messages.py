from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class MessageArgs(BaseModel):
    team_id: str
    text: Optional[str] = None
    images: Optional[List[str]] = None

@router.post("/message/")
def handle_message(args: MessageArgs):
    pass
