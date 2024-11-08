from enum import Enum
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import json
from pydantic import BaseModel
from typing import List, Optional

import sys
sys.path.append("..")

from ..keys import read_keys_for_team
from utils import OpenAIModel, openai_chat_completion_streaming

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


@router.get("/message/")
def handle_message(args: MessageArgs):
    keys = read_keys_for_team(team_id=args.team_id)

    if keys is None:
        raise HTTPException(status_code=404, detail="Team ID not found")

    if args.images is not None:
        if args.output_modality == Modality.image:
            # Use Dall-E API
            print("Dall-E API not implemented yet")
            pass
            # if the input contains audio, transcribe with Whisper

        if args.output_modality == Modality.text:
            # Use GPT4o API
            openai_chat_completion_streaming(
                openai_api_key=keys["OPENAI_API_KEY"],
                model=OpenAIModel.gpt4o,
                text=args.text,
                images=args.images
            )
            pass

        if args.output_modality == Modality.audio:
            # Use GPT4o API, and then text-to-speech the result with preferred provider
            print("Text-to-speech API not implemented yet")
            pass

    elif args.output_modality == Modality.audio:
        # Use Hume API
        print("Hume API not implemented yet")
        pass

    elif args.output_modality == Modality.text:
        completion = openai_chat_completion_streaming(
            openai_api_key=keys["OPENAI_API_KEY"],
            model=OpenAIModel.gpt4o,
            text=args.text,
            images=args.images
        )

        def completion_stream(api_response_stream):
            for chunk in api_response_stream:
                # print(chunk)
                if chunk.choices[0].delta.content is not None:
                    yield json.dumps({
                        "modality": "text",
                        "chunk_text": chunk.choices[0].delta.content
                    })

        return StreamingResponse(
            content=completion_stream(completion),
            media_type="text/event-stream"
        )
