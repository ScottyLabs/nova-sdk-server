from enum import Enum
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class Modality(str, Enum):
    text = "text"
    image = "image"
    audio = "audio"

class MessageArgs(BaseModel):
    team_id: str
    text: Optional[str] = None
    images: Optional[List[str]] = None
    output_modality: Modality

@router.post("/message/")
def handle_message(args: MessageArgs):
    if args.images is not None:
        if args.output_modality == Modality.image:
            # Use Dall-E API
            pass
            # if the input contains audio, transcribe with Whisper

        if args.output_modality == Modality.text:
            # Use GPT4o API
            pass

        if args.output_modality == Modality.audio:
            # Use GPT4o API, and then text-to-speech the result with preferred provider
            pass

    elif args.output_modality == Modality.audio:
        # Use Hume API
        pass

    elif args.output_modality == Modality.text:
        # Might be able to use Hume as well?
        pass
