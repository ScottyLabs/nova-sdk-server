import httpx
import time

LOCALHOST_URL = "http://localhost:8000"

def test_streaming_chat_completion():
    stream_started = False
    with httpx.stream(
        "GET",
        f"{LOCALHOST_URL}/message/",
        json={
            "team_id": "dev",
            "text": "please write me an advertisement for Nova, ScottyLabs' newest event, which gives participants free access to GPT4o!",
            "output_modality": "text"
        }
    ) as response:
        for chunk in response.iter_raw():
            if not stream_started:
                start_time = time.time()
                stream_started = True
            # print(chunk)
            continue

    # We expect the stream to take at least 1 second to complete
    assert time.time() - start_time > 1.0

if __name__ == "__main__":
    test_streaming_chat_completion()

