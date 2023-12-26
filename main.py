from record import Recorder
from openai import OpenAI
import os
from playsound import playsound
from pathlib import Path

client = OpenAI(api_key=os.environ['OPENAI_KEY'])

def play_audio(file_path):
    playsound(file_path)
def main():
    recorder = Recorder()
    greeted = False

    while True:
        try:
            greeting = client.audio.speech.create(
                model="tts-1",
                voice="fable",
                input="Hello I am The Disk, AI created by Deepware. How can I help you?"
            )
            if(not greeted):
                Path("response.mp3").unlink(missing_ok=True)
                greeting.stream_to_file("response.mp3")
                play_audio('response.mp3')
                greeted = True
            recorder.start_recording()
            input("Press Enter to stop recording")
            recorder.stop_recording()
            with open('rec.wav', 'rb') as audio_file:
                transcript = client.audio.transcriptions.create(
                    model='whisper-1', file=audio_file, response_format="text"
                )

                if "exit" in transcript.lower():
                    break


            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant built by Deepware. Your name is The Disk. Always answer to the point and consise. Try to keep the conversation continue by asking back question like human. Browse internet for current date and time."},
                    {"role": "user", "content": transcript}
                ]
            )

            voice_response = client.audio.speech.create(
                model="tts-1",
                voice="fable",
                input=str(response.choices[0].message.content)
            )
            Path("response.mp3").unlink(missing_ok=True)
            voice_response.stream_to_file("response.mp3")
            play_audio('response.mp3')

        except Exception as e:
            print(f"An error occurred: {e}")
            break

if __name__ == "__main__":
    main()
