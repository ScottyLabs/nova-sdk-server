from enum import Enum
from openai import OpenAI
from typing import Optional, List


class OpenAIModel(str, Enum):
  gpt4o = "gpt-4o"
  o1 = "o1"
  dall_e = "dall-e"

def openai_chat_completion_streaming(
    *,
    openai_api_key: str,
    model: OpenAIModel,
    text: str,
    images: Optional[List[str]] = None
) -> List[str]:
  client = OpenAI(api_key=openai_api_key)

  return client.chat.completions.create(
    model=model,
    messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": text}
    ],
    stream=True
  )

