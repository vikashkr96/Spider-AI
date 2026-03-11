import pygame
import random
import asyncio
import edge_tts
import os
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice", "en-CA-LiamNeural")

AUDIO_PATH = r"Data\speech.mp3"


async def TextToAudioFile(text: str) -> None:
    if os.path.exists(AUDIO_PATH):
        os.remove(AUDIO_PATH)

    communicate = edge_tts.Communicate(
        text=text,
        voice=AssistantVoice,
        pitch="+5Hz",
        rate="+13%"
    )

    await communicate.save(AUDIO_PATH)


def TTS(text, func=lambda: True):
    try:
        asyncio.run(TextToAudioFile(text))

        if not pygame.mixer.get_init():
            pygame.mixer.init()

        pygame.mixer.music.load(AUDIO_PATH)
        pygame.mixer.music.play()

        clock = pygame.time.Clock()

        while pygame.mixer.music.get_busy():
            if func() is False:
                break
            clock.tick(10)

        return True

    except Exception as e:
        print(f"TTS Error: {e}")
        return False

    finally:
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()

        if os.path.exists(AUDIO_PATH):
            try:
                os.remove(AUDIO_PATH)
            except:
                pass
            
def TextToSpeech(Text, func=lambda: True):
    Data = str(Text).split(".")

    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information."
    ]

    if len(Data) > 4 and len(Text) > 250:
        short_text = ". ".join(Data[:2]) + ". " + random.choice(responses)
        TTS(short_text, func)
    else:
        TTS(Text, func)

if __name__ == "__main__":
    while True:
        text = input("Enter the text: ").strip()
        if not text:
            continue
        TextToSpeech(text)
