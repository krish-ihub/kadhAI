
import os
import uuid
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

ELEVENLABS_API_KEY = "sk_872e2e5554002f174761a4fb2dfa5e540e6ae887b8a367f6"
client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
)


def text_to_speech_file(text: str) -> str:
    # Calling the text_to_speech conversion API with detailed parameters
    response = client.text_to_speech.convert(
        voice_id="Xb7hH8MSUJpSbSDYk0k2", # Adam pre-made voice
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2_5", # use the turbo model for low latency
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
        ),
    )

    # uncomment the line below to play the audio back
    # play(response)

    # Generating a unique file name for the output MP3 file
    save_file_path = f"{uuid.uuid4()}.mp3"

    # Writing the audio to a file
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!")

    # Return the path of the saved audio file
    return save_file_path

text_to_speech_file("ஒரு பெரிய பூனை ஒரு சிறிய எலியை ஒரு சிறிய எலியில் இருந்து பாதுகாக்கிறது, அது ஒரு சிறிய எலியாக மாறுகிறது, அது ஒரு புதிய வீட்டைக் கட்டுகிறது, அங்கு அது ஒரு புதிய வீட்டைக் கட்டுகிறது. \nகதை:\n ஒரு காலத்தில், ஒரு பெரிய பூனை இருந்தது. அவர் மிகவும் பெரியவர், ஆனால் அவர் மிகவும் அழகானவர். ஒரு நாள், அவர் ஒரு சிறிய எலியைப் பார்த்தார். எலி மிகவும் சிறியது, அது மிகவும் பெரியது. பூனை எலியைப் பாதுகாக்க விரும்பினது, எனவே அவர் எலியைப் பின்தொடர்ந்தார். பூனை எலியைப் பின்தொடர்ந்து சென்றது, ஆனால் அது மிகவும் தாமதமாகிவிட்டது. சுட்டி மிகவும் சிறியதாக இருந்தது, அது எலியைப் பிடிக்க முடியவில்லை. பூனை மிகவும் சோகமாக இருந்தது, ஆனால் பின்னர் அவர் ஒரு புதிய வீட்டை பார்த்தார். அது ஒரு சிறிய எலி! பூனை எலியைப் பார்த்து மிகவும் மகிழ்ச்சியடைந்தது, அது எலியைப் பின்தொடர்வதை நிறுத்த விரும்பினது. எனவே, பூனை எலியைப் பின்தொடர்ந்து, ஒரு சிறிய எலியுடன் ஒரு சிறிய வீட்டைக் கட்டியது. சுட்டி மிகவும் மகிழ்ச்சியாக இருந்தது, அது பூனையை ஒரு புதிய வீடாக மாற்றியது. பூனை எலியைப் பார்த்து மிகவும் மகிழ்ச்சியடைந்தது, அது தனது புதிய வீட்டை நேசித்தது. அன்று முதல், பூனை தனது புதிய வீட்டில் ஒரு புதிய வீட்டைக் கட்ட விரும்பினது.")
