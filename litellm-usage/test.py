import asyncio

def test_math_reasoning_proxy():
    from pydantic import BaseModel
    from openai import OpenAI

    client = OpenAI(
        api_key="sk-Jh-HX5lcn5XZsGbY2DeZxA", # 👈 PROXY KEY (can be anything, if master_key not set)
        # api_key="sk-kpwnp9Ex28-OD5YQn6NzxQ", # 👈 PROXY KEY (can be anything, if master_key not set)
        base_url="http://0.0.0.0:4000" # 👈 PROXY BASE URL
        # base_url="https://nova-litellm-proxy.onrender.com" # 👈 PROXY BASE URL
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



def test_image_generation_proxy():
    import openai
    client = openai.OpenAI(
        api_key="sk-PlEKAIXqUbez3NsgWN02JQ",
        # base_url="https://nova-litellm-proxy.onrender.com"
        base_url="http://0.0.0.0:4000"
    )

    image = client.images.generate(
        prompt="A cute baby sea otter",
        model="dall-e-3",
    )

    print(image)

# def test_o1():
#     import openai
#     client = openai.OpenAI(
#         api_key="sk-4k-LoM1WA6KL4M9MTjuAIw",
#         base_url="http://0.0.0.0:4000"
#     )
    
#     response = client.chat.completions.create(
#         model="azure/o1-mini",
#         messages=[
#             {
#                 "role": "user", 
#                 "content": "Write a bash script that takes a matrix represented as a string with format '[1,2],[3,4],[5,6]' and prints the transpose in the same format."
#             }
#         ]
#     )

#     print(response.choices[0].message.content)


    # # request sent to model set on litellm proxy, `litellm --model`
    # # response = client.chat.completions.create(model="gpt-3.5-turbo", messages = [
    # response = client.chat.completions.create(model="o1-mini", messages = [
    #     {
    #         "role": "user",
    #         "content": "this is a test request, write a short poem"
    #     }
    # ])

    # print(response)

    # from openai import OpenAI
    # client = OpenAI(
    #     api_key="sk-4k-LoM1WA6KL4M9MTjuAIw",
    #     base_url="http://0.0.0.0:4000"
    # )

    # response = client.chat.completions.create(model="o1-preview", messages=[{"role": "user", "content": "Hello world"}])
    # print(response)


    # import openai
    # client = openai.OpenAI(
    #     api_key="sk-PlEKAIXqUbez3NsgWN02JQ",
    #     base_url="http://0.0.0.0:4000" # LiteLLM Proxy is OpenAI compatible, Read More: https://docs.litellm.ai/docs/proxy/user_keys
    #     # api_key="sk-kpwnp9Ex28-OD5YQn6NzxQ",
    #     # base_url="https://nova-litellm-proxy.onrender.com/" # LiteLLM Proxy is OpenAI compatible, Read More: https://docs.litellm.ai/docs/proxy/user_keys
    # )

    # response = client.chat.completions.create(
    #     model="o1-preview", # model to send to the proxy
    #     # model="gpt-4", # model to send to the proxy
    #     # model="gemini/gemini-1.5-pro", # model to send to the proxy
    #     messages = [
    #         {
    #             "role": "user",
    #             "content": "Who are you?"
    #         }
    #     ],
    #     stream=True
    # )
    # print(response)

def transcribe_audio():
    from openai import OpenAI
    client = OpenAI(   
        base_url="http://0.0.0.0:4000",
        api_key="sk-4k-LoM1WA6KL4M9MTjuAIw"
    )

    audio_file= open("./test.m4a", "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file,
    )
    print(transcription.text)
    
def tts():
    from openai import OpenAI
    client = OpenAI(   
        base_url="http://0.0.0.0:4000",
        api_key="sk-4k-LoM1WA6KL4M9MTjuAIw"
    )
    
    from pathlib import Path

    speech_file_path = Path(__file__).parent / "speech.mp3"
    response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="Today is a wonderful day to build something people love!"
    )

    response.stream_to_file(speech_file_path)


