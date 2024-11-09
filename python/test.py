import openai
import litellm
import json
import requests
from openai import OpenAI
from pathlib import Path
from pydantic import BaseModel
import os

PROXY_ENDPOINT = "https://nova-litellm-proxy.onrender.com/"
TEAM_API_KEY = os.getenv("TEAM_EXAMPLE_KEY")


def example_chat(model_name: str, stream: bool = True):
    """
    Examples of chat completions from the proxy
    """
    client = openai.OpenAI(
        api_key=TEAM_API_KEY,
        base_url=PROXY_ENDPOINT
    )

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "user",
                "content": "Who are you?"
            }
        ],
        stream=stream
    )

    for chunk in response:
        print(chunk)


def example_embeddings():
    """
    Examples of embeddings from the proxy
    """
    client = OpenAI(
        api_key=TEAM_API_KEY,
        base_url=PROXY_ENDPOINT
    )

    embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input="The food was delicious and the waiter...",
        encoding_format="float"
    )
    print(embedding)


def example_audio_transcription():
    """
    Examples of audio transcription from the proxy
    """
    client = OpenAI(
        base_url=PROXY_ENDPOINT,
        api_key=TEAM_API_KEY
    )

    audio_file = open("./example_audio_input.m4a", "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
    )
    print(transcription.text)


def example_tts():
    """
    Examples of text-to-speech from the proxy
    """
    client = OpenAI(
        base_url=PROXY_ENDPOINT,
        api_key=TEAM_API_KEY
    )

    speech_file_path = Path(__file__).parent / "example_tts_output.mp3"
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input="Welcome to the future of Generative AI! Today is a wonderful day to build something people love!"
    )

    response.stream_to_file(speech_file_path)


def example_response_parsing():
    """
    Examples of chat completions with response parsing from the proxy
    """

    client = OpenAI(
        api_key=TEAM_API_KEY,
        base_url=PROXY_ENDPOINT
    )

    class Step(BaseModel):
        explanation: str
        output: str

    class MathReasoning(BaseModel):
        steps: list[Step]
        final_answer: str

    completion = client.beta.chat.completions.parse(
        model="openai/gpt-4o",
        messages=[
            {"role": "system",
             "content": "You are a helpful math tutor. Guide the user through the solution step by step."},
            {"role": "user", "content": "how can I solve 8x + 7 = -23"}
        ],
        response_format=MathReasoning,
    )

    math_reasoning = completion.choices[0].message.parsed
    print(math_reasoning)


def example_image_generation():
    """
    Examples of image generation from the proxy
    """
    client = openai.OpenAI(
        api_key=TEAM_API_KEY,
        base_url=PROXY_ENDPOINT
    )

    image = client.images.generate(
        prompt="NOVA, the greatest gen-AI hackathon!",
        model="dall-e-3",
    )

    print(image)
    url = image.data[0].url
    open("example_image_generation.png", "wb").write(requests.get(url).content)


def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    if "tokyo" in location.lower():
        return json.dumps({"location": "Tokyo", "temperature": "10", "unit": "celsius"})
    elif "san francisco" in location.lower():
        return json.dumps({"location": "San Francisco", "temperature": "72", "unit": "fahrenheit"})
    elif "paris" in location.lower():
        return json.dumps({"location": "Paris", "temperature": "22", "unit": "celsius"})
    else:
        return json.dumps({"location": location, "temperature": unit})


def example_function_calling():
    try:
        # Step 1: send the conversation and available functions to the model
        messages = [{"role": "user", "content": "What's the weather like in San Francisco, Tokyo, and Paris?"}]
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "Get the current weather in a given location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state, e.g. San Francisco, CA",
                            },
                            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                        },
                        "required": ["location"],
                    },
                },
            }
        ]
        response = litellm.completion(
            model="gpt-3.5-turbo-1106",
            messages=messages,
            tools=tools,
            tool_choice="auto",  # auto is default, but we'll be explicit
            api_base=PROXY_ENDPOINT,
            api_key=TEAM_API_KEY
        )
        print("\nFirst LLM Response:\n", response)
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        print("\nLength of tool calls", len(tool_calls))

        # Step 2: check if the model wanted to call a function
        if tool_calls:
            # Step 3: call the function
            # Note: the JSON response may not always be valid; be sure to handle errors
            available_functions = {
                "get_current_weather": get_current_weather,
            }  # only one function in this example, but you can have multiple
            messages.append(response_message)  # extend conversation with assistant's reply

            # Step 4: send the info for each function call and function response to the model
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                function_response = function_to_call(
                    location=function_args.get("location"),
                    unit=function_args.get("unit"),
                )
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )  # extend conversation with function response
            second_response = litellm.completion(
                model="gpt-3.5-turbo-1106",
                messages=messages,
                api_base=PROXY_ENDPOINT,
                api_key=TEAM_API_KEY
            )  # get a new response from the model where it can see the function response
            print("\nSecond LLM response:\n", second_response)
            return second_response
    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    # example_chat("anthropic/claude-3-5-sonnet-20241022", stream=True)
    # example_chat("anthropic/claude-3-5-sonnet-20241022", stream=False)
    # example_chat("openai/gpt-4o", stream=True)
    # example_chat("openai/gpt-4o", stream=False)
    # example_chat("gpt-4o-mini", stream=True)
    # example_chat("gpt-4o-mini", stream=False)
    # example_chat("gemini/gemini-1.5-pro", stream=True)
    # example_chat("gemini/gemini-1.5-pro", stream=False)
    # example_embeddings()
    # example_audio_transcription()
    # example_tts()
    # example_response_parsing()
    # example_image_generation()
    example_function_calling()
    pass
