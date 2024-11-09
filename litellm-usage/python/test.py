PROXY_ENDPOINT = "https://nova-litellm-proxy.onrender.com/"
TEAM_API_KEY = "************"

def example_chat(model_name: str, stream: bool = True):
    """ 
    Examples of chat completions from the proxy
    """
    import openai
    client = openai.OpenAI(
        api_key=TEAM_API_KEY,
        base_url=PROXY_ENDPOINT
    )

    response = client.chat.completions.create(
        model=model_name,
        messages = [
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
    from openai import OpenAI
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
    from openai import OpenAI
    client = OpenAI(   
        base_url=PROXY_ENDPOINT,
        api_key=TEAM_API_KEY
    )

    audio_file= open("./example_audio_input.m4a", "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file,
    )
    print(transcription.text)
    
def example_tts():
    """ 
    Examples of text-to-speech from the proxy
    """
    from openai import OpenAI
    client = OpenAI(   
        base_url=PROXY_ENDPOINT,
        api_key=TEAM_API_KEY
    )
    
    from pathlib import Path

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
    from pydantic import BaseModel
    from openai import OpenAI

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
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful math tutor. Guide the user through the solution step by step."},
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
    import openai
    import requests
    client = openai.OpenAI(
        api_key=TEAM_API_KEY,
        base_url=PROXY_ENDPOINT
    )

    image = client.images.generate(
        prompt="A cute baby sea otter",
        model="dall-e-3",
    )

    print(image)
    url = image.data[0].url
    open("example_image_generation.png", "wb").write(requests.get(url).content)

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
    pass