def test_openai_streaming_proxy():
    import openai
    client = openai.OpenAI(
        api_key="sk-PlEKAIXqUbez3NsgWN02JQ",
        base_url="http://0.0.0.0:4000" # LiteLLM Proxy is OpenAI compatible, Read More: https://docs.litellm.ai/docs/proxy/user_keys
        # api_key="sk-kpwnp9Ex28-OD5YQn6NzxQ",
        # base_url="https://nova-litellm-proxy.onrender.com/" # LiteLLM Proxy is OpenAI compatible, Read More: https://docs.litellm.ai/docs/proxy/user_keys
    )

    response = client.chat.completions.create(
        model="anthropic/claude-3-5-sonnet-20241022", # model to send to the proxy
        # model="gpt-4", # model to send to the proxy
        # model="gemini/gemini-1.5-pro", # model to send to the proxy
        messages = [
            {
                "role": "user",
                "content": "Who are you?"
            }
        ],
        stream=True
    )

    for chunk in response:
        print(chunk)

# def test_gemini_streaming_proxy():
#     """ TODO: CREATE A WRAPPER AROUND THIS CODE """
#     import requests

#     response = requests.post(
#         "https://nova-litellm-proxy.onrender.com/chat/completions",
#         headers={"Authorization": f"Bearer sk-G9snAgjEYkAJjzB-GkERow"},
#         json={
#             "model": "gemini-1.5-pro",
#             "messages": [{"role": "user", "content": "List 5 popular cookie recipes."}],
#         },
#     )

#     print(response.json())
    
# async def test_gemini_streaming_proxy_async():
#     import openai
#     client = openai.AsyncOpenAI(
#         api_key="sk-G9snAgjEYkAJjzB-GkERow",            # litellm proxy api key
#         base_url="https://nova-litellm-proxy.onrender.com" # litellm proxy base url
#     )


#     response = await client.chat.completions.create(
#         model="gemini-1.5-pro",
#         messages=[
#             {
#                 "role": "system",
#                 "content": [
#                         {
#                             "type": "text",
#                             "text": "Here is the full text of a complex legal agreement" * 4000,
#                             "cache_control": {"type": "ephemeral"}, # 👈 KEY CHANGE
#                         }
#                 ],
#             },
#             {
#                 "role": "user",
#                 "content": "what are the key terms and conditions in this agreement?",
#             },
#         ],
#     )
    
#     for chunk in response:
#         print(chunk)

# def test_claude_streaming_proxy():
#     """ TODO: CREATE A WRAPPER AROUND THIS CODE """
#     import requests

#     response = requests.post(
#         "https://nova-litellm-proxy.onrender.com/chat/completions",
#         headers={"Authorization": f"Bearer sk-G9snAgjEYkAJjzB-GkERow"},
#         json={
#             "model": "claude-3.5-sonnet",
#             "messages": [{"role": "user", "content": "List 5 popular cookie recipes."}],
#         },
#     )
#     print(response.json())

def test_embeddings_proxy():
    from openai import OpenAI
    client = OpenAI(
        api_key="sk-PlEKAIXqUbez3NsgWN02JQ",
        base_url="http://0.0.0.0:4000"
    )

    embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input="The food was delicious and the waiter...",
        encoding_format="float"
    )

    print(embedding)

# if __name__ == "__main__":
#     # test_math_reasoning_proxy()
#     # test_image_generation_proxy()
#     # test_openai_streaming_proxy()
#     # test_gemini_streaming_proxy()
#     # test_claude_streaming_proxy()
#     # asyncio.run(test_gemini_streaming_proxy_async())
#     # test_embeddings_proxy()
#     # test_o1()
#     # transcribe_audio()
#     # tts()
#     test_gemini_streaming_proxy_async()
#     pass


################################################################################
################################################################################
################################################################################

PROXY_ENDPOINT = "https://nova-litellm-proxy.onrender.com/"
TEAM_API_KEY = "sk-ewS5OjKr85inbWbzALELAA"
# PROXY_ENDPOINT = "http://0.0.0.0:4000"
# TEAM_API_KEY = "sk-PlEKAIXqUbez3NsgWN02JQ"

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
    # example_chat("gpt-4o", stream=True)
    # example_chat("gpt-4o", stream=False)
    # example_chat("gemini/gemini-1.5-pro", stream=True)
    # example_chat("gemini/gemini-1.5-pro", stream=False)
    # example_embeddings()
    # example_audio_transcription()
    # example_tts()
    # example_response_parsing()
    example_image_generation()


# curl -X POST "https://nova-litellm-proxy.onrender.com/model/new" \
#     -H 'Authorization: Bearer nova-2024' \
#     -H "Content-Type: application/json" \
#     -d '{ "model_name": "*", "litellm_params": {"model": "*"} }'


