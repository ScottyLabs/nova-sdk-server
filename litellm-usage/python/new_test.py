""" https://docs.litellm.ai/docs/providers/litellm_proxy#usage-with-langchain-llamaindex-openai-js-anthropic-sdk-instructor """

from litellm import completion
messages = [{ "content": "Hello, how are you?","role": "user"}]
response = completion(
    model="litellm_proxy/claude-3-5-sonnet-20240620", 
    messages=messages, 
    api_base = "https://nova-litellm-proxy.onrender.com/",
    api_key = "************"
)
print(response)
